# Setup Guide

This program automates a vulnerability assessment, but it relies on a few
tools being installed and running first. Follow this guide before running
the program.

---

## Prerequisites Overview

| Requirement | Where it runs | Purpose |
|---|---|---|
| Python 3.8+ | Assessment machine | Runs this program |
| Nmap | Assessment machine | Network reconnaissance |
| Nessus Essentials | Assessment machine | Vulnerability scanning |
| Network access to target | — | The target must be reachable |

---

## 1. Install Python Dependencies

From inside the `scanner/` folder, install the required Python libraries:

```bash
pip install -r requirements.txt
```

---

## 2. Install Nmap

On Kali Linux, Nmap is usually pre-installed. To confirm or install:

```bash
sudo apt update
sudo apt install nmap -y
nmap --version
```

---

## 3. Install and Set Up Nessus Essentials

The program connects to Nessus through its API, so Nessus must be
installed, running, and initialized first.

### Step 1 — Register for an Activation Code
Complete the form using a valid email address at:
https://www.tenable.com/tenable-for-education/nessus-essentials?edu=true

The activation code is sent to the email used during registration.
Keep it — you will need it during initialization.

### Step 2 — Download Nessus
```bash
wget https://www.tenable.com/downloads/api/v2/pages/nessus/files/Nessus-latest-debian10_amd64.deb
```

### Step 3 — Install Nessus
```bash
sudo dpkg -i Nessus-latest-debian10_amd64.deb
```

If you encounter dependency errors, resolve them with:
```bash
sudo apt --fix-broken install
```

### Step 4 — Start and Enable the Nessus Service
```bash
sudo systemctl start nessusd
sudo systemctl enable nessusd
```

### Step 5 — Confirm Nessus Is Running
```bash
sudo systemctl status nessusd
```
If active, you will see a running service confirmation.

### Step 6 — Access Nessus in the Browser
Open Firefox and navigate to:
https://localhost:8834

Be sure to use HTTPS. A security warning will appear instead of Nessus.
Choose **Advanced**, then **Continue**.

### Step 7 — Initialize Nessus
1. Wait for the initializing screen to finish.
2. When prompted for an installation type, choose **Nessus Essentials**.
3. Choose **Skip** when prompted to activate, then enter the activation
   code sent to your email.
4. Create a username and password, and record them for later.
5. Wait for Nessus to download its plugins (this can take a while on
   first setup).

---

## 4. Generate Nessus API Keys

This program authenticates to Nessus using API keys, not your username
and password. To generate them:

1. Log in to Nessus at `https://localhost:8834`
2. Click your profile icon (top right) and go to **My Account**
3. Open the **API Keys** tab
4. Click **Generate** — this produces an **Access Key** and a **Secret Key**
5. Copy both immediately and keep them safe; the secret key is shown only once

When you run the program, it will ask you for these two keys.

> ⚠️ Generating new API keys invalidates any previous ones.

---

## 5. Verify Everything Is Ready

Before running the program, confirm:

- [ ] Python dependencies installed (`pip install -r requirements.txt`)
- [ ] Nmap installed and working (`nmap --version`)
- [ ] Nessus service running (`sudo systemctl status nessusd`)
- [ ] Nessus accessible at `https://localhost:8834`
- [ ] Nessus API keys generated and saved
- [ ] The target system is running and reachable (try `ping <target_ip>`)

Once all boxes are checked, you are ready to run the program.

See [USAGE.md](USAGE.md) for how to run it.