# Smart City Infrastructure — Vulnerability Assessment

## The Problem

> You are a Cybersecurity Analyst working for a municipal IT department
> responsible for securing critical infrastructure in a newly developed
> smart city initiative. A legacy network server, which manages traffic
> monitoring and smart streetlights, has been flagged as a potential
> security risk due to its outdated software and weak authentication
> mechanisms.
>
> Your team has assigned you to conduct a security audit of the server,
> identifying vulnerabilities that could lead to unauthorized access or
> system manipulation, which could disrupt city operations.
>
> Using Nessus on a Kali Linux VM, perform a comprehensive vulnerability
> scan on Metasploitable 2, assess the impact of discovered security
> weaknesses, and provide actionable mitigation strategies to enhance
> the security of the smart city infrastructure.

---

## 🎯 Objective

Conduct a full vulnerability assessment of a legacy smart city server,
identify security weaknesses that could lead to unauthorized access or
infrastructure manipulation, and recommend mitigations aligned with the
**CIS Critical Security Controls v8.1**.

---

## 🛠️ Tools Used

| Tool | Purpose |
|---|---|
| **Nmap** | Network enumeration and service/OS discovery |
| **Nessus Essentials** | Automated vulnerability scanning |
| **FTP Client** | Manual validation of anonymous FTP access |
| **SSH Client** | Manual validation of default SSH credentials |
| **psql** | Manual validation of default PostgreSQL credentials |
| **showmount** | NFS export enumeration |
| **iptables** | Firewall configuration review |

---

## 🖥️ Environment

| Component | Details |
|---|---|
| **Attacker Machine** | Kali Linux — 192.168.56.102 |
| **Target Machine** | Metasploitable 2 — 192.168.56.103 |
| **Network Type** | VirtualBox Host-Only Adapter |
| **Target OS** | Ubuntu 8.04 (End of Life since 2013) |
| **Context** | Legacy server managing traffic monitoring and smart streetlights |

---

## 📁 Repository Structure
smart-city-security-assessment/

│

├── README.md                        # Project overview (this file)

├── report/

│   └── vulnerability-report.txt    # Full formal vulnerability report

├── walkthrough/

│   ├── 01-setup.md                  # VM setup & network configuration

│   ├── 02-reconnaissance.md         # Nmap scan & asset discovery

│   ├── 03-nessus-scan.md           # Nessus setup & scan results

│   ├── 04-manual-validation.md      # Manual validation of findings

│   ├── 05-logging-firewall.md       # Logging & firewall review

│   └── 06-recommendations.md       # CIS Controls-based mitigations

└── screenshots/

└── README.md                    # Screenshot guide


---

## 🔍 Key Findings Summary

| Severity | Count | Smart City Impact |
|---|---|---|
| 🔴 Critical | 10 | Direct infrastructure takeover possible |
| 🟠 High | 6 | Remote code execution on city systems |
| 🟡 Medium | 24 | Encrypted traffic interception risk |
| 🟡 Low | 9 | Information disclosure |
| 🔵 Info | 140 | Service and configuration detections |
| **Total** | **69** | |

---

## 🚨 Most Critical Findings

| Finding | CVSS | Real-World Risk |
|---|---|---|
| Bind Shell Backdoor (Port 1524) | 9.8 | Instant root access to traffic control server |
| VNC Default Password | 10.0 | Attacker views and controls city dashboard live |
| vsftpd 2.3.4 Backdoor | 10.0 | Malicious configs uploadable to city systems |
| NFS Root Export (`/ *`) | 7.5 | All city data readable by any network host |
| Default SSH Credentials | 7.5 | msfadmin/msfadmin grants remote server access |
| Default PostgreSQL Credentials | 9.8 | Full database access — all sensor data exposed |
| Empty Firewall (iptables) | N/A | All 23 ports reachable with zero filtering |
| OS End of Life (Ubuntu 8.04) | 10.0 | No security patches available since 2013 |

---

## 📋 Compliance Framework

All recommendations are mapped to **CIS Critical Security Controls v8.1**:

| CIS Control | Application |
|---|---|
| Control 1 — Enterprise Asset Inventory | Track all city infrastructure components |
| Control 2 — Software Asset Inventory | Remove unauthorized/outdated software |
| Control 4 — Secure Configuration | Harden all services and close unused ports |
| Control 5 — Account Management | Eliminate default credentials across all services |
| Control 6 — Access Control Management | Enforce least privilege and disable root login |
| Control 7 — Continuous Vulnerability Management | Patch all services, replace EOL OS |
| Control 8 — Audit Log Management | Deploy SIEM, configure alerting |
| Control 12 — Network Infrastructure Management | Implement firewall rules and segmentation |
| Control 13 — Network Monitoring and Defense | Deploy IDS/IPS for real-time detection |
| Control 17 — Incident Response Management | Develop and test IR plan |

---

## ⚠️ Disclaimer

This assessment was conducted in a **controlled lab environment** using
intentionally vulnerable software. All findings are documented for
**educational purposes only**. Never perform security assessments on
systems you do not own or have explicit written permission to test.

---

## 🔗 Related Work

This assessment is part of a series of vulnerability assessments
demonstrating the same methodology applied to different organizational
contexts:

- [XYZ Financial Services — Legacy Infrastructure Audit](https://github.com/EUGEN-NYONGESA/metasploitable2-assessment)
- **Smart City Infrastructure Assessment** ← you are here

---

## 📄 Full Report

👉 [View the Full Vulnerability Report](report/vulnerability-report.txt)

---

## 👤 Author

**[EUGEN-NYONGESA](https://github.com/EUGEN-NYONGESA)**  
Cybersecurity Analyst | Full-Stack Developer