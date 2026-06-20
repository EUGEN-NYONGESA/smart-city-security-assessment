# 06 — Recommendations & Security Hardening

Remediation recommendations for all identified vulnerabilities mapped
to CIS Critical Security Controls v8.1, with smart city context.

---

## 🔴 Immediate — Critical Priority

### 1. Remove vsftpd and Replace with SFTP
**CIS Control 4** — Secure Configuration of Enterprise Assets

vsftpd 2.3.4 must be removed immediately. It contains a deliberate
backdoor that could allow an attacker to upload malicious traffic
control configurations.

```bash
sudo systemctl stop vsftpd
sudo systemctl disable vsftpd
sudo apt-get remove vsftpd
```

Replace with SFTP via OpenSSH — no additional software needed.

---

### 2. Close the Bind Shell on Port 1524
**CIS Control 4** — Secure Configuration of Enterprise Assets

An open root shell on a server managing city infrastructure is an
immediate critical risk. Identify and terminate the process, then
block the port at the firewall.

```bash
sudo netstat -tlnp | grep 1524
sudo kill -9 [PID]
```

---

### 3. Eliminate All Default Credentials
**CIS Control 5** — Account Management

Change credentials immediately on all services:
- PostgreSQL: `ALTER USER postgres WITH PASSWORD '[STRONG_PASSWORD]';`
- VNC: run `vncpasswd` to set a strong password
- SSH: disable password auth, enforce key-based authentication
- MySQL: change root password and remove anonymous accounts

For a city infrastructure server, default credentials represent
a direct path to manipulating public safety systems.

---

### 4. Restrict NFS Exports
**CIS Control 4** — Secure Configuration of Enterprise Assets

Edit `/etc/exports` to restrict access:
```bash
# Change from:
/ *

# To specific paths and trusted IPs only:
/city/traffic/configs [TRUSTED_IP](ro,sync,root_squash)
```

Never export the root filesystem. Exporting `/` to `*` gives any
network device full read/write access to all city system files.

---

### 5. Disable SSL v2/v3 and Enforce TLS 1.2+
**CIS Control 7** — Continuous Vulnerability Management

SSL v2 and v3 are broken protocols. Their presence enables DROWN
and POODLE attacks, allowing interception of encrypted city data
communications including sensor readings and control commands.

---

## 🟠 High Priority

### 6. Harden SSH Configuration
**CIS Control 6** — Access Control Management

Edit `/etc/ssh/sshd_config`:
```bash
PermitRootLogin no
PasswordAuthentication no
MaxAuthTries 3
LoginGraceTime 30
AllowUsers [specific_admin_user]
```

Restart SSH after changes:
```bash
sudo systemctl restart sshd
```

---

### 7. Disable All Legacy Remote Access Protocols
**CIS Control 4** — Secure Configuration of Enterprise Assets

Telnet, rlogin, rsh, and rexec all transmit data in plaintext.
On a city infrastructure server, this means admin credentials and
control commands travel unencrypted across the network.

```bash
sudo update-inetd --disable telnet
sudo update-inetd --disable login
sudo update-inetd --disable shell
sudo update-inetd --disable exec
```

---

### 8. Patch or Replace Outdated Services
**CIS Control 7** — Continuous Vulnerability Management

| Service | Current | Action |
|---|---|---|
| Ubuntu 8.04 | EOL 2013 | Migrate to Ubuntu 22.04 LTS |
| Apache 2.2.8 | EOL | Upgrade to Apache 2.4.x |
| OpenSSH 4.7p1 | Outdated | Upgrade to latest stable |
| PostgreSQL 8.3 | EOL | Upgrade to PostgreSQL 15+ |
| Samba 3.X | Vulnerable | Upgrade to 4.2.11+ |
| ISC BIND 9.4.2 | Vulnerable | Upgrade to 9.11.22+ |

Nessus remediations tab specifically flagged:
- ISC BIND: upgrade to 9.11.22 / 9.16.6 / 9.17.4
- Samba: upgrade to 4.2.11 / 4.3.8 / 4.4.2

---

## 🔥 Infrastructure & Monitoring

### 9. Implement Firewall Rules
**CIS Control 12** — Network Infrastructure Management

```bash
# Allow only required services
sudo iptables -A INPUT -m state \
  --state ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Drop everything else
sudo iptables -A INPUT -j DROP

# Save rules
sudo iptables-save > /etc/iptables/rules.v4
```

---

### 10. Deploy SIEM and Intrusion Detection
**CIS Control 8** — Audit Log Management
**CIS Control 13** — Network Monitoring and Defense

- Deploy **Wazuh** or **ELK Stack** for centralized log collection
- Configure alerts for: multiple failed logins, NFS mount attempts,
  unauthorized port access, and after-hours activity
- Deploy **Snort** or **Suricata** for real-time traffic analysis
- Establish log retention of minimum 90 days

For smart city infrastructure, real-time detection is critical —
a compromised traffic server could cause accidents within minutes.

---

### 11. Develop an Incident Response Plan
**CIS Control 17** — Incident Response Management

The IR plan for smart city infrastructure must include:
- Immediate isolation procedures for the traffic server
- Fallback to manual traffic control during incidents
- Escalation contacts including city operations center
- Communication plan for public notification if services are disrupted
- Post-incident forensic review process
- Quarterly IR drills

---

## 📊 Full Remediation Priority Table

| Priority | Finding | CIS Control | Effort |
|---|---|---|---|
| 🔴 Immediate | Remove vsftpd backdoor | Control 4 | Low |
| 🔴 Immediate | Close bind shell port 1524 | Control 4 | Low |
| 🔴 Immediate | Change all default credentials | Control 5 | Low |
| 🔴 Immediate | Restrict NFS exports | Control 4 | Low |
| 🔴 Immediate | Disable SSL v2/v3 | Control 7 | Medium |
| 🟠 High | Harden SSH configuration | Control 6 | Medium |
| 🟠 High | Disable Telnet/rlogin/rsh | Control 4 | Low |
| 🟠 High | Patch all outdated services | Control 7 | High |
| 🟠 High | Migrate OS to Ubuntu 22.04 | Control 7 | High |
| 🔥 Critical | Implement firewall rules | Control 12 | Medium |
| 🔥 Critical | Deploy SIEM and IDS | Control 8/13 | High |
| 🔥 Critical | Develop IR plan | Control 17 | Medium |

---

> ➡️ Next: [Full Vulnerability Report](../report/vulnerability-report.txt)