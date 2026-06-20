# 01 — Environment Setup

This section documents the environment setup required before conducting
the vulnerability assessment.

---

## 🖥️ Virtual Machines Required

| VM | Role | Network IP |
|---|---|---|
| Kali Linux | Attacker / Assessment Machine | 192.168.56.102 |
| Metasploitable 2 | Target / Vulnerable Machine | 192.168.56.103 |

---

## 🌐 Network Configuration

Both virtual machines are configured using **VirtualBox Host-Only Adapter**
to isolate the assessment environment from external networks.

### Steps to configure Host-Only Adapter:
1. Open **VirtualBox**
2. Select the VM → Click **Settings** → **Network**
3. Set **Adapter 1** to **Host-Only Adapter**
4. Repeat for both Kali Linux and Metasploitable 2

### Verify Connectivity
From Kali Linux, ping Metasploitable 2 to confirm network reachability:

```bash
ping [TARGET_IP]
```

**Expected output:**

---

## 🔧 Nessus Installation on Kali Linux

### Step 1 — Register for Nessus Essentials
Complete the registration form using a valid email address at:
https://www.tenable.com/tenable-for-education/nessus-essentials

An activation code will be sent to your email — save it for later.

### Step 2 — Download Nessus
```bash
wget https://www.tenable.com/downloads/api/v2/pages/nessus/files/Nessus-latest-debian10_amd64.deb
```

### Step 3 — Install Nessus
```bash
sudo dpkg -i Nessus-latest-debian10_amd64.deb
```

If dependency errors occur:
```bash
sudo apt --fix-broken install
```

### Step 4 — Start and Enable the Nessus Service
```bash
sudo systemctl start nessusd
sudo systemctl enable nessusd
```

### Step 5 — Verify Nessus is Running
```bash
sudo systemctl status nessusd
```

**Expected output:**
Active: active (running)

### Step 6 — Access Nessus in Browser
Open Firefox and navigate to:
https://localhost:8834

> ⚠️ A security warning will appear — click **Advanced** then **Continue**

### Step 7 — Complete Nessus Setup
1. Select **Nessus Essentials**
2. Click **Skip** when prompted to activate
3. Enter the activation code received via email
4. Create a username and password
5. Wait for Nessus to initialize (may take several minutes)

---

## ✅ Setup Checklist

- [ ] Kali Linux VM running
- [ ] Metasploitable 2 VM running
- [ ] Both VMs on Host-Only Adapter
- [ ] Ping from Kali to Metasploitable successful
- [ ] Nessus installed and running on Kali
- [ ] Nessus accessible at https://localhost:8834

---

> ➡️ Next: [02 — Reconnaissance](02-reconnaissance.md)