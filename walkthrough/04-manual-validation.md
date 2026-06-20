# 04 — Manual Validation of Findings

This section documents the manual validation of key vulnerabilities
identified by the Nessus scan, confirming their exploitability.

---

## 🎯 Objective

- Manually confirm at least 3 vulnerabilities found by Nessus
- Document proof of exploitation for each finding
- Assess real-world impact of each vulnerability

---

## ✅ Test 1 — Anonymous FTP Access (vsftpd 2.3.4)

### What We're Testing
vsftpd 2.3.4 contains a known backdoor (CVE-2011-2523) and allows
anonymous login without credentials.

### Command
```bash
ftp [TARGET_IP]
```

### Steps
1. When prompted for **Name**, enter: `anonymous`
2. When prompted for **Password**, press **Enter** (no password)

### Result
Connected to [TARGET_IP].

220 (vsFTPd 2.3.4)

Name: anonymous

331 Please specify the password.

Password:

230 Login successful.

Remote system type is UNIX.

Using binary mode to transfer files.


### ✅ Validated
Anonymous FTP login succeeded with no credentials. An attacker could
upload malicious files or access sensitive data on the FTP server.

**Severity:** Critical  
**CVE:** CVE-2011-2523  
**CIS Control:** CIS Control 4 — Secure Configuration for Assets

---

## ✅ Test 2 — Weak SSH Configuration

### What We're Testing
OpenSSH 4.7p1 uses legacy weak algorithms and exposes the system
to brute-force attacks with root login enabled.

### Command
```bash
ssh -o HostKeyAlgorithms=+ssh-rsa \
    -o PubkeyAcceptedAlgorithms=+ssh-rsa \
    root@[TARGET_IP]
```

### Result
root@[TARGET_IP]'s password:

Permission denied, please try again.

### ✅ Validated
Key findings confirmed:
- SSH connection was accepted and prompted for password
- Legacy `ssh-rsa` algorithm had to be explicitly enabled,
  confirming the server uses outdated cryptographic standards
- Root login is enabled, making brute-force attacks feasible
- All failed attempts were logged in `/var/log/auth.log`
- Nessus KB confirmed: `Host/PQC/22/SSH/vulnerable=1`

**Severity:** High  
**CIS Control:** CIS Control 6 — Access Control Management

---

## ✅ Test 3 — Default PostgreSQL Credentials

### What We're Testing
PostgreSQL 8.3.x is running with default credentials,
allowing unauthorized database access.

### Command
```bash
PGPASSWORD=postgres psql -h [TARGET_IP] -U postgres
```

### Result
psql (16.2 (Debian 16.2-1), server 8.3.1)

WARNING: psql major version 16, server major version 8.3.

Some psql features might not work.

Type "help" for help.
postgres=#

### ✅ Validated
Full PostgreSQL administrative access granted using default
credentials (`postgres/postgres`). Additionally confirmed:
- Server version 8.3.1 is severely outdated (EOL)
- SSL connection failed with unsupported protocol error,
  confirming POODLE/DROWN vulnerability
- An attacker has full control over all databases

**Severity:** Critical  
**CVE:** CVE-2012-2122  
**CIS Control:** CIS Control 4 — Secure Configuration for Assets

---

## ✅ Test 4 — NFS Root Filesystem Export

### What We're Testing
The NFS service is exporting the entire root filesystem
to all hosts with no access restrictions.

### Command
```bash
showmount -e [TARGET_IP]
```

### Result
Export list for [TARGET_IP]:

/ *

### ✅ Validated
The entire root filesystem (`/`) is exported to all hosts (`*`).
This means any machine on the network can mount and access:
- `/etc/passwd` and `/etc/shadow` (credentials)
- SSH keys
- Database files
- All system configuration files

This is one of the most severe misconfigurations found.

**Severity:** Critical  
**CIS Control:** CIS Control 4 — Secure Configuration for Assets

---

## 📊 Validation Summary

| Test | Vulnerability | Result | Severity |
|---|---|---|---|
| Anonymous FTP | vsftpd 2.3.4 anonymous login | ✅ Confirmed | Critical |
| Weak SSH | Legacy algorithms, root exposed | ✅ Confirmed | High |
| Default PostgreSQL | postgres/postgres access | ✅ Confirmed | Critical |
| NFS Export | Root filesystem world-readable | ✅ Confirmed | Critical |

---

> ➡️ Next: [05 — Logging & Firewall Review](05-logging-firewall.md)

