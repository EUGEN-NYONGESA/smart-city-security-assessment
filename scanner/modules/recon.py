"""
recon.py
--------
Handles network reconnaissance using Nmap.

This module performs the same job as the manual Nmap scan in the
assessment walkthrough: it discovers open ports, identifies the services
and versions running on them, and sorts those services into risk
categories so the analyst immediately sees what matters most.

It uses the 'python-nmap' library, which is a Python wrapper around the
real nmap tool. Nmap itself must be installed on the system.
"""

import nmap   # python-nmap library — wraps the real nmap command


# ---------------------------------------------------------------------------
# KNOWLEDGE BASE
# ---------------------------------------------------------------------------
# This dictionary maps known services/ports to a risk category and a short
# explanation. It encodes the same expert knowledge we applied by hand when
# categorizing assets in the manual assessment.
#
# When the scan finds one of these ports, we can automatically explain why
# it matters. Anything not listed here is given a sensible default.
# ---------------------------------------------------------------------------
RISK_KNOWLEDGE = {
    21:   ("Critical", "FTP — often vsftpd, known for the CVE-2011-2523 backdoor"),
    1524: ("Critical", "Bind shell — an open root shell requiring no authentication"),
    3306: ("Critical", "MySQL — frequently weak or default authentication"),
    139:  ("Critical", "Samba — vulnerable to RCE via CVE-2007-2447"),
    445:  ("Critical", "Samba — vulnerable to RCE via CVE-2007-2447"),
    5432: ("Critical", "PostgreSQL — frequently uses default credentials"),
    5900: ("Critical", "VNC — often protected only by a default password"),
    22:   ("High",     "SSH — remote access; risky if outdated or root login enabled"),
    80:   ("High",     "HTTP — web server; risky if outdated (e.g. Apache 2.2.x)"),
    8180: ("High",     "HTTP — Apache Tomcat; often an outdated engine"),
    6667: ("High",     "IRC — UnrealIRCd has a known backdoor"),
    2049: ("High",     "NFS — often misconfigured to export sensitive paths"),
    23:   ("Medium",   "Telnet — transmits credentials in plaintext"),
    512:  ("Medium",   "rexec — legacy remote execution, unencrypted"),
    513:  ("Medium",   "rlogin — legacy remote login, unencrypted"),
    514:  ("Medium",   "rsh — legacy remote shell, unencrypted"),
    2121: ("Medium",   "ProFTPD — secondary FTP, possible misconfiguration"),
    25:   ("Low",      "SMTP — mail service, lower direct risk"),
    53:   ("Low",      "DNS — name resolution; outdated BIND has known issues"),
    111:  ("Low",      "RPC — auxiliary service supporting NFS"),
    1099: ("Low",      "Java RMI — possible deserialization risk"),
    6000: ("Low",      "X11 — GUI exposure, usually access-denied"),
    8009: ("Low",      "AJP — Apache Jserv backend connector"),
}

# A default used when a discovered port is not in our knowledge base
DEFAULT_RISK = ("Low", "Service not in knowledge base — review manually")


def run_nmap(target_ip):
    """
    Run an Nmap scan against the target.

    The scan uses:
      -sV  to detect service versions
      -O   to detect the operating system

    Note: OS detection (-O) requires root/administrator privileges, so this
    program is expected to be run with sufficient permissions (e.g. sudo).

    Returns the python-nmap scanner object, which holds all the results.
    """
    print(f"\n[*] Starting Nmap scan against {target_ip} ...")
    print("    (This may take 30-60 seconds)")

    scanner = nmap.PortScanner()

    # The arguments string mirrors the manual command: nmap -sV -O <ip>
    scanner.scan(hosts=target_ip, arguments="-sV -O")

    print("[+] Nmap scan complete.")
    return scanner


def parse_services(scanner, target_ip):
    """
    Pull the useful information out of the raw Nmap results.

    For each open TCP port, we collect:
      - the port number
      - the service name (e.g. "ftp")
      - the product and version (e.g. "vsftpd 2.3.4")

    Returns a list of dictionaries, one per open port.
    """
    services = []

    # If the host didn't respond at all, return an empty list
    if target_ip not in scanner.all_hosts():
        print("[!] The target did not respond to the scan.")
        return services

    host_data = scanner[target_ip]

    # Make sure the host actually has TCP results
    if "tcp" not in host_data.all_protocols():
        print("[!] No open TCP ports were found.")
        return services

    # Go through every TCP port that was found
    for port in sorted(host_data["tcp"].keys()):
        port_info = host_data["tcp"][port]

        # Only care about ports that are actually open
        if port_info["state"] != "open":
            continue

        # Build a readable version string from product + version fields
        product = port_info.get("product", "").strip()
        version = port_info.get("version", "").strip()
        full_version = f"{product} {version}".strip()
        if full_version == "":
            full_version = "unknown"

        services.append({
            "port": port,
            "service": port_info.get("name", "unknown"),
            "version": full_version,
        })

    print(f"[+] Found {len(services)} open ports.")
    return services


def categorize_assets(services):
    """
    Sort the discovered services into risk categories using our knowledge
    base. This is the automated version of the manual asset-categorization
    table we built during the assessment.

    Returns a dictionary grouping services under each risk level.
    """
    # Start with empty lists for each category
    categorized = {
        "Critical": [],
        "High": [],
        "Medium": [],
        "Low": [],
    }

    for service in services:
        port = service["port"]

        # Look up the risk for this port, or use the default
        risk_level, reason = RISK_KNOWLEDGE.get(port, DEFAULT_RISK)

        # Attach the reason to the service record
        service_with_reason = service.copy()
        service_with_reason["reason"] = reason

        # Place it in the right category
        categorized[risk_level].append(service_with_reason)

    return categorized


def get_os_guess(scanner, target_ip):
    """
    Try to extract Nmap's best guess at the operating system.

    Returns a short description, or a fallback message if OS detection
    didn't produce a result.
    """
    if target_ip not in scanner.all_hosts():
        return "Unknown (host did not respond)"

    host_data = scanner[target_ip]

    # Nmap stores OS matches in an "osmatch" list when -O succeeds
    if "osmatch" in host_data and len(host_data["osmatch"]) > 0:
        return host_data["osmatch"][0]["name"]

    return "Unknown (OS detection inconclusive)"


def format_findings_text(services, categorized, os_guess, target_ip):
    """
    Build a clean, human-readable text summary of the reconnaissance.

    This text is what gets saved as an evidence file later, and is also
    fed into the final report. We keep it plain and readable.
    """
    lines = []
    lines.append("NMAP RECONNAISSANCE FINDINGS")
    lines.append("=" * 45)
    lines.append(f"Target IP        : {target_ip}")
    lines.append(f"Operating System : {os_guess}")
    lines.append(f"Open Ports Found : {len(services)}")
    lines.append("")

    # List each category in order of importance
    for level in ["Critical", "High", "Medium", "Low"]:
        items = categorized[level]
        if len(items) == 0:
            continue

        lines.append(f"\n{level.upper()} RISK ASSETS")
        lines.append("-" * 45)
        for item in items:
            lines.append(
                f"  Port {item['port']:<6} {item['service']:<12} "
                f"{item['version']}"
            )
            lines.append(f"      Reason: {item['reason']}")

    lines.append("")
    return "\n".join(lines)


def perform_reconnaissance(target_ip):
    """
    The main entry point for this module. It runs the whole recon process
    and returns a structured result the rest of the program can use.

    Returns a dictionary containing:
      - the raw service list
      - the categorized assets
      - the OS guess
      - a ready-to-save text summary
    """
    scanner = run_nmap(target_ip)
    services = parse_services(scanner, target_ip)
    categorized = categorize_assets(services)
    os_guess = get_os_guess(scanner, target_ip)
    summary_text = format_findings_text(services, categorized, os_guess, target_ip)

    return {
        "services": services,
        "categorized": categorized,
        "os_guess": os_guess,
        "summary_text": summary_text,
    }


# Allows testing this module on its own:
#   sudo python modules/recon.py
# (sudo is needed for OS detection)
if __name__ == "__main__":
    test_ip = input("Enter an IP to test recon against: ").strip()
    result = perform_reconnaissance(test_ip)
    print("\n" + result["summary_text"])