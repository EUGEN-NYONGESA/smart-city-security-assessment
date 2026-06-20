# 03 — Nessus Vulnerability Scan

Automated vulnerability scan performed using Nessus Essentials against
the smart city legacy server.

---

## ⚙️ Scan Configuration

### Start Nessus
```bash
sudo systemctl start nessusd
```

Navigate to `https://localhost:8834` in Firefox.

### Create New Scan
1. Click **"New Scan"**
2. Select **"Basic Network Scan"**
3. Configure:
   - **Name:** `Smart City Infrastructure Assessment`
   - **Target:** `192.168.56.103`
4. Click **"Save"** then **"Launch"**

---

## 📊 Scan Summary

| Metric | Value |
|---|---|
| **Scan Name** | Smart City Infrastructure Assessment |
| **Policy** | Basic Network Scan |
| **Status** | Completed |
| **Severity Base** | CVSS v3.0 |
| **Start** | Today at 2:19 PM |
| **End** | Today at 2:38 PM |
| **Duration** | 19 minutes |
| **Total Vulnerabilities** | 69 |

### Vulnerability Breakdown (Host View)

| Severity | Count |
|---|---|
| 🔴 Critical | 10 |
| 🟠 High | 6 |
| 🟡 Medium | 24 |
| 🟡 Low | 9 |
| 🔵 Info | 140 |

---

## 🔴 Critical Findings

| Vulnerability | CVSS | Family | Count |
|---|---|---|---|
| Canonical Ubuntu Linux SEoL (8.04.x) | 10.0 | General | 1 |
| VNC Server 'password' Password | 10.0 | Gain a shell remotely | 1 |
| SSL Version 2 and 3 Protocol Detection | 9.8 | Service detection | 2 |
| Bind Shell Backdoor Detection | 9.8 | Backdoors | 1 |
| SSL (Multiple Issues) | Critical | Gain a shell remotely | 3 |
| Apache Tomcat (Multiple Issues) | Mixed | Web Servers | 4 |

---

## 🟠 High Findings

| Vulnerability | CVSS | Family | Count |
|---|---|---|---|
| NFS Shares World Readable | 7.5 | RPC | 1 |
| rlogin Service Detection | 7.5 | Service detection | 1 |
| Samba Badlock Vulnerability | 7.5 | General | 1 |

---

## 🟡 Medium Findings

| Vulnerability | CVSS | Family | Count |
|---|---|---|---|
| TLS Version 1.0 Protocol Detection | 6.5 | Service detection | 2 |
| Unencrypted Telnet Server | 6.5 | Misc | 1 |
| SSL Anonymous Cipher Suites Supported | 5.9 | Service detection | 1 |
| SSL DROWN Attack Vulnerability | 5.9 | Misc | 1 |
| SSL (Multiple Issues) | Mixed | General | 28 |
| ISC Bind (Multiple Issues) | Mixed | DNS | 5 |
| SSH (Multiple Issues) | Mixed | Misc | 6 |
| HTTP (Multiple Issues) | Mixed | Web Servers | 5 |
| SMB (Multiple Issues) | Mixed | Misc | 2 |
| TLS (Multiple Issues) x2 | Mixed | Misc/SMTP | 2+2 |

---

## 🟡 Low Findings

| Vulnerability | CVSS | Family |
|---|---|---|
| SSL/TLS Diffie-Hellman Modulus <= 1024 Bit | 3.7 | Misc |
| X Server Detection | 2.6 | Service detection |
| ICMP Timestamp Request Remote Date Disclosure | 2.1 | General |

---

## 🔵 Notable Info Findings

| Finding | Count | Family |
|---|---|---|
| SMB (Multiple Issues) | 7 | Windows |
| Nessus SYN Scanner | 25 | Port scanners |
| RPC Services Enumeration | 10 | Service detection |
| Service Detection | 10 | Service detection |
| FTP (Multiple Issues) | 3 | Service detection |
| VNC (Multiple Issues) | 3 | Service detection |
| DNS (Multiple Issues) | 3 | DNS |
| SSH (Multiple Issues) | 2+2 | General/Service detection |
| Apache HTTP Server (Multiple Issues) | 2 | Web Servers |
| MySQL Server Detection | 2 | Databases |
| NFS Share Export List | 1 | RPC |
| vsftpd Detection | 1 | FTP |
| PostgreSQL Server Detection | 1 | Service detection |
| Telnet Server Detection | 1 | Service detection |

---

## 🔧 Nessus Recommended Remediations

| Action | Vulnerabilities Addressed |
|---|---|
| Upgrade ISC BIND to 9.11.22 / 9.16.6 / 9.17.4 or later | 3 |
| Upgrade Samba to 4.2.11 / 4.3.8 / 4.4.2 or later | 1 |

---

## ⚠️ Scan Limitations

The Notes tab flagged 3 DNS issues during the scan:
- Unable to resolve `log4shell-generic-*.r.nessus.org`
- Unable to resolve DNS `r.nessus.org` to check Log4j Vulnerability

This occurred because the VM operates in an isolated Host-Only network
with no external DNS access. As a result, **Log4Shell (CVE-2021-44228)**
could not be fully validated via external DNS callback during this scan.
However, Log4Shell probe payloads were captured in the system's auth logs,
confirming the test was attempted. This is a testing limitation, not an
indication the system is safe from Log4Shell.

---

> ➡️ Next: [04 — Manual Validation](04-manual-validation.md)