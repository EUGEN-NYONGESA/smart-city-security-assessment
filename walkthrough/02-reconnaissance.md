# 02 — Reconnaissance & Asset Discovery

Initial reconnaissance performed using Nmap to identify open ports,
running services, and the operating system of the smart city server.

---

## 🎯 Objective

- Discover all open ports on the legacy smart city server
- Identify running services and their versions
- Determine the target OS
- Categorize assets by risk level and smart city impact

---

## 🔍 Nmap Scan

```bash
sudo nmap -sV -O 192.168.56.103
```

| Flag | Purpose |
|---|---|
| `-sV` | Detect service versions |
| `-O` | OS fingerprinting |
| `sudo` | Required for OS detection |

---

## 📊 Scan Results

**Target:** 192.168.56.103
**OS:** Linux 2.6.9 - 2.6.33 (Ubuntu 8.04 — End of Life since 2013)
**Open Ports:** 23
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

### 🔴 Critical Assets

| Port | Service | Version | Smart City Risk |
|---|---|---|---|
| 21 | FTP | vsftpd 2.3.4 | Backdoor — attacker uploads malicious traffic configs |
| 1524 | Bindshell | Root shell | Instant root access to city infrastructure server |
| 3306 | MySQL | 5.0.51a | City sensor and operational data exposed |
| 139/445 | Samba | 3.X-4.X | RCE — attacker pushes commands via city network shares |
| 5432 | PostgreSQL | 8.3.0-8.3.7 | Default credentials expose all city databases |
| 5900 | VNC | Protocol 3.3 | Attacker views and controls city monitoring dashboard |

### 🟠 High Risk Assets

| Port | Service | Version | Smart City Risk |
|---|---|---|---|
| 22 | SSH | OpenSSH 4.7p1 | Default credentials grant remote server admin access |
| 80 | HTTP | Apache 2.2.8 | City web monitoring interface exposed |
| 8180 | HTTP | Apache Tomcat 5.5 | Smart city application layer vulnerable |
| 6667 | IRC | UnrealIRCd | Backdoor — potential C2 channel for attackers |
| 2049 | NFS | 2-4 | Root filesystem exported to all network hosts |

### 🟡 Medium Risk Assets

| Port | Service | Risk |
|---|---|---|
| 23 | Telnet | Admin credentials sent in plaintext over city network |
| 512-514 | rexec/rlogin/rsh | Legacy unencrypted remote access |
| 2121 | ProFTPD | Secondary FTP misconfiguration risk |

### 🔵 Low / Informational

| Port | Service | Notes |
|---|---|---|
| 25 | SMTP | Postfix mail service |
| 53 | DNS | ISC BIND 9.4.2 — outdated |
| 111 | RPC | rpcbind — supports NFS |
| 1099 | Java RMI | Deserialization risk |
| 6000 | X11 | GUI exposure — access denied |
| 8009 | AJP13 | Apache Jserv backend |

---

## 🔑 Key Smart City Observations

- **23 open ports** on a server managing public safety infrastructure
  is a critical oversight — any one of them is a potential entry point
- **Port 1524** gives an attacker instant root control of traffic lights
  and streetlight systems with no credentials required
- **VNC on port 5900** lets an attacker view and manipulate the live
  city monitoring dashboard in real time
- **NFS root export** means all traffic schedules, sensor data, and
  city configurations are readable by any host on the network
- The OS (**Ubuntu 8.04**) has had no security patches since 2013

---

> ➡️ Next: [03 — Nessus Scan](03-nessus-scan.md)