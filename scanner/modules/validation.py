"""
validation.py
-------------
Performs safe, automated validation of common vulnerabilities.

This module automates the same manual checks we ran during the assessment
to confirm that vulnerabilities flagged by Nessus are genuinely exploitable:
  - anonymous FTP login
  - SSH access with provided/default credentials
  - PostgreSQL access with default credentials
  - NFS export enumeration

IMPORTANT — these are VALIDATION checks, not exploits. They confirm whether
a weakness exists (e.g. "can we log in?") but do not modify, damage, or take
control of the target. This keeps the tool ethical and safe to run.

Several checks rely on command-line tools (ftp, showmount, psql) being
installed on the machine running this program.
"""

import socket
import subprocess
import ftplib       # Python's built-in FTP client library
import paramiko     # third-party SSH client library


# A short timeout (seconds) for network operations so checks don't hang
TIMEOUT = 10


def test_anonymous_ftp(target_ip):
    """
    Check whether the FTP service allows anonymous login.

    'Anonymous' login means connecting with the username 'anonymous' and
    no real password. If it succeeds, anyone can access the FTP service
    without credentials — the vsftpd finding from our assessment.

    Uses Python's built-in ftplib, so no external tool is needed.

    Returns a dictionary describing the result.
    """
    print("[*] Validating anonymous FTP access ...")

    result = {
        "check": "Anonymous FTP Access",
        "success": False,
        "detail": "",
    }

    try:
        ftp = ftplib.FTP()
        ftp.connect(target_ip, 21, timeout=TIMEOUT)

        # Try logging in anonymously (ftplib defaults to anonymous when
        # no username/password is given)
        ftp.login()

        # If we get here, login succeeded
        banner = ftp.getwelcome()
        result["success"] = True
        result["detail"] = (
            f"Anonymous login SUCCEEDED. Server banner: {banner}. "
            "An attacker can access the FTP service with no credentials."
        )
        ftp.quit()

    except ftplib.error_perm as e:
        # A permission error means anonymous login was refused (good)
        result["detail"] = f"Anonymous login refused: {e}"
    except (socket.timeout, ConnectionRefusedError):
        result["detail"] = "Could not connect to FTP (port 21 closed or filtered)."
    except Exception as e:
        result["detail"] = f"FTP check failed: {e}"

    return result


def test_ssh_login(target_ip, username, password):
    """
    Check whether SSH login succeeds with the provided credentials.

    In our assessment we proved that default credentials (msfadmin/msfadmin)
    worked. This automates that test using the paramiko SSH library.

    We deliberately allow the older key algorithms here because legacy
    targets like Metasploitable use them — the same reason we passed
    special flags to ssh manually.

    Returns a dictionary describing the result.
    """
    print("[*] Validating SSH access with provided credentials ...")

    result = {
        "check": "SSH Credential Access",
        "success": False,
        "detail": "",
    }

    try:
        client = paramiko.SSHClient()

        # Automatically accept the target's host key (fine in a lab; in
        # production you would verify it instead)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(
            hostname=target_ip,
            username=username,
            password=password,
            timeout=TIMEOUT,
            allow_agent=False,
            look_for_keys=False,
        )

        # If we reach here, the login worked
        result["success"] = True
        result["detail"] = (
            f"SSH login SUCCEEDED with username '{username}'. "
            "This confirms valid (possibly default/weak) credentials grant "
            "remote shell access to the system."
        )
        client.close()

    except paramiko.AuthenticationException:
        result["detail"] = (
            f"SSH login failed for '{username}' — credentials were rejected. "
            "The service is still exposed, but these credentials did not work."
        )
    except (socket.timeout, ConnectionRefusedError):
        result["detail"] = "Could not connect to SSH (port 22 closed or filtered)."
    except Exception as e:
        result["detail"] = f"SSH check failed: {e}"

    return result


def test_default_postgres(target_ip):
    """
    Check whether PostgreSQL accepts the default credentials.

    During the assessment, the credentials postgres/postgres granted full
    database access. This automates that test.

    We use the 'psql' command-line client via subprocess, passing the
    password through the PGPASSWORD environment variable (the same trick
    we used manually). psql must be installed on the machine running this.

    Returns a dictionary describing the result.
    """
    print("[*] Validating default PostgreSQL credentials ...")

    result = {
        "check": "Default PostgreSQL Credentials",
        "success": False,
        "detail": "",
    }

    # We run a harmless command (SELECT version();) just to prove access
    import os
    env = os.environ.copy()
    env["PGPASSWORD"] = "postgres"   # the default password we are testing

    command = [
        "psql",
        "-h", target_ip,
        "-U", "postgres",
        "-c", "SELECT version();",
    ]

    try:
        completed = subprocess.run(
            command,
            env=env,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )

        # A return code of 0 means the command ran successfully = we got in
        if completed.returncode == 0:
            result["success"] = True
            result["detail"] = (
                "Default credentials (postgres/postgres) SUCCEEDED. "
                "Full database access was granted. "
                f"Server response: {completed.stdout.strip().splitlines()[0]}"
            )
        else:
            result["detail"] = (
                "Default credentials were refused or connection failed. "
                f"Error: {completed.stderr.strip()}"
            )

    except FileNotFoundError:
        result["detail"] = (
            "The 'psql' client is not installed on this machine, so this "
            "check could not run. Install it with: sudo apt install postgresql-client"
        )
    except subprocess.TimeoutExpired:
        result["detail"] = "PostgreSQL connection timed out."
    except Exception as e:
        result["detail"] = f"PostgreSQL check failed: {e}"

    return result


def check_nfs_exports(target_ip):
    """
    List what the NFS service is exporting to the network.

    In our assessment, 'showmount -e' revealed the entire root filesystem
    (/ *) was exported to everyone — a critical misconfiguration. This
    automates that check.

    Uses the 'showmount' command via subprocess. showmount must be installed
    (it comes with the nfs-common package).

    Returns a dictionary describing the result.
    """
    print("[*] Checking NFS exports ...")

    result = {
        "check": "NFS Export Enumeration",
        "success": False,
        "detail": "",
    }

    command = ["showmount", "-e", target_ip]

    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )

        if completed.returncode == 0:
            output = completed.stdout.strip()

            # If the output mentions "/" being exported to "*", that's the
            # worst-case scenario we want to flag clearly.
            if "/" in output and "*" in output:
                result["success"] = True
                result["detail"] = (
                    "NFS is exporting sensitive paths to all hosts. "
                    f"Export list:\n{output}\n"
                    "This allows any network host to mount and read the "
                    "exported filesystem."
                )
            else:
                result["detail"] = f"NFS exports found:\n{output}"
        else:
            result["detail"] = (
                "No NFS exports found or NFS not running. "
                f"{completed.stderr.strip()}"
            )

    except FileNotFoundError:
        result["detail"] = (
            "The 'showmount' tool is not installed on this machine. "
            "Install it with: sudo apt install nfs-common"
        )
    except subprocess.TimeoutExpired:
        result["detail"] = "NFS check timed out."
    except Exception as e:
        result["detail"] = f"NFS check failed: {e}"

    return result


def format_validation_text(results, target_ip):
    """
    Build a readable text summary of all validation results for evidence
    and for the final report.
    """
    lines = []
    lines.append("MANUAL VALIDATION RESULTS")
    lines.append("=" * 45)
    lines.append(f"Target IP: {target_ip}")
    lines.append("")

    for r in results:
        # A simple visual marker for each result
        status = "CONFIRMED" if r["success"] else "Not confirmed"
        lines.append(f"[{status}] {r['check']}")
        lines.append(f"    {r['detail']}")
        lines.append("")

    return "\n".join(lines)


def run_validation(config):
    """
    The main entry point for this module. Runs all four validation checks
    against the target and returns the collected results.

    Returns a dictionary with the list of results and a text summary.
    """
    target_ip = config["target_ip"]

    print("\n[*] Running manual validation checks ...")

    # Run each check in turn, collecting the results
    results = [
        test_anonymous_ftp(target_ip),
        test_ssh_login(
            target_ip,
            config["ssh_username"],
            config["ssh_password"]
        ),
        test_default_postgres(target_ip),
        check_nfs_exports(target_ip),
    ]

    summary_text = format_validation_text(results, target_ip)

    return {
        "results": results,
        "summary_text": summary_text,
    }


# Allows testing this module on its own:
#   python modules/validation.py
if __name__ == "__main__":
    test_config = {
        "target_ip": input("Target IP: ").strip(),
        "ssh_username": input("SSH username: ").strip(),
        "ssh_password": input("SSH password: ").strip(),
    }

    result = run_validation(test_config)
    print("\n" + result["summary_text"])