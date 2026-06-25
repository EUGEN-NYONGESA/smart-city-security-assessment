"""
evidence.py
-----------
Saves all findings as plain-text evidence files.

Good security work is reproducible and provable. This module writes every
stage's findings to timestamped .txt files inside a dedicated folder for
each assessment, so there is a clear paper trail of exactly what was found.

These evidence files serve two purposes:
  1. Proof that each check was actually performed
  2. Raw material that feeds into the final report
"""

import os
from datetime import datetime


def create_evidence_folder(base_dir, assessment_id):
    """
    Create a dedicated folder for this assessment's evidence files.

    The folder is named using the assessment ID (which includes the target
    IP and a timestamp), so every run gets its own clearly labeled folder.

    Returns the full path to the created folder.
    """
    # Build the folder path, e.g. evidence/192.168.56.103_20260620_143000/
    folder_path = os.path.join(base_dir, assessment_id)

    # Create it (and any parent folders). exist_ok avoids an error if it
    # somehow already exists.
    os.makedirs(folder_path, exist_ok=True)

    print(f"\n[+] Evidence will be saved in: {folder_path}")
    return folder_path


def save_evidence(folder_path, filename, content):
    """
    Write a single piece of evidence to a .txt file.

    'filename' should be a short descriptive name without an extension,
    e.g. "01_nmap_recon". We add the .txt extension automatically.

    A header with a timestamp is added to the top of every file so each
    piece of evidence is self-dating.
    """
    # Ensure the filename ends in .txt
    if not filename.endswith(".txt"):
        filename = filename + ".txt"

    full_path = os.path.join(folder_path, filename)

    # Build a small header recording when this evidence was saved
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = (
        f"Evidence file: {filename}\n"
        f"Generated: {timestamp}\n"
        f"{'=' * 45}\n\n"
    )

    # Write the header plus the actual content
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(header + content)

    print(f"    [saved] {filename}")
    return full_path


def save_all_evidence(folder_path, recon_data, nessus_data,
                      validation_data, logging_data):
    """
    Save the findings from every stage as separate, numbered evidence files.

    Numbering the files keeps them in logical order when viewed in a folder.
    Each stage's data may be None if that stage failed, so we check before
    saving and record a placeholder if needed.

    Returns a list of the file paths that were created.
    """
    print("\n[*] Saving all evidence files ...")
    saved_files = []

    # 1. Nmap reconnaissance
    if recon_data:
        path = save_evidence(folder_path, "01_nmap_recon",
                             recon_data["summary_text"])
        saved_files.append(path)

    # 2. Nessus scan findings
    if nessus_data:
        path = save_evidence(folder_path, "02_nessus_findings",
                             nessus_data["summary_text"])
        saved_files.append(path)
    else:
        path = save_evidence(folder_path, "02_nessus_findings",
                             "The Nessus scan did not complete. See run logs.")
        saved_files.append(path)

    # 3. Manual validation results
    if validation_data:
        path = save_evidence(folder_path, "03_manual_validation",
                             validation_data["summary_text"])
        saved_files.append(path)

    # 4. Logging and firewall review
    if logging_data:
        path = save_evidence(folder_path, "04_logging_firewall",
                             logging_data["summary_text"])
        saved_files.append(path)

    print(f"[+] Saved {len(saved_files)} evidence files.")
    return saved_files


# Allows testing this module on its own:
#   python modules/evidence.py
if __name__ == "__main__":
    print("Testing evidence module ...")

    # Create a test folder and save a sample file
    folder = create_evidence_folder("evidence", "test_192.168.1.1_demo")
    save_evidence(folder, "00_test", "This is a sample evidence file.\n")
    print("\nDone. Check the evidence/ folder.")