# 06 — Recommendations & Security Hardening

This section provides remediation recommendations for all identified
vulnerabilities, mapped to the **CIS Critical Security Controls v8.1**.

---

## 🎯 Objective

- Provide actionable mitigations for each finding
- Map each recommendation to a CIS Control
- Prioritize remediations by risk level

---

## 🔴 Critical Priority Remediations

### 1. Disable vsftpd and Replace with Secure Alternative
**Vulnerability:** vsftpd 2.3.4 backdoor (CVE-2011-2523)  
**CIS Control:** Control 2 — Inventory and Control of Software Assets

**Actions:**
```bash
# Disable and remove vsftpd
sudo systemctl stop vsftpd
sudo systemctl disable vsftpd
sudo apt-get remove vsftpd

# Replace with secure SFTP (built into OpenSSH)
# Configure SFTP subsystem in /etc/ssh/sshd_config:
# Subsystem sftp /usr/lib/openssh/sftp-server
```

**Why:** vsftpd 2.3.4 contains a deliberate backdoor that allows
unauthenticated remote code execution. It must be removed immediately.

---

### 2. Close the Bind Shell Backdoor (Port 1524)
**Vulnerability:** Open root shell on port 1524  
**CIS Control:** Control 4 — Secure Configuration for Assets

**Actions:**
- Identify and terminate the process listening on port 1524
- Remove any scripts or services that open this shell on startup
- Implement firewall rules to block unauthorized ports

```bash
# Identify the process
sudo netstat -tlnp | grep 1524
# Kill the process
sudo kill -9 [PID]
```

---

### 3. Change Default PostgreSQL Credentials
**Vulnerability:** Default credentials allowing full DB access  
**CIS Control:** Control 4 — Secure Configuration for Assets

**Actions:**
```sql
-- Connect and change password immediately
ALTER USER postgres WITH PASSWORD '[STRONG_PASSWORD]';

-- Restrict remote access in pg_hba.conf
-- Change from: host all all 0.0.0.0/0 trust
-- Change to:   host all all 127.0.0.1/32 md5
```

---

### 4. Restrict NFS Exports
**Vulnerability:** Root filesystem exported to all hosts  
**CIS Control:** Control 4 — Secure Configuration for Assets

**Actions:**
```bash
# Edit /etc/exports — change from:
/ *

# To a restricted export:
/specific/path [TRUSTED_IP](ro,sync,no_root_squash)

# Then restart NFS
sudo exportfs -ra
sudo systemctl restart nfs-kernel-server
```

---

### 5. Disable VNC or Set Strong Password
**Vulnerability:** VNC using default password  
**CIS Control:** Control 6 — Access Control Management

**Actions:**
```bash
# Set a strong VNC password
vncpasswd

# Or disable VNC entirely if not needed
sudo systemctl stop vncserver
sudo systemctl disable vncserver
```

---

## 🟠 High Priority Remediations

### 6. Harden SSH Configuration
**Vulnerability:** Legacy algorithms, root login enabled  
**CIS Control:** Control 6 — Access Control Management

**Actions — edit `/etc/ssh/sshd_config`:**
```bash
# Disable root login
PermitRootLogin no

# Disable password authentication, use keys only
PasswordAuthentication no

# Disable legacy algorithms
KexAlgorithms curve25519-sha256,diffie-hellman-group14-sha256
HostKeyAlgorithms ecdsa-sha2-nistp256,ssh-ed25519
Ciphers aes256-gcm@openssh.com,chacha20-poly1305@openssh.com

# Restart SSH
sudo systemctl restart sshd
```

---

### 7. Update Apache and Samba
**Vulnerability:** Outdated versions with known CVEs  
**CIS Control:** Control 7 — Continuous Vulnerability Management

**Actions:**
```bash
# Update all packages
sudo apt-get update && sudo apt-get upgrade

# Specifically update Apache and Samba
sudo apt-get install --only-upgrade apache2
sudo apt-get install --only-upgrade samba
```

---

### 8. Restrict or Remove NFS rlogin and Legacy Services
**Vulnerability:** Legacy unencrypted remote access protocols  
**CIS Control:** Control 4 — Secure Configuration for Assets

**Actions:**
```bash
# Disable rlogin, rsh, rexec
sudo systemctl stop rlogin
sudo update-inetd --disable login
sudo update-inetd --disable shell
sudo update-inetd --disable exec
```

---

## 🟡 Medium Priority Remediations

### 9. Disable Telnet — Enforce SSH
**Vulnerability:** Unencrypted Telnet server  
**CIS Control:** Control 6 — Access Control Management

**Actions:**
```bash
sudo systemctl stop telnet
sudo systemctl disable telnet
sudo update-inetd --disable telnet
```

---

### 10. Upgrade SSL/TLS Configuration
**Vulnerability:** SSL v2/v3, TLS 1.0, DROWN, POODLE  
**CIS Control:** Control 7 — Continuous Vulnerability Management

**Actions:**
- Disable SSL v2 and v3 on all services
- Disable TLS 1.0 and 1.1
- Enforce TLS 1.2 minimum, TLS 1.3 preferred
- Replace weak Diffie-Hellman parameters (≥2048 bit)

---

## 🔥 Firewall & Monitoring Remediations

### 11. Implement Firewall Rules
**CIS Control:** Control 4 — Secure Configuration for Assets

```bash
# Allow only necessary inbound traffic
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Drop everything else
sudo iptables -A INPUT -j DROP

# Save rules
sudo iptables-save > /etc/iptables/rules.v4
```

---

### 12. Implement Centralized Logging and SIEM
**CIS Control:** Control 8 — Audit Log Management

**Actions:**
- Deploy a SIEM solution (e.g., Splunk, ELK Stack, Wazuh)
- Configure centralized log collection from all services
- Set up automated alerts for:
  - Multiple failed login attempts
  - Unauthorized access to sensitive files
  - Unusual network traffic patterns
- Establish a log retention policy (minimum 90 days)

---

## 📊 Remediation Priority Summary

| Priority | Finding | CIS Control | Effort |
|---|---|---|---|
| 🔴 Immediate | Remove vsftpd backdoor | Control 2 | Low |
| 🔴 Immediate | Close bind shell port 1524 | Control 4 | Low |
| 🔴 Immediate | Change PostgreSQL credentials | Control 4 | Low |
| 🔴 Immediate | Restrict NFS exports | Control 4 | Low |
| 🔴 Immediate | Secure/disable VNC | Control 6 | Low |
| 🟠 High | Harden SSH configuration | Control 6 | Medium |
| 🟠 High | Update Apache and Samba | Control 7 | Low |
| 🟠 High | Disable legacy protocols | Control 4 | Low |
| 🟡 Medium | Disable Telnet | Control 6 | Low |
| 🟡 Medium | Upgrade SSL/TLS | Control 7 | Medium |
| 🔥 Critical | Implement firewall rules | Control 4 | Medium |
| 🔥 Critical | Deploy SIEM solution | Control 8 | High |

---

## 🏁 Conclusion

The Metasploitable 2 system represents a worst-case security scenario
with critical misconfigurations across every layer of the stack.
Immediate remediation of critical findings combined with a structured
security improvement roadmap aligned to CIS Controls will significantly
reduce the attack surface and improve the overall security posture.

Regular vulnerability assessments should be scheduled quarterly to
ensure continuous security improvement.

---

> ➡️ Next: [Full Vulnerability Report](../report/vulnerability-report.md)