"""
main.py
-------
The main orchestrator for AutoVAS (Automated Vulnerability Assessment Scanner).

This is the file you run to start an assessment:

    sudo python main.py

It ties together all the modules in the correct order, mirroring the exact
workflow of the manual assessment:

    1. Collect user inputs
    2. Create an evidence folder
    3. Run Nmap reconnaissance
    4. Run the Nessus scan
    5. Run manual validation checks
    6. Review logging and firewall
    7. Save all evidence
    8. Generate the final reports

Each step's output is passed along to the next. The program is designed to
keep going wherever it safely can, so that a failure in one stage (for
example, Nessus being unreachable) still produces as much evidence and
reporting as possible.
"""

import sys

# Import each module we built in the previous phases
from modules import inputs
from modules import recon
from modules import nessus
from modules import validation
from modules import logging_review
from modules import evidence
from modules import report


# Folders where output is written (relative to the scanner/ directory)
EVIDENCE_BASE_DIR = "evidence"
REPORTS_DIR = "reports"


def print_banner():
    """
    Print a welcome banner and the ethical-use disclaimer.

    Showing the disclaimer every run reinforces that this tool is for
    authorized testing only.
    """
    banner = r"""
    =====================================================
      AutoVAS — Automated Vulnerability Assessment Scanner
    =====================================================
      Automates: recon -> scan -> validate -> report
    -----------------------------------------------------
      FOR AUTHORIZED SECURITY TESTING ONLY.
      Only run this against systems you own or have
      explicit written permission to test.
    =====================================================
    """
    print(banner)


def print_step(number, title):
    """
    Print a clear, consistent header for each major step so the user can
    follow the program's progress.
    """
    print("\n" + "#" * 55)
    print(f"#  STEP {number}: {title}")
    print("#" * 55)


def main():
    """
    Run the complete assessment workflow from start to finish.
    """
    print_banner()

    # -----------------------------------------------------------------
    # STEP 1: Collect and confirm user inputs
    # -----------------------------------------------------------------
    print_step(1, "Collecting Inputs")
    try:
        config = inputs.collect_inputs()
    except KeyboardInterrupt:
        # Allow the user to cancel cleanly with Ctrl+C
        print("\n\nCancelled by user. Exiting.")
        sys.exit(0)

    # -----------------------------------------------------------------
    # STEP 2: Create a dedicated evidence folder for this run
    # -----------------------------------------------------------------
    print_step(2, "Preparing Evidence Folder")
    evidence_folder = evidence.create_evidence_folder(
        EVIDENCE_BASE_DIR, config["assessment_id"]
    )

    # -----------------------------------------------------------------
    # STEP 3: Reconnaissance (Nmap)
    # -----------------------------------------------------------------
    print_step(3, "Reconnaissance (Nmap)")
    try:
        recon_data = recon.perform_reconnaissance(config["target_ip"])
    except Exception as e:
        # If recon fails entirely, we note it and continue with no data
        print(f"[!] Reconnaissance failed: {e}")
        recon_data = None

    # -----------------------------------------------------------------
    # STEP 4: Vulnerability scan (Nessus)
    # -----------------------------------------------------------------
    print_step(4, "Vulnerability Scan (Nessus)")
    try:
        nessus_data = nessus.run_nessus_scan(config)
    except Exception as e:
        print(f"[!] Nessus scan failed: {e}")
        nessus_data = None

    if nessus_data is None:
        # This is a major step, so we warn clearly but keep going — the
        # recon and validation evidence is still valuable on its own.
        print("[!] Continuing without Nessus results.")

    # -----------------------------------------------------------------
    # STEP 5: Manual validation checks
    # -----------------------------------------------------------------
    print_step(5, "Manual Validation")
    try:
        validation_data = validation.run_validation(config)
    except Exception as e:
        print(f"[!] Validation checks failed: {e}")
        validation_data = None

    # -----------------------------------------------------------------
    # STEP 6: Logging and firewall review (over SSH)
    # -----------------------------------------------------------------
    print_step(6, "Logging & Firewall Review")
    try:
        logging_data = logging_review.review_system(config)
    except Exception as e:
        print(f"[!] Logging review failed: {e}")
        logging_data = None

    # -----------------------------------------------------------------
    # STEP 7: Save all gathered evidence to .txt files
    # -----------------------------------------------------------------
    print_step(7, "Saving Evidence")
    evidence.save_all_evidence(
        evidence_folder,
        recon_data,
        nessus_data,
        validation_data,
        logging_data
    )

    # -----------------------------------------------------------------
    # STEP 8: Generate the final reports (.txt and .docx)
    # -----------------------------------------------------------------
    print_step(8, "Generating Reports")
    try:
        txt_path, docx_path = report.generate_reports(
            config,
            recon_data,
            nessus_data,
            validation_data,
            logging_data,
            REPORTS_DIR
        )
    except Exception as e:
        print(f"[!] Report generation failed: {e}")
        txt_path, docx_path = None, None

    # -----------------------------------------------------------------
    # DONE: Summarize where everything was saved
    # -----------------------------------------------------------------
    print("\n" + "=" * 55)
    print("  ASSESSMENT COMPLETE")
    print("=" * 55)
    print(f"  Target        : {config['target_ip']}")
    print(f"  Evidence saved: {evidence_folder}/")
    if txt_path:
        print(f"  Text report   : {txt_path}")
    if docx_path:
        print(f"  Word report   : {docx_path}")
    print("=" * 55)
    print("\nReview the evidence files and report for full details.\n")


# This is the standard Python entry point. The code inside only runs when
# the file is executed directly (python main.py), not when imported.
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting.")
        sys.exit(0)