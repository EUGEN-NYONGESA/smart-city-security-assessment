"""
inputs.py
---------
Handles collecting and validating all user inputs needed to run an
assessment. This is the first thing the program does.

The goal is to make the program interactive and friendly: it asks the
user clear questions, validates their answers, and hides sensitive input
like passwords from the screen.
"""

import re               # for validating the IP address pattern
import getpass          # for hiding password input on screen
from datetime import datetime


def validate_ip(ip):
    """
    Check whether a string is a valid IPv4 address.

    An IPv4 address has four numbers separated by dots (e.g. 192.168.56.103),
    and each number must be between 0 and 255.

    Returns True if valid, False otherwise.
    """
    # This pattern matches four groups of 1-3 digits separated by dots
    pattern = r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"
    match = re.match(pattern, ip)

    # If the overall shape is wrong, it's not valid
    if not match:
        return False

    # Check each of the four numbers is in the valid range (0-255)
    for group in match.groups():
        if int(group) < 0 or int(group) > 255:
            return False

    return True


def ask_for_ip():
    """
    Ask the user for the target IP address and keep asking until they
    provide a valid one.
    """
    while True:
        ip = input("Enter the target IP address (e.g. 192.168.56.103): ").strip()

        if validate_ip(ip):
            return ip
        else:
            print("  [!] That doesn't look like a valid IP address. Please try again.\n")


def ask_for_credentials():
    """
    Ask the user for the SSH username and password of the target system.
    The password is hidden as the user types it, for security.
    """
    print("\n--- SSH Credentials (used for logging and firewall review) ---")
    username = input("Enter the SSH username: ").strip()

    # getpass hides the password as it is typed
    password = getpass.getpass("Enter the SSH password (input hidden): ")

    return username, password


def ask_for_nessus_details():
    """
    Ask the user for their Nessus API keys and server URL.

    Nessus uses two keys for API access: an Access Key and a Secret Key.
    These are generated inside the Nessus web interface under
    Settings > My Account > API Keys.
    """
    print("\n--- Nessus API Details ---")
    print("(Generate these in Nessus under Settings > My Account > API Keys)")

    access_key = input("Enter your Nessus Access Key: ").strip()
    secret_key = getpass.getpass("Enter your Nessus Secret Key (input hidden): ").strip()

    # Offer a sensible default so the user can just press Enter
    url = input("Enter the Nessus URL [default: https://localhost:8834]: ").strip()
    if url == "":
        url = "https://localhost:8834"

    return access_key, secret_key, url


def confirm_inputs(config):
    """
    Show the user a summary of everything they entered (except passwords)
    and ask them to confirm before the assessment begins.

    Returns True if the user confirms, False if they want to start over.
    """
    print("\n" + "=" * 55)
    print("  Please confirm the assessment details:")
    print("=" * 55)
    print(f"  Target IP        : {config['target_ip']}")
    print(f"  SSH Username     : {config['ssh_username']}")
    print(f"  SSH Password     : {'*' * 8} (hidden)")
    print(f"  Nessus URL       : {config['nessus_url']}")
    print(f"  Nessus Keys      : {'*' * 8} (hidden)")
    print("=" * 55)

    answer = input("\nProceed with these settings? (yes/no): ").strip().lower()
    return answer in ("yes", "y")


def collect_inputs():
    """
    The main function of this module. It runs the full input-collection
    process and returns everything bundled into a single dictionary that
    the rest of the program can use.

    The dictionary also includes a unique 'assessment_id' based on the
    target and the current time, used to name evidence folders.
    """
    print("\nLet's set up the assessment.\n")

    # Collect each piece of information
    target_ip = ask_for_ip()
    ssh_username, ssh_password = ask_for_credentials()
    access_key, secret_key, nessus_url = ask_for_nessus_details()

    # Build a unique ID for this run, e.g. "192.168.56.103_20260620_143000"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    assessment_id = f"{target_ip}_{timestamp}"

    # Bundle everything into one dictionary
    config = {
        "target_ip": target_ip,
        "ssh_username": ssh_username,
        "ssh_password": ssh_password,
        "nessus_access_key": access_key,
        "nessus_secret_key": secret_key,
        "nessus_url": nessus_url,
        "assessment_id": assessment_id,
    }

    # Let the user confirm before continuing
    if not confirm_inputs(config):
        print("\nRestarting input collection...\n")
        return collect_inputs()   # start over if they say no

    return config


# This block lets us test this module on its own by running:
#   python modules/inputs.py
# It will only run when the file is executed directly, not when imported.
if __name__ == "__main__":
    print("Testing the input module...")
    result = collect_inputs()
    print("\nCollected configuration (passwords hidden):")
    for key, value in result.items():
        if "password" in key or "key" in key:
            print(f"  {key}: {'*' * 8}")
        else:
            print(f"  {key}: {value}")