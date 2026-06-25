"""
logging_review.py
-----------------
Reviews the target's logging and firewall configuration over SSH.

This automates Task 6 from the manual assessment: connecting to the target,
reading its authentication log for failed login attempts, and checking its
firewall (iptables) rules. These reveal whether the system can detect and
resist attacks.

It uses paramiko to run commands over SSH, just as we did manually after
logging in.
"""

import socket
import paramiko


TIMEOUT = 15


def run_remote_command(client, command):
    """
    Run a single command on the target over an existing SSH connection and
    return its text output.

    'client' is an already-connected paramiko SSHClient.
    """
    stdin, stdout, stderr = client.exec_command(command, timeout=TIMEOUT)
    output = stdout.read().decode("utf-8", errors="ignore")
    error = stderr.read().decode("utf-8", errors="ignore")

    # Some commands (like sudo iptables) may need the password or print to
    # stderr; we combine both streams so nothing is lost.
    return output + error


def review_system(config):
    """
    Connect to the target over SSH and gather logging and firewall info.

    Returns a dictionary with the findings and a text summary. If the SSH
    connection fails, it returns a result explaining why rather than crashing.
    """
    target_ip = config["target_ip"]
    username = config["ssh_username"]
    password = config["ssh_password"]

    print("\n[*] Reviewing logging and firewall configuration over SSH ...")

    result = {
        "connected": False,
        "auth_log": "",
        "firewall": "",
        "summary_text": "",
    }

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=target_ip,
            username=username,
            password=password,
            timeout=TIMEOUT,
            allow_agent=False,
            look_for_keys=False,
        )
        result["connected"] = True
        print("[+] Connected over SSH.")

    except paramiko.AuthenticationException:
        result["summary_text"] = (
            "Could not review logging/firewall: SSH credentials were rejected."
        )
        print("[!] SSH authentication failed — skipping logging review.")
        return result
    except (socket.timeout, ConnectionRefusedError):
        result["summary_text"] = (
            "Could not review logging/firewall: SSH connection failed."
        )
        print("[!] SSH connection failed — skipping logging review.")
        return result
    except Exception as e:
        result["summary_text"] = f"Could not review logging/firewall: {e}"
        return result

    # --- Read failed login attempts from the authentication log ---
    print("[*] Reading authentication log ...")
    auth_log = run_remote_command(
        client,
        "cat /var/log/auth.log | grep 'Failed password'"
    )
    result["auth_log"] = auth_log.strip()

    # --- Read the firewall rules ---
    print("[*] Reading firewall (iptables) rules ...")
    # We try with sudo; on Metasploitable the msfadmin user can sudo.
    # The '-S' flag lists rules in a simple format.
    firewall = run_remote_command(
        client,
        f"echo {password} | sudo -S iptables -L 2>/dev/null"
    )
    result["firewall"] = firewall.strip()

    client.close()

    # --- Build a readable summary ---
    result["summary_text"] = format_review_text(result, target_ip)
    print("[+] Logging and firewall review complete.")

    return result


def format_review_text(result, target_ip):
    """
    Build a readable text summary of the logging and firewall review.
    """
    lines = []
    lines.append("LOGGING AND FIREWALL REVIEW")
    lines.append("=" * 45)
    lines.append(f"Target IP: {target_ip}")
    lines.append("")

    # --- Authentication log section ---
    lines.append("Authentication Log — Failed Login Attempts")
    lines.append("-" * 45)
    if result["auth_log"]:
        lines.append(result["auth_log"])
        # Count how many failed attempts were captured
        count = len(result["auth_log"].splitlines())
        lines.append("")
        lines.append(f"Total failed login attempts recorded: {count}")
        lines.append(
            "Logging exists, but note whether any alerting or lockout is "
            "in place (none was observed in the lab environment)."
        )
    else:
        lines.append("No failed login attempts were found in the log.")

    lines.append("")

    # --- Firewall section ---
    lines.append("Firewall Rules (iptables)")
    lines.append("-" * 45)
    if result["firewall"]:
        lines.append(result["firewall"])
        # Detect the worst-case "empty firewall" scenario
        if "policy ACCEPT" in result["firewall"] and \
           result["firewall"].count("\n") < 12:
            lines.append("")
            lines.append(
                "OBSERVATION: The firewall appears to have no real rules — "
                "all chains default to ACCEPT. This means no network-level "
                "filtering is protecting the exposed services."
            )
    else:
        lines.append("Could not read firewall rules (or none are set).")

    lines.append("")
    return "\n".join(lines)


# Allows testing this module on its own:
#   python modules/logging_review.py
if __name__ == "__main__":
    test_config = {
        "target_ip": input("Target IP: ").strip(),
        "ssh_username": input("SSH username: ").strip(),
        "ssh_password": input("SSH password: ").strip(),
    }
    result = review_system(test_config)
    print("\n" + result["summary_text"])