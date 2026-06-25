# Problem Definition

## Background

A municipal IT department (or any organization) needs to regularly assess
the security of legacy servers managing critical infrastructure. Doing this
manually is slow and inconsistent.

## The Core Problem

Manual vulnerability assessment requires an analyst to:

- Remember and correctly type many different tool commands
- Switch between multiple interfaces (terminal, Nessus web UI, text editor)
- Manually interpret and transcribe large volumes of scan data
- Repeat the identical process for every new target
- Hand-write a structured report each time

This introduces three key problems:

1. **Time cost** — A single assessment can take hours of manual work.
2. **Human error** — Findings can be missed, mistyped, or misinterpreted.
3. **Inconsistency** — Two analysts may produce very different reports
   for the same system.

## Goals

The program must:

| # | Goal |
|---|------|
| 1 | Accept simple user inputs (IP, credentials, API keys) |
| 2 | Automate Nmap reconnaissance |
| 3 | Automate Nessus scanning via its API |
| 4 | Automate manual validation of common vulnerabilities |
| 5 | Automate logging and firewall review over SSH |
| 6 | Save all raw findings as evidence files |
| 7 | Generate a consistent, professional report |
| 8 | Be reproducible — same process every run |

## Non-Goals

To keep scope focused, the program will **not**:

- Exploit vulnerabilities beyond safe validation checks
- Make any changes to the target system
- Replace human judgment in interpreting business risk
- Support every possible service (focuses on common ones)

## Success Criteria

The program is successful if an analyst can run it against a target,
walk away, and return to find:

- Evidence files documenting every check performed
- A complete report matching the quality of a manually written one