# 05 — Logging, Monitoring & Firewall Review

Review of authentication logs, monitoring capabilities, and firewall
configuration on the smart city legacy server.

---

## 🔐 Accessing the Target System

```bash
ssh -o HostKeyAlgorithms=+ssh-rsa \
    -o PubkeyAcceptedAlgorithms=+ssh-rsa \
    msfadmin@192.168.56.103
```
Password: [default Metasploitable credentials]

---

## 📋 Authentication Log Review

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

Jun 20 08:27:22 metasploitable sshd[9176]: Failed password for

msfadmin from [ATTACKER_IP] port 60300 ssh2

Jun 20 10:02:55 metasploitable sshd[10170]: Failed password for

invalid user ${jndi from [ATTACKER_IP] port 35742 ssh2

### Analysis

**Finding 1 — Two Log4Shell Probes Captured**
${jndi from [ATTACKER_IP] — Jun 20 05:09:51 (first scan)
${jndi from [ATTACKER_IP] — Jun 20 10:02:55 (second scan)

Both Log4Shell (CVE-2021-44228) payloads injected by Nessus during
the two scan sessions were captured in logs. Zero alerts were triggered
and zero automated responses occurred. In a real smart city environment,
this type of attack could go completely unnoticed.

**Finding 2 — No Account Lockout or Rate Limiting**
Multiple failed root login attempts across a 7-minute window produced
no lockout, no IP block, and no rate limiting of any kind. An attacker
can attempt unlimited login combinations without any consequence.

**Finding 3 — Default Credential Login Logged but Not Blocked**
Jun 20 08:27:22 — Failed password for msfadmin

Even a failed attempt on the default account was logged — confirming
that when we subsequently succeeded, that success was also logged but
triggered no alert.

---

## 🔥 Firewall Configuration Review

```bash
sudo iptables -L
```

### Result
Chain INPUT  (policy ACCEPT) — no rules
Chain FORWARD (policy ACCEPT) — no rules
Chain OUTPUT (policy ACCEPT) — no rules

### Analysis
The firewall is completely empty. Every chain has a default policy
of ACCEPT with no rules defined.

| Chain | Policy | Rules | Impact |
|---|---|---|---|
| INPUT | ACCEPT | None | All inbound traffic allowed |
| FORWARD | ACCEPT | None | All forwarded traffic allowed |
| OUTPUT | ACCEPT | None | All outbound traffic allowed |

For a server managing traffic lights and streetlights, this means:
- Any device on the city network can reach any of the 23 open ports
- No traffic filtering between city systems and this server
- An attacker who gains network access faces zero resistance

---

## 📊 Monitoring & IR Readiness

| Control Area | Status | Finding |
|---|---|---|
| Authentication Logging | ⚠️ Partial | Logs exist but unmonitored |
| Centralized SIEM | ❌ Absent | No SIEM solution detected |
| Automated Alerts | ❌ Absent | No alerting in place |
| Intrusion Detection | ❌ Absent | No IDS/IPS found |
| Log Retention Policy | ❌ Absent | No policy defined |
| Firewall Rules | ❌ Absent | iptables completely empty |
| Incident Response Plan | ❌ Absent | No IR plan found |
| Disaster Recovery | ❌ Absent | No DR/BCP strategy |
| Account Lockout Policy | ❌ Absent | No lockout after failed logins |

---

> ➡️ Next: [06 — Recommendations](06-recommendations.md)