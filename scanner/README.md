# 🛡️ AutoVAS — Automated Vulnerability Assessment Scanner

A Python program that automates the complete vulnerability assessment
workflow demonstrated in this repository — from reconnaissance to final
report generation — for a target system.

The user simply provides a few inputs (target IP, credentials), and the
program performs the entire assessment in the background, producing
evidence files and a professional report.

---

## 🎯 The Problem

Performing a vulnerability assessment manually involves many repetitive
steps:

1. Running an Nmap scan and interpreting the output
2. Configuring and launching a Nessus scan through the web interface
3. Waiting for the scan and manually reviewing 70+ findings
4. Running manual validation commands one by one (FTP, SSH, etc.)
5. Documenting every finding and result by hand
6. Writing a formal report from scratch

This process is **time-consuming, error-prone, and hard to reproduce
consistently** across different targets. An analyst auditing multiple
systems repeats the same steps over and over.

---

## 💡 The Solution

**AutoVAS** automates this entire workflow. The analyst provides:

- Target IP address
- SSH username and password (for logging/firewall review)
- Nessus API credentials

The program then automatically:

1. ✅ Runs an Nmap scan and categorizes discovered assets
2. ✅ Launches a Nessus scan via the API and waits for completion
3. ✅ Pulls and organizes all vulnerability findings
4. ✅ Runs manual validation checks against common vulnerabilities
5. ✅ Reviews logging and firewall configuration over SSH
6. ✅ Saves all raw findings as evidence (.txt files)
7. ✅ Generates a professional vulnerability report (.txt and .docx)

---

## 🧱 How It Works (High Level)

┌──────────────────┐
                │   User Inputs    │
                │  IP, creds, keys │
                └────────┬─────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
 ┌──────────┐     ┌──────────┐     ┌──────────┐
 │   Nmap   │     │  Nessus  │     │  Manual  │
 │   Recon  │     │   API    │     │Validation│
 └────┬─────┘     └────┬─────┘     └────┬─────┘
      │                │                │
      └────────────────┼────────────────┘
                       ▼
              ┌──────────────────┐
              │ Evidence Storage │
              │   (.txt files)   │
              └────────┬─────────┘
                       ▼
              ┌──────────────────┐
              │ Report Generator │
              │  (.txt + .docx)  │
              └──────────────────┘

---

## 📁 Project Structure

scanner/

│

├── README.md                  # This file

├── requirements.txt           # Python dependencies

├── main.py                    # Orchestrator — runs the full pipeline

│

├── modules/                   # Core functionality

│   ├── init.py

│   ├── inputs.py              # Collects and validates user input

│   ├── recon.py              # Nmap scanning and asset categorization

│   ├── nessus.py             # Nessus API integration

│   ├── validation.py         # Manual vulnerability validation

│   ├── logging_review.py     # SSH-based logging/firewall review

│   ├── evidence.py           # Saves findings as .txt evidence

│   └── report.py             # Generates the final report

│

├── evidence/                  # Output — raw findings as proof

│

├── reports/                   # Output — generated reports

│

└── docs/                      # Additional documentation

├── SETUP.md              # Installation and setup guide

├── USAGE.md              # How to run the program

└── ARCHITECTURE.md       # Technical design explanation

---

## ⚠️ Disclaimer

This tool is for **authorized security testing only**. Never run it
against systems you do not own or have explicit written permission to
test. It was built for educational purposes as part of a controlled
lab environment.

---

## 📌 Build Progress

This project is being built phase by phase. See commit history for the
step-by-step development process.

- [x] Phase 1 — Problem definition & project structure
- [x] Phase 2 — Pseudocode
- [x] Phase 3 — Input handling
- [ ] Phase 4 — Nmap reconnaissance
- [ ] Phase 5 — Nessus API integration
- [ ] Phase 6 — Manual validation
- [ ] Phase 7 — Evidence generation
- [ ] Phase 8 — Report generation
- [ ] Phase 9 — Main orchestrator
- [ ] Phase 10 — Final documentation

