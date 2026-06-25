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

This project was built phase by phase. The commit history shows the
step-by-step development process, making it a useful reference for anyone
learning how a tool like this comes together.

- [x] Phase 1 — Problem definition & project structure
- [x] Phase 2 — Pseudocode
- [x] Phase 3 — Input handling
- [x] Phase 4 — Nmap reconnaissance
- [x] Phase 5 — Nessus API integration
- [x] Phase 6 — Manual validation
- [x] Phase 7 — Evidence generation
- [x] Phase 8 — Report generation
- [x] Phase 9 — Main orchestrator
- [x] Phase 10 — Final documentation

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Make sure Nessus is running and you have API keys
#    (see docs/SETUP.md)

# 3. Run the assessment
sudo python main.py
```

See [docs/USAGE.md](docs/USAGE.md) for the full guide.

---

## 📚 Documentation

- [docs/PROBLEM.md](docs/PROBLEM.md) — What problem this solves
- [docs/PSEUDOCODE.md](docs/PSEUDOCODE.md) — The program logic in plain English
- [docs/SETUP.md](docs/SETUP.md) — Installation and Nessus setup
- [docs/USAGE.md](docs/USAGE.md) — How to run it
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — Technical design

---

## 👤 Author

**[EUGEN-NYONGESA](https://github.com/EUGEN-NYONGESA)**  
Cybersecurity Analyst | Full-Stack Developer

