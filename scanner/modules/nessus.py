"""
nessus.py
---------
Handles all communication with Nessus through its REST API.

This module automates everything we did manually in the Nessus web
interface during the assessment:
  - connecting and authenticating
  - creating a "Basic Network Scan"
  - launching it against the target
  - waiting for it to finish
  - downloading and organizing the results

Nessus exposes a REST API on its web port (default 8834). We talk to it
using the 'requests' library. Because Nessus uses a self-signed HTTPS
certificate by default, we disable certificate verification for these
local requests (safe in a controlled lab, but noted as a caveat).
"""

import time
import requests

# Nessus uses a self-signed certificate locally, which would normally
# trigger SSL warnings. We disable verification and silence the warning,
# because in our controlled lab this is expected behavior.
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# How often (in seconds) we check whether the scan has finished
POLL_INTERVAL = 30


def build_headers(access_key, secret_key):
    """
    Build the authentication headers Nessus expects on every API request.

    Nessus API key authentication uses a single header in the format:
        X-ApiKeys: accessKey=<key>; secretKey=<key>

    Returns a dictionary of headers.
    """
    return {
        "X-ApiKeys": f"accessKey={access_key}; secretKey={secret_key}",
        "Content-Type": "application/json",
    }


def check_nessus_reachable(url, headers):
    """
    Pre-flight check — confirm Nessus is running, reachable, and that our
    API keys are accepted, BEFORE we try to do any real work.

    This is the safeguard we discussed: rather than crashing later, we
    fail early with a clear, helpful message.

    Returns True if everything is good, False otherwise.
    """
    print("\n[*] Checking connection to Nessus ...")

    try:
        # The /server/status endpoint is a lightweight way to test the
        # connection. It tells us whether the server is ready.
        response = requests.get(
            f"{url}/server/status",
            headers=headers,
            verify=False,      # accept the self-signed cert
            timeout=10
        )
    except requests.exceptions.ConnectionError:
        print("[!] Could not connect to Nessus.")
        print(f"    Is Nessus running and reachable at {url}?")
        print("    Start it with: sudo systemctl start nessusd")
        print("    See scanner/docs/SETUP.md for full setup instructions.")
        return False
    except requests.exceptions.Timeout:
        print("[!] Connection to Nessus timed out.")
        print("    Nessus may still be starting up. Wait a moment and retry.")
        return False

    # A 401 status means our API keys were rejected
    if response.status_code == 401:
        print("[!] Nessus rejected the API keys.")
        print("    Double-check your Access Key and Secret Key.")
        print("    Generate new ones in Nessus under My Account > API Keys.")
        return False

    if response.status_code != 200:
        print(f"[!] Nessus returned an unexpected status: {response.status_code}")
        return False

    # Check whether the server reports itself as ready
    status = response.json().get("status", "unknown")
    if status != "ready":
        print(f"[!] Nessus is reachable but not ready (status: {status}).")
        print("    It may still be initializing plugins. Try again shortly.")
        return False

    print("[+] Connected to Nessus successfully.")
    return True


def get_scan_template_uuid(url, headers):
    """
    Find the unique ID (UUID) of the "Basic Network Scan" template.

    Nessus identifies each scan type by a UUID rather than its name, so we
    must look it up. This is the same template we selected manually in the
    web interface.

    Returns the UUID string, or None if it can't be found.
    """
    print("[*] Locating the 'Basic Network Scan' template ...")

    response = requests.get(
        f"{url}/editor/scan/templates",
        headers=headers,
        verify=False,
        timeout=15
    )

    if response.status_code != 200:
        print("[!] Could not retrieve scan templates.")
        return None

    templates = response.json().get("templates", [])

    # Search the templates for the one named "Basic Network Scan"
    for template in templates:
        if template.get("name") == "basic":
            print("[+] Found the Basic Network Scan template.")
            return template.get("uuid")

    print("[!] Could not find the Basic Network Scan template.")
    return None


def create_scan(url, headers, template_uuid, target_ip, scan_name):
    """
    Create a new scan in Nessus targeting our IP.

    This is the equivalent of filling in the 'New Scan' form in the web
    interface: choosing the template, naming the scan, and entering the
    target.

    Returns the new scan's ID number, or None on failure.
    """
    print(f"[*] Creating scan '{scan_name}' for target {target_ip} ...")

    # The settings mirror what we filled in manually
    payload = {
        "uuid": template_uuid,
        "settings": {
            "name": scan_name,
            "text_targets": target_ip,
            "enabled": True,
        }
    }

    response = requests.post(
        f"{url}/scans",
        headers=headers,
        json=payload,
        verify=False,
        timeout=15
    )

    if response.status_code != 200:
        print(f"[!] Failed to create scan (status {response.status_code}).")
        return None

    scan_id = response.json()["scan"]["id"]
    print(f"[+] Scan created with ID {scan_id}.")
    return scan_id


def launch_scan(url, headers, scan_id):
    """
    Launch (start) a scan that has already been created.

    Returns True if the scan started successfully, False otherwise.
    """
    print("[*] Launching the scan ...")

    response = requests.post(
        f"{url}/scans/{scan_id}/launch",
        headers=headers,
        verify=False,
        timeout=15
    )

    if response.status_code != 200:
        print(f"[!] Failed to launch scan (status {response.status_code}).")
        return False

    print("[+] Scan launched. Now waiting for it to complete.")
    return True


def wait_for_completion(url, headers, scan_id):
    """
    Repeatedly check the scan's status until it finishes.

    Nessus reports a scan's status as 'running', 'completed', etc. We poll
    every POLL_INTERVAL seconds and print progress so the user knows the
    program hasn't frozen.

    Returns True when the scan completes, False if it fails or is canceled.
    """
    elapsed = 0

    while True:
        response = requests.get(
            f"{url}/scans/{scan_id}",
            headers=headers,
            verify=False,
            timeout=15
        )

        if response.status_code != 200:
            print("[!] Lost connection while checking scan status.")
            return False

        # The current status lives under info > status
        status = response.json()["info"]["status"]

        if status == "completed":
            print(f"\n[+] Scan completed after about {elapsed // 60} minutes.")
            return True

        if status in ("canceled", "aborted"):
            print(f"\n[!] Scan ended unexpectedly with status: {status}")
            return False

        # Still running — report progress and wait before checking again
        minutes = elapsed // 60
        seconds = elapsed % 60
        print(f"    Scan status: {status} "
              f"(elapsed {minutes}m {seconds}s) ...", end="\r")

        time.sleep(POLL_INTERVAL)
        elapsed += POLL_INTERVAL


def get_findings(url, headers, scan_id):
    """
    Download the scan results and organize the vulnerabilities by severity.

    Nessus returns a list of vulnerabilities, each with a severity number:
        4 = Critical, 3 = High, 2 = Medium, 1 = Low, 0 = Informational

    We translate those numbers into readable labels and group the findings.

    Returns a dictionary grouping findings under each severity label.
    """
    print("[*] Downloading scan results ...")

    response = requests.get(
        f"{url}/scans/{scan_id}",
        headers=headers,
        verify=False,
        timeout=30
    )

    if response.status_code != 200:
        print("[!] Failed to download scan results.")
        return None

    vulnerabilities = response.json().get("vulnerabilities", [])

    # Map Nessus severity numbers to human-readable labels
    severity_labels = {
        4: "Critical",
        3: "High",
        2: "Medium",
        1: "Low",
        0: "Info",
    }

    # Prepare empty groups
    findings = {
        "Critical": [],
        "High": [],
        "Medium": [],
        "Low": [],
        "Info": [],
    }

    # Sort each vulnerability into the right group
    for vuln in vulnerabilities:
        severity_number = vuln.get("severity", 0)
        label = severity_labels.get(severity_number, "Info")

        findings[label].append({
            "name": vuln.get("plugin_name", "Unknown"),
            "family": vuln.get("plugin_family", "Unknown"),
            "count": vuln.get("count", 0),
        })

    # Print a quick summary so the user sees the outcome immediately
    print("[+] Results downloaded. Summary:")
    for label in ["Critical", "High", "Medium", "Low", "Info"]:
        print(f"      {label:<10}: {len(findings[label])} findings")

    return findings


def format_findings_text(findings, target_ip):
    """
    Build a readable text summary of the Nessus findings for evidence and
    for inclusion in the final report.
    """
    lines = []
    lines.append("NESSUS VULNERABILITY SCAN FINDINGS")
    lines.append("=" * 45)
    lines.append(f"Target IP: {target_ip}")
    lines.append("")

    # Count total findings across all severities
    total = sum(len(findings[level]) for level in findings)
    lines.append(f"Total findings: {total}")
    lines.append("")

    # List findings grouped by severity, most serious first
    for level in ["Critical", "High", "Medium", "Low", "Info"]:
        items = findings[level]
        if len(items) == 0:
            continue

        lines.append(f"\n{level.upper()} ({len(items)})")
        lines.append("-" * 45)
        for item in items:
            lines.append(
                f"  {item['name']}  "
                f"[{item['family']}]  x{item['count']}"
            )

    lines.append("")
    return "\n".join(lines)


def run_nessus_scan(config):
    """
    The main entry point for this module. It runs the entire Nessus
    workflow from start to finish using the user's configuration.

    Returns a dictionary with the organized findings and a text summary,
    or None if any critical step fails.
    """
    url = config["nessus_url"]
    headers = build_headers(
        config["nessus_access_key"],
        config["nessus_secret_key"]
    )
    target_ip = config["target_ip"]

    # Step 0: make sure Nessus is actually reachable first
    if not check_nessus_reachable(url, headers):
        return None

    # Step 1: find the scan template
    template_uuid = get_scan_template_uuid(url, headers)
    if template_uuid is None:
        return None

    # Step 2: create the scan
    scan_name = f"AutoVAS_{config['assessment_id']}"
    scan_id = create_scan(url, headers, template_uuid, target_ip, scan_name)
    if scan_id is None:
        return None

    # Step 3: launch it
    if not launch_scan(url, headers, scan_id):
        return None

    # Step 4: wait for it to finish
    if not wait_for_completion(url, headers, scan_id):
        return None

    # Step 5: pull and organize the results
    findings = get_findings(url, headers, scan_id)
    if findings is None:
        return None

    summary_text = format_findings_text(findings, target_ip)

    return {
        "findings": findings,
        "summary_text": summary_text,
        "scan_id": scan_id,
    }


# Allows testing this module on its own:
#   python modules/nessus.py
if __name__ == "__main__":
    # Build a minimal test config from manual input
    test_config = {
        "nessus_url": input("Nessus URL [https://localhost:8834]: ").strip()
                      or "https://localhost:8834",
        "nessus_access_key": input("Access Key: ").strip(),
        "nessus_secret_key": input("Secret Key: ").strip(),
        "target_ip": input("Target IP: ").strip(),
        "assessment_id": "test_run",
    }

    result = run_nessus_scan(test_config)
    if result:
        print("\n" + result["summary_text"])
    else:
        print("\nScan did not complete. See messages above.")