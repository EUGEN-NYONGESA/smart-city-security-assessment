# 03 — Nessus Vulnerability Scan

This section documents the Nessus automated vulnerability scan performed
against the target system, including setup, configuration, and results.

---

## 🎯 Objective

- Configure and launch a Nessus Basic Network Scan
- Identify vulnerabilities across all open ports and services
- Categorize findings by severity level

---

## ⚙️ Nessus Scan Configuration

### Step 1 — Start Nessus
```bash
sudo systemctl start nessusd
```

Then open Firefox and navigate to:
https://localhost:8834

### Step 2 — Create a New Scan
1. Click **"New Scan"**
2. Select **"Basic Network Scan"**
3. Configure the scan:
   - **Name:** `Metasploitable2 Assessment`
   - **Target:** `[TARGET_IP]`
4. Click **"Save"** then **"Launch"**

> ⏱️ Scan Duration: approximately 15-20 minutes

---

## 📊 Scan Summary

| Metric | Value |
|---|---|
| **Policy** | Basic Network Scan |
| **Status** | Completed |
| **Severity Base** | CVSS v3.0 |
| **Scanner** | Local Scanner |
| **Total Vulnerabilities** | 70 |
| **Scan Duration** | 19 minutes |

### Vulnerability Distribution

| Severity | Count |
|---|---|
| 🔴 Critical | 6 |
| 🟠 High | 3 |
| 🟡 Medium | 4 |
| 🟡 Low | 3 |
| 🔵 Info | 54 |

---

## 🔴 Critical Findings

| Vulnerability | CVSS | Family | Count |
|---|---|---|---|
| Canonical Ubuntu Linux SEoL (8.04.x) | 10.0 | General | 1 |
| VNC Server 'password' Password | 10.0 | Gain a shell remotely | 1 |
| SSL Version 2 and 3 Protocol Detection | 9.8 | Service detection | 2 |
| Bind Shell Backdoor Detection | 9.8 | Backdoors | 1 |
| SSL (Multiple Issues) | Critical | Gain a shell remotely | 3 |

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

---

## 🟡 Low Findings

| Vulnerability | CVSS | Family | Count |
|---|---|---|---|
| SSL/TLS Diffie-Hellman Modulus <= 1024 Bit | 3.7 | Misc | 1 |
| X Server Detection | 2.6 | Service detection | 1 |
| ICMP Timestamp Request Remote Date Disclosure | 2.1 | General | 1 |

---

## 🔵 Notable Informational Findings

| Group | Count | Family |
|---|---|---|
| SMB (Multiple Issues) | 7 | Windows |
| Nessus SYN Scanner | 25 | Port scanners |
| RPC Services Enumeration | 10 | Service detection |
| TLS (Multiple Issues) | 4 | General |
| DNS (Multiple Issues) | 3 | DNS |
| FTP (Multiple Issues) | 3 | Service detection |
| VNC (Multiple Issues) | 3 | Service detection |
| SSH (Multiple Issues) | 2+2 | General/Service detection |
| Apache HTTP Server (Multiple Issues) | 2 | Web Servers |
| MySQL Server Detection | 2 | Databases |

---

## 🔑 Key Observations from Nessus KB File

The Nessus knowledge base file confirmed additional technical details:

- `Services/wild_shell=1524` — Bind shell backdoor active on port 1524
- `nfs/exportlist=/` — Entire root filesystem exported via NFS
- `ftp/banner/21=220 (vsFTPd 2.3.4)` — vsftpd backdoor version confirmed
- `SSL/vulnerable_to_poodle/5432=1` — PostgreSQL vulnerable to POODLE
- `Host/PQC/22/SSH/vulnerable=1` — SSH vulnerable to post-quantum concerns
- `mysql/3306/ver=5.0.51a-3ubuntu5` — MySQL version confirmed
- `www/apache/80/pristine/version=2.2.8` — Apache version confirmed
- Telnet banner exposed credentials in plaintext

---

> ➡️ Next: [04 — Manual Validation](04-manual-validation.md)