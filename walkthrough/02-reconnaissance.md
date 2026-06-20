# 02 — Reconnaissance & Asset Discovery

This section documents the initial reconnaissance performed on the target
system using **Nmap** to identify open ports, running services, and the
operating system.

---

## 🎯 Objective

- Discover all open ports on the target system
- Identify running services and their versions
- Determine the target operating system
- Categorize assets based on criticality and risk

---

## 🔍 Nmap Scan

### Command Used
```bash
sudo nmap -sV -O [TARGET_IP]
```

### Flags Explained
| Flag | Purpose |
|---|---|
| `-sV` | Probe open ports to determine service/version info |
| `-O` | Enable OS detection |
| `sudo` | Required for OS fingerprinting |

---

## 📊 Scan Results

**Target:** 192.168.56.103  
**Host Status:** Up  
**OS Detected:** Linux 2.6.9 - 2.6.33 (Ubuntu 8.04 - End of Life)  
**Total Open Ports:** 23

PORT     STATE SERVICE     VERSION

21/tcp   open  ftp         vsftpd 2.3.4

22/tcp   open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1

23/tcp   open  telnet      Linux telnetd

25/tcp   open  smtp        Postfix smtpd

53/tcp   open  domain      ISC BIND 9.4.2

80/tcp   open  http        Apache httpd 2.2.8 (Ubuntu) DAV/2

111/tcp  open  rpcbind     2 (RPC #100000)

139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X

445/tcp  open  netbios-ssn Samba smbd 3.X - 4.X

512/tcp  open  exec        netkit-rsh rexecd

513/tcp  open  login       OpenBSD or Solaris rlogind

514/tcp  open  shell       Netkit rshd

1099/tcp open  java-rmi    GNU Classpath grmiregistry

1524/tcp open  bindshell   Metasploitable root shell

2049/tcp open  nfs         2-4 (RPC #100003)

2121/tcp open  ftp         ProFTPD 1.3.1

3306/tcp open  mysql       MySQL 5.0.51a-3ubuntu5

5432/tcp open  postgresql  PostgreSQL DB 8.3.0 - 8.3.7

5900/tcp open  vnc         VNC (protocol 3.3)

6000/tcp open  X11         (access denied)

6667/tcp open  irc         UnrealIRCd

8009/tcp open  ajp13       Apache Jserv (Protocol v1.3)

8180/tcp open  http        Apache Tomcat/Coyote JSP engine 1.1

---

## 📂 Asset Categorization

Assets were categorized based on their **criticality** and **exploitation risk**.

### 🔴 Critical Assets

| Port | Service | Version | Risk Reason |
|---|---|---|---|
| 21 | FTP | vsftpd 2.3.4 | Known backdoor — CVE-2011-2523 |
| 1524 | Bindshell | Metasploitable root shell | Open root shell — instant access |
| 3306 | MySQL | 5.0.51a | Weak/no authentication |
| 139/445 | Samba | 3.X-4.X | RCE via CVE-2007-2447 |
| 5432 | PostgreSQL | 8.3.0-8.3.7 | Default credentials |

### 🟠 High Risk Assets

| Port | Service | Version | Risk Reason |
|---|---|---|---|
| 22 | SSH | OpenSSH 4.7p1 | Outdated, root login enabled |
| 80 | HTTP | Apache 2.2.8 | Outdated, known CVEs |
| 8180 | HTTP | Apache Tomcat 1.1 | Outdated Tomcat engine |
| 6667 | IRC | UnrealIRCd | Known backdoor vulnerability |

### 🟡 Medium Risk Assets

| Port | Service | Risk Reason |
|---|---|---|
| 23 | Telnet | Transmits credentials in plaintext |
| 5900 | VNC | Protocol 3.3 — unencrypted, weak auth |
| 2121 | FTP | ProFTPD — secondary FTP, misconfiguration risk |
| 2049 | NFS | Often misconfigured, file exposure risk |
| 512-514 | rexec/rlogin/rsh | Legacy protocols, no encryption |

### 🔵 Low / Informational Assets

| Port | Service | Notes |
|---|---|---|
| 25 | SMTP | Postfix — lower exploitation risk |
| 53 | DNS | ISC BIND 9.4.2 — outdated |
| 111 | RPC | rpcbind — auxiliary service |
| 6000 | X11 | GUI exposure, access denied |
| 8009 | AJP13 | Apache Jserv backend connector |

---

## 🔑 Key Observations

- **23 open ports** represent an extremely large attack surface
- **Port 1524** (Metasploitable root shell) is a deliberate backdoor
  providing instant root access — highest possible risk
- The OS (**Ubuntu 8.04**) has been **End of Life since 2013**,
  meaning no security patches are available
- Multiple **legacy protocols** (Telnet, rlogin, rsh) transmit
  data in plaintext, exposing credentials to interception

---

> ➡️ Next: [03 — Nessus Scan](03-nessus-scan.md)
