# 04 — Manual Validation of Findings

Manual verification of key vulnerabilities to confirm exploitability
and assess real-world impact on smart city operations.

---

## 🎯 Objective

- Manually confirm vulnerabilities found by Nessus
- Test for anonymous and default credential access
- Assess impact on traffic monitoring and streetlight systems

---

## ✅ Test 1 — Anonymous FTP Access (vsftpd 2.3.4)

### What We're Testing
vsftpd 2.3.4 allows unauthenticated anonymous login. An attacker
could use this to upload malicious configuration files to the
traffic monitoring system.

### Command
```bash
ftp 192.168.56.103
```
Username: `anonymous` | Password: press Enter

### Result
Connected to 192.168.56.103.

220 (vsFTPd 2.3.4)

Name: anonymous

331 Please specify the password.

Password:

230 Login successful.

Remote system type is UNIX.

### ✅ Validated
Anonymous FTP login confirmed with no credentials. In a smart city
context, an attacker could use this to replace traffic light
configuration files with malicious ones, causing signal failures
or dangerous intersection behavior.

**Severity:** Critical
**CVE:** CVE-2011-2523
**CIS Control:** Control 4 — Secure Configuration of Enterprise Assets

---

## ✅ Test 2 — Default SSH Credentials

### What We're Testing
OpenSSH 4.7p1 with default credentials (msfadmin/msfadmin) grants
full remote access to the city infrastructure server.

### Command
```bash
ssh -o HostKeyAlgorithms=+ssh-rsa \
    -o PubkeyAcceptedAlgorithms=+ssh-rsa \
    msfadmin@192.168.56.103
```
Password: `msfadmin`

### Result
Linux metasploitable 2.6.24-16-server #1 SMP Thu Apr 10 13:58:00 UTC 2008

Last login: Sat Jun 20 08:27:27 2026 from 192.168.56.102

msfadmin@metasploitable:~$

### ✅ Validated
Full SSH access granted using default credentials. An attacker now
has a remote shell on the server managing city traffic and streetlights.
They can stop services, alter configurations, or pivot to other
city systems from this foothold.

**Severity:** High
**CIS Control:** Control 5 — Account Management

---

## ✅ Test 3 — Default PostgreSQL Credentials

### What We're Testing
PostgreSQL 8.3.x running with default credentials, exposing all
city sensor and operational databases.

### Command
```bash
PGPASSWORD=postgres psql -h 192.168.56.103 -U postgres
```

### Result
psql (8.3.1)

SSL connection (cipher: DHE-RSA-AES256-SHA, bits: 256)

Type "help" for help.

postgres=#

### ✅ Validated
Full PostgreSQL administrative access granted. All city databases —
including traffic sensor readings, streetlight schedules, and
operational logs — are accessible. Additionally, the SSL connection
uses an outdated cipher suite, confirming cryptographic weaknesses.

**Severity:** Critical
**CIS Control:** Control 5 — Account Management

---

## ✅ Test 4 — NFS Root Filesystem Export

### What We're Testing
NFS service exporting the entire root filesystem to all hosts
with no access restrictions.

### Command
```bash
showmount -e 192.168.56.103
```

### Result
Export list for 192.168.56.103:
/ *

### ✅ Validated
The entire root filesystem is exported to all hosts (`*`) with no
restrictions. Any machine on the city network can mount this share
and read every file including:
- `/etc/shadow` — system password hashes
- SSH private keys — enabling passwordless access
- Traffic configuration files — enabling infrastructure manipulation
- All database files — exposing city operational data

**Severity:** Critical
**CIS Control:** Control 4 — Secure Configuration of Enterprise Assets

---

## 📊 Validation Summary

| Test | Vulnerability | Result | Severity |
|---|---|---|---|
| Anonymous FTP | vsftpd 2.3.4 no-auth login | ✅ Confirmed | Critical |
| Default SSH | msfadmin/msfadmin remote shell | ✅ Confirmed | High |
| Default PostgreSQL | postgres/postgres full DB access | ✅ Confirmed | Critical |
| NFS Root Export | `/ *` world-accessible | ✅ Confirmed | Critical |

---

> ➡️ Next: [05 — Logging & Firewall Review](05-logging-firewall.md)