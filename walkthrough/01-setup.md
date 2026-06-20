# 01 — Environment Setup

This section documents the environment setup required before conducting
the smart city infrastructure vulnerability assessment.

---

## 🖥️ Virtual Machines Required

| VM | Role | IP Address |
|---|---|---|
| Kali Linux | Attacker / Assessment Machine | 192.168.56.102 |
| Metasploitable 2 | Target / Legacy Smart City Server | 192.168.56.103 |

---

## 🌐 Network Configuration

Both VMs run on a **VirtualBox Host-Only Adapter** to isolate the
assessment from external networks — simulating an internal audit of
the smart city server without exposing real infrastructure.

### Configure Host-Only Adapter
1. Open **VirtualBox**
2. Select VM → **Settings** → **Network**
3. Set **Adapter 1** to **Host-Only Adapter**
4. Repeat for both VMs

### Verify Connectivity
```bash
ping 192.168.56.103
```

Expected output:
64 bytes from 192.168.56.103: icmp_seq=1 ttl=64 time=0.5 ms
0% packet loss

---

## 🔧 Nessus Installation on Kali Linux

### Step 1 — Register for Nessus Essentials
Register at:
https://www.tenable.com/tenable-for-education/nessus-essentials

An activation code will be sent to your email.

### Step 2 — Download Nessus
```bash
wget https://www.tenable.com/downloads/api/v2/pages/nessus/files/Nessus-latest-debian10_amd64.deb
```

### Step 3 — Install Nessus
```bash
sudo dpkg -i Nessus-latest-debian10_amd64.deb
```

### Step 4 — Start Nessus
```bash
sudo systemctl start nessusd
sudo systemctl enable nessusd
```

### Step 5 — Access Nessus
Open Firefox and navigate to:
https://localhost:8834

Accept the security warning → Select **Nessus Essentials** → Enter
activation code → Create username and password → Wait for initialization.

---

## ✅ Setup Checklist

- [ ] Kali Linux VM running
- [ ] Metasploitable 2 VM running
- [ ] Both VMs on Host-Only Adapter
- [ ] Ping from Kali to Metasploitable successful
- [ ] Nessus installed and accessible at https://localhost:8834

---

> ➡️ Next: [02 — Reconnaissance](02-reconnaissance.md)