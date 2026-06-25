# Architecture

A technical explanation of how AutoVAS is designed, for anyone who wants
to understand, modify, or extend it.

---

## Design Philosophy

The program follows three principles:

1. **One module, one job.** Each file in `modules/` does a single part of
   the assessment. This makes the code easy to read and to change.
2. **Fail gracefully.** A failure in one stage never crashes the whole
   program. It saves what it can and continues.
3. **Mirror the manual process.** The program follows the exact same steps
   a human analyst takes, so the code is easy to relate to the real-world
   workflow it automates.

---

## How the Pieces Fit Together

main.py
                   (orchestrator)
                         │
   ┌──────────┬──────────┼──────────┬──────────┐
   ▼          ▼          ▼          ▼          ▼

   inputs.py   recon.py   nessus.py  validation  logging_review

│          │          │          │          │

└──────────┴──────────┴──────────┴──────────┘

│

collected data objects

│

┌──────────────┴──────────────┐

▼                              ▼

evidence.py                     report.py

(saves .txt proof)          (builds .txt + .docx)


`main.py` calls each module in order and passes the resulting data along.
The modules never call each other directly — all coordination happens in
the orchestrator. This keeps the modules independent and testable.

---

## The Modules

| Module | Responsibility | Key external tool/library |
|---|---|---|
| `inputs.py` | Collect and validate user input | getpass |
| `recon.py` | Nmap scan and asset categorization | python-nmap |
| `nessus.py` | Drive Nessus through its REST API | requests |
| `validation.py` | Safe checks (FTP, SSH, PostgreSQL, NFS) | ftplib, paramiko |
| `logging_review.py` | Read logs and firewall over SSH | paramiko |
| `evidence.py` | Write findings to .txt files | (standard library) |
| `report.py` | Build the final .txt and .docx report | python-docx |

---

## Data Flow

Each assessment stage produces a Python dictionary. For example, the recon
stage returns:

```python
{
    "services": [...],        # list of open ports/services
    "categorized": {...},     # services grouped by risk
    "os_guess": "...",        # detected operating system
    "summary_text": "..."     # ready-to-save text summary
}
```

These dictionaries are passed to `evidence.py` (to be saved) and to
`report.py` (to be turned into the report). Because every stage produces a
`summary_text` field, saving evidence is uniform and simple.

---

## Why a Knowledge Base for Recon?

`recon.py` contains a `RISK_KNOWLEDGE` dictionary that maps known ports to
risk levels and explanations. This encodes the expert judgment a human
analyst applies when categorizing assets. Keeping it as a simple dictionary
means anyone can extend it — just add a new port and its risk reasoning.

---

## Extending the Program

The design makes common extensions straightforward:

- **Add a new validation check:** write a new function in `validation.py`
  following the pattern of the existing ones (return a dict with `check`,
  `success`, and `detail`), then add it to the `run_validation` list.
- **Support a new service in recon:** add an entry to `RISK_KNOWLEDGE`.
- **Change the report wording:** edit `build_report_sections` in
  `report.py` — both the text and Word reports update automatically.
- **Add a new output format (e.g. PDF):** add a new generator function in
  `report.py` that consumes the same `sections` list.

---

## Error Handling Strategy

Every module's main function is wrapped in error handling at the
orchestrator level. Within modules, network and tool operations have their
own try/except blocks that return a descriptive result rather than raising.
This two-layer approach means:

- Expected problems (a closed port, a missing tool) are handled inside the
  module and reported cleanly.
- Unexpected problems are caught by the orchestrator so the program still
  finishes and saves what it has.