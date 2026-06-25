# Usage Guide

How to run AutoVAS once everything is set up.

> Before running, complete everything in [SETUP.md](SETUP.md) — Python
> dependencies, Nmap, Nessus, and your Nessus API keys.

---

## Running the Program

From inside the `scanner/` folder, run:

```bash
sudo python main.py
```

> **Why sudo?** Nmap's OS detection (`-O`) and some validation checks need
> elevated privileges. Running with sudo ensures every stage works.

---

## What the Program Will Ask You

The program is interactive. It will prompt you for:

| Prompt | What to enter |
|---|---|
| Target IP address | The IP of the system to assess (e.g. 192.168.56.103) |
| SSH username | A valid username on the target (for logging review) |
| SSH password | That user's password (input is hidden) |
| Nessus Access Key | From Nessus > My Account > API Keys |
| Nessus Secret Key | From Nessus > My Account > API Keys (hidden) |
| Nessus URL | Press Enter for the default (https://localhost:8834) |

After you enter everything, the program shows a summary and asks you to
confirm before it begins.

---

## What Happens Next

The program runs through eight steps automatically, printing its progress:

STEP 1: Collecting Inputs

STEP 2: Preparing Evidence Folder

STEP 3: Reconnaissance (Nmap)

STEP 4: Vulnerability Scan (Nessus)      <- takes 15-20 minutes

STEP 5: Manual Validation

STEP 6: Logging & Firewall Review

STEP 7: Saving Evidence

STEP 8: Generating Reports

The Nessus scan is the longest stage. The program polls it every 30
seconds and prints a live progress line, so you know it is still working.

You can safely leave it running and come back when it's done.

---

## Where to Find the Results

When the program finishes, it tells you exactly where everything was saved:

evidence/<target-ip>_<timestamp>/

01_nmap_recon.txt

02_nessus_findings.txt

03_manual_validation.txt

04_logging_firewall.txt
reports/

report_<target-ip><timestamp>.txt

report<target-ip>_<timestamp>.docx

- The **evidence files** are your raw proof — exactly what each check found.
- The **reports** are the polished deliverable, in both text and Word format.

---

## Stopping the Program

You can cancel at any time by pressing **Ctrl+C**. The program exits
cleanly without leaving anything in a broken state.

---

## Common Issues

| Problem | Likely cause and fix |
|---|---|
| "Could not connect to Nessus" | Nessus isn't running. Start it: `sudo systemctl start nessusd` |
| "Nessus rejected the API keys" | Wrong keys. Regenerate them in Nessus > My Account > API Keys |
| "psql is not installed" | Install it: `sudo apt install postgresql-client` |
| "showmount is not installed" | Install it: `sudo apt install nfs-common` |
| OS shows as "Unknown" | You probably didn't run with `sudo` |
| SSH review skipped | SSH credentials were wrong, or SSH is closed on the target |

---

## A Note on Scope

This program validates vulnerabilities; it does not exploit them. It will
tell you whether a weakness exists (for example, whether default
credentials work), but it never modifies or takes control of the target.
Always ensure you have permission before assessing any system.