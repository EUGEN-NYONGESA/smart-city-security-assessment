# 05 — Logging, Monitoring & Firewall Review

This section documents the review of logging mechanisms, monitoring
capabilities, and firewall configuration on the target system.

---

## 🎯 Objective

- Assess whether the system logs security events
- Determine if any monitoring or alerting is in place
- Review firewall rules and network access controls

---

## 🔐 Accessing the Target System

To run commands on the target system from Kali, SSH in using
the default credentials:

```bash
ssh -o HostKeyAlgorithms=+ssh-rsa \
    -o PubkeyAcceptedAlgorithms=+ssh-rsa \
    msfadmin@[TARGET_IP]
```

> Password: [REDACTED — default Metasploitable credentials]

---

## 📋 Task 1 — Review Authentication Logs

### Command
```bash
cat /var/log/auth.log | grep "Failed password"
```

### Result
Jun 20 05:09:51 metasploitable sshd[5735]: Failed password for

invalid user ${jndi from [ATTACKER_IP] port 34382 ssh2

Jun 20 05:59:23 metasploitable sshd[6199]: Failed password for

root from [ATTACKER_IP] port 48168 ssh2

Jun 20 06:00:02 metasploitable sshd[6203]: Failed password for

root from [ATTACKER_IP] port 36698 ssh2

Jun 20 06:00:50 metasploitable sshd[6206]: Failed password for

root from [ATTACKER_IP] port 56640 ssh2

Jun 20 06:02:06 metasploitable sshd[6206]: Failed password for

root from [ATTACKER_IP] port 56640 ssh2

Jun 20 06:02:29 metasploitable sshd[6206]: Failed password for

root from [ATTACKER_IP] port 56640 ssh2

Jun 20 06:02:45 metasploitable sshd[6215]: Failed password for

root from [ATTACKER_IP] port 45368 ssh2

Jun 20 06:03:24 metasploitable sshd[6217]: Failed password for

root from [ATTACKER_IP] port 55098 ssh2

Jun 20 06:06:42 metasploitable sshd[6228]: Failed password for

root from [ATTACKER_IP] port 33800 ssh2

### Analysis

**Finding 1 — Basic logging exists but is unmonitored:**
- Auth logs are present and recording failed login attempts
- However there is no SIEM, no alerting, and no one reviewing them
- Logs exist but provide no active protection

**Finding 2 — Log4Shell probe detected:**
Failed password for invalid user ${jndi from [ATTACKER_IP]

- Nessus probed the system with a **Log4Shell (CVE-2021-44228)**
  injection payload via SSH during the scan
- The `${jndi...}` string in the username field confirms the probe
- This is consistent with the extensive `log4shell/dns` entries
  found in the Nessus KB file

---

## 🔥 Task 2 — Review Firewall Configuration

### Command
```bash
sudo iptables -L
```

### Result
Chain INPUT (policy ACCEPT)

target     prot opt source               destination
Chain FORWARD (policy ACCEPT)

target     prot opt source               destination
Chain OUTPUT (policy ACCEPT)

target     prot opt source               destination

### Analysis
The firewall is **completely empty** — no rules whatsoever:

| Chain | Policy | Rules | Risk |
|---|---|---|---|
| INPUT | ACCEPT | None | All inbound traffic accepted |
| FORWARD | ACCEPT | None | All forwarded traffic accepted |
| OUTPUT | ACCEPT | None | All outbound traffic accepted |

This means:
- ❌ No port blocking
- ❌ No IP filtering
- ❌ No traffic inspection
- ❌ All 23 open ports are completely unprotected
- ❌ An attacker can reach every service with no restriction

---

## 📊 Monitoring & IR Readiness Summary

| Control Area | Status | Finding |
|---|---|---|
| Authentication Logging | ⚠️ Partial | Logs exist but unmonitored |
| Centralized SIEM | ❌ Missing | No SIEM solution detected |
| Automated Alerts | ❌ Missing | No alerting mechanisms |
| Intrusion Detection (IDS) | ❌ Missing | No IDS/IPS in place |
| Log Retention Policy | ❌ Missing | No retention policy found |
| Firewall Rules | ❌ Missing | iptables completely empty |
| Incident Response Plan | ❌ Missing | No IR plan evident |
| Disaster Recovery | ❌ Missing | No DR/BCP strategy found |

---

## 🔑 Key Conclusions

1. The system has **basic logging** but no active monitoring
2. Without a SIEM or IDS, a breach could go **undetected indefinitely**
3. The **empty firewall** leaves all services fully exposed
4. The **Log4Shell probe** in logs highlights the need for
   log analysis and threat detection tools
5. In the event of a breach, there would be **minimal forensic
   data** available for investigation

---

> ➡️ Next: [06 — Recommendations](06-recommendations.md)
