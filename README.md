<div align="center">

![Footprinting and Network Scanning: Penetration Testing Report, Week 2](assets/banner.png)

![Kali Linux](https://img.shields.io/badge/Kali%20Linux-2026.3-557C94?style=for-the-badge&logo=kalilinux&logoColor=white)
![Nmap](https://img.shields.io/badge/Nmap-7.99-404040?style=for-the-badge)
![Phases](https://img.shields.io/badge/Phases-1%20%26%202-14B8A6?style=for-the-badge)
![Scope](https://img.shields.io/badge/Scope-Authorized%20targets%20only-2EA043?style=for-the-badge)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Karibwende%20Blair-0A66C2?style=for-the-badge)](https://www.linkedin.com/in/karibwende-blair-088012287)

</div>

# Penetration Testing Report: Footprinting and Network Scanning

**W2-PM-FINAL | Cybersecurity | Networkwalks**

| Field | Detail |
| --- | --- |
| **Pentester** | Karibwende Blair |
| **Program** | Networkwalks Cybersecurity Internship |
| **Date of testing** | 12 November 2026 |
| **Modules completed** | W2-PM1 (footprinting with multiple Kali tools), W2-PM5 (Zenmap network scanning) |
| **Targets** | 1. `networkwalks.com` (public website and DNS records)<br>2. My own local network (`192.168.1.0/24`) |
| **Authorization** | Networkwalks Letter of Authorization for cybersecurity testing |
| **Phases covered** | **Phase 1:** Reconnaissance and footprinting<br>**Phase 2:** Scanning and network discovery |
| **Test environment** | Kali Linux 2026.3 (VirtualBox 7.2.6 VM) on an Ubuntu 26.04.1 host |

---

## Executive summary

I footprinted the public domain `networkwalks.com` with command-line reconnaissance tools, then scanned my own local network with Zenmap to discover live hosts and draw a network topology. No exploitation, brute forcing, or service disruption took place. Everything in this report was collected through passive or light information gathering and host discovery.

| Area | Key result |
| --- | --- |
| **Domain registration** | Registered through GoDaddy on 6 Nov 2019, expires 6 Nov 2027. Four registrar lock statuses set. DNSSEC unsigned. |
| **DNS hosting** | Name servers `NS6135.HOSTGATOR.COM` and `NS6136.HOSTGATOR.COM` |
| **Web stack** | Apache, WordPress 7.1.4, WordPress Download Manager 3.3.76, jQuery 3.7.1 |
| **Server address** | `192.232.216.135` (consistent across WhatWeb and nslookup) |
| **Web protection** | Protected by a ModSecurity (SpiderLabs) web application firewall |
| **Local network** | 8 live hosts found among 256 addresses on `192.168.1.0/24`, in 18.99 seconds |

> [!NOTE]
> The findings below are **observations from information gathering, not confirmed vulnerabilities**. See [Limitations](#8-limitations).

## Contents

1. [Liability disclaimer](#1-liability-disclaimer)
2. [Scope and authorization](#2-scope-and-authorization)
3. [Environment and tools](#3-environment-and-tools)
4. [Phase 1: Footprinting and reconnaissance](#4-phase-1-footprinting-and-reconnaissance)
5. [Phase 2: Network scanning with Zenmap](#5-phase-2-network-scanning-with-zenmap)
6. [Risk analysis](#6-risk-analysis)
7. [Recommendations](#7-recommendations)
8. [Limitations](#8-limitations)
9. [Conclusion](#9-conclusion)
10. [Command log](#10-command-log)

---

## 1. Liability disclaimer

I carried out these activities only against systems I was authorized in writing to test, or that I own. This material is for education and research. Do not use anything in this repository against a system you do not own or have explicit permission to test. Unauthorized access is a crime in most countries, even when no damage is done, and every action you take is your own responsibility. The author and Networkwalks are not responsible for misuse of this information.

## 2. Scope and authorization

Testing was limited to the targets and activities named in the Networkwalks Letter of Authorization.

| Target | Basis for permission |
| --- | --- |
| `networkwalks.com` and its DNS records | Owned by Networkwalks, authorized in writing |
| My own local network (`192.168.1.0/24`) | Network I own and control |

| Permitted | Not permitted |
| --- | --- |
| Footprinting with passive or light tools (`whois`, `whatweb`, `nslookup`, `curl`, `wafw00f`, `dnsrecon`) | Exploitation, unauthorized access, or privilege escalation |
| Host discovery with an Nmap or Zenmap ping scan of my own subnet | Denial of service, brute force, or password attacks |
| | Accessing, copying, changing, or deleting any data |
| | Social engineering, or testing anything outside the scope above |

## 3. Environment and tools

All commands were run from a Kali Linux 2026.3 virtual machine. For Phase 2 the VM was connected to my local network so that it could reach `192.168.1.0/24`.

| Tool | Purpose |
| --- | --- |
| **WHOIS** | Domain registration details: registrar, dates, name servers |
| **WhatWeb** | Fingerprint web technologies: server, CMS, plugins, IP |
| **nslookup** | Resolve the domain name to an IP address through DNS |
| **curl -I** | Read the HTTP response headers without downloading the page |
| **wafw00f** (v2.4.2) | Detect whether a web application firewall protects the site |
| **Zenmap** (Nmap 7.99) | Discover live hosts on the local subnet and draw the topology |

---

## 4. Phase 1: Footprinting and reconnaissance

**Target:** `networkwalks.com`. Only passive and light information-gathering commands were used.

### 4.1 WHOIS

**Goal:** find out who registered the domain, when, and which name servers it uses.

```bash
whois networkwalks.com
```

![WHOIS output for networkwalks.com](screenshots/01-whois.png)
*Figure 1. WHOIS record for networkwalks.com.*

**Observations**

- Registrar: GoDaddy.com, LLC (IANA ID 146)
- Created 6 November 2019, last updated 12 November 2025, expires 6 November 2027
- Four client lock statuses set: delete, renew, transfer, and update prohibited
- Name servers: `NS6135.HOSTGATOR.COM` and `NS6136.HOSTGATOR.COM`
- DNSSEC: unsigned

**Why it matters:** the record shows who manages the domain and where DNS is hosted, which tells an attacker whose accounts and services matter. The registrar locks are a good control, since they make unauthorized domain transfers harder.

### 4.2 WhatWeb

**Goal:** fingerprint the technologies behind the website.

```bash
whatweb networkwalks.com
```

![WhatWeb output for networkwalks.com](screenshots/02-whatweb.png)
*Figure 2. WhatWeb fingerprint of the site.*

**Observations**

- `http://networkwalks.com` returns `301 Moved Permanently` and redirects to HTTPS
- The HTTPS site answers `200 OK` from an **Apache** server at `192.232.216.135`
- Software exposed in the page metadata: **WordPress 7.1.4** and **WordPress Download Manager 3.3.76**
- Other technologies: jQuery 3.7.1, Google Tag Manager, HTML5
- A public contact address, `info@networkwalks.com`, appears on the page
- Cookie `__wpdm_client` is marked HttpOnly
- WhatWeb also reported Bootstrap 7.1.4, which is identical to the WordPress version string. I treat that as a probable fingerprinting false positive and do not rely on it.

**Why it matters:** exact CMS and plugin versions let an attacker look up known weaknesses for that software, which is why version information is often hidden.

### 4.3 nslookup

**Goal:** turn the domain name into an IP address.

```bash
nslookup networkwalks.com
```

![nslookup output for networkwalks.com](screenshots/03-nslookup.png)
*Figure 3. DNS resolution through 8.8.8.8.*

**Observations**

- `networkwalks.com` resolves to `192.232.216.135` (non-authoritative answer from `8.8.8.8`)
- This matches the IP address WhatWeb reported

**Why it matters:** the IP address is the network location of the service and the starting point for any further scanning, within an authorized scope.

### 4.4 curl (HTTP headers)

**Goal:** read the response headers. The `-I` option sends a HEAD request.

```bash
curl -I https://networkwalks.com
```

![curl header output for networkwalks.com](screenshots/04-curl.png)
*Figure 4. HTTP response headers.*

**Observations**

- `HTTP/1.1 200 OK` from an **Apache** server
- A `Link` header discloses the WordPress REST API at `/wp-json/`
- `X-Endurance-Cache-Level` and `X-nginx-cache: WordPress` headers reveal the hosting and caching layer
- A `Permissions-Policy` header is set, and the cookie carries the `Secure` and `HttpOnly` flags
- In the captured output, I did not see `Strict-Transport-Security`, `Content-Security-Policy`, `X-Frame-Options`, or `X-Content-Type-Options`

**Why it matters:** headers confirm the software stack and show which browser protections the site enforces. Several common hardening headers were not present.

### 4.5 wafw00f

**Goal:** detect whether a web application firewall (WAF) sits in front of the site.

```bash
wafw00f networkwalks.com
```

![wafw00f output for networkwalks.com](screenshots/05-wafw00f.png)
*Figure 5. WAF detection result.*

**Observations**

- The site is behind **ModSecurity (SpiderLabs)**
- Detection took only 2 requests

**Why it matters:** knowing the WAF product tells an attacker what filtering to expect. For the defender, a WAF is a positive control.

<!-- DNSRECON: paste section 4.6 from dnsrecon-snippet.md here -->

---

## 5. Phase 2: Network scanning with Zenmap

**Scope:** my own local network only. This phase was **host discovery**, not port scanning.

### 5.1 Scan configuration

In Zenmap I entered the target `192.168.1.0/24` and selected the **Ping scan** profile. Zenmap runs this Nmap command:

```bash
nmap -sn 192.168.1.0/24
```

The `-sn` option means "host discovery only": Nmap checks which addresses answer and does **not** scan ports. `/24` covers all 256 addresses in the subnet.

### 5.2 Results

The scan started at 17:02 (UTC−05:00) on 12 November 2026 and completed in **18.99 seconds**, checking **256 IP addresses** and finding **8 hosts up**.

![Zenmap ping scan results](screenshots/07-zenmap-ping-scan.png)
*Figure 6. Zenmap Nmap output (the last three bytes of each MAC address are redacted for privacy).*

| IP address | Hostname | MAC prefix | Vendor | Latency | Note |
| --- | --- | --- | --- | --- | --- |
| 192.168.1.64 | none | `6C:22:1A` | AltoBeam | 0.45 s | |
| 192.168.1.65 | none | `88:54:1F` | Google | 0.72 s | |
| 192.168.1.67 | none | `7A:4D:90` | Unknown | 0.71 s | Randomized MAC |
| 192.168.1.68 | none | `DE:22:77` | Unknown | 0.60 s | Randomized MAC |
| 192.168.1.69 | none | `F6:09:D7` | Unknown | 0.81 s | Randomized MAC |
| 192.168.1.73 | none | `34:2E:B7` | Intel Corporate | 0.0005 s | Very low latency, likely my VM host |
| 192.168.1.254 | `dsldevice.lan` | `50:1B:32` | Taicang T&W Electronics | 0.054 s | Likely the DSL router and gateway |
| 192.168.1.78 | none | not shown | not shown | not shown | My scanning machine |

**Reading the results**

- Nmap does not print a MAC address for the machine it runs on, which explains why `192.168.1.78` has none.
- Three hosts show no vendor. Their first byte (`7A`, `DE`, `F6`) has the "locally administered" bit set, which is typical of phones and other devices that use randomized private Wi-Fi addresses. A missing vendor name here is expected and is not a sign of anything unusual.
- The router and host identifications are inferences from the hostname, vendor, and latency, not confirmed by further testing.

### 5.3 Network topology

I opened the **Topology** tab, enabled the legend, and used **Save Graphic** to export the diagram. The scanning machine sits at the centre as `localhost`, with the eight discovered hosts around it.

![Zenmap network topology](screenshots/08-zenmap-topology.png)
*Figure 7. Zenmap topology of 192.168.1.0/24.*

**Why it matters:** host discovery is the first step of internal reconnaissance. An attacker uses the list to decide which hosts to examine next. A defender runs the same scan to confirm that only expected devices are on the network.

---

## 6. Risk analysis

| # | Observation | Evidence | Potential impact | Risk |
| :-: | --- | --- | --- | :-: |
| 1 | CMS and plugin versions exposed | WhatWeb: WordPress 7.1.4, WordPress Download Manager 3.3.76 | Exact versions make it easy to look up known weaknesses for that software | 🟠 Medium |
| 2 | WordPress REST API advertised | curl: `Link` header pointing to `/wp-json/` | Helps with fingerprinting and enumeration | 🟢 Low |
| 3 | Server IP address identifiable | nslookup: `192.232.216.135` | Reveals the network location of the service | 🟢 Low |
| 4 | WAF product identifiable | wafw00f: ModSecurity (SpiderLabs) | Shows which filtering to expect. The WAF itself is a positive control | 🟢 Low |
| 5 | Common security headers not observed | curl: no HSTS, CSP, X-Frame-Options, or X-Content-Type-Options in the captured output | Weaker browser-side protection against some web attacks | 🟢 Low |
| 6 | DNSSEC not enabled | WHOIS: `DNSSEC: unsigned` | DNS answers cannot be cryptographically validated | 🟢 Low |
| 7 | Public contact email on the home page | WhatWeb: `info@networkwalks.com` | A target for spam and phishing | 🟢 Low |
| 8 | Several devices visible on the local network | Zenmap: 8 live hosts, 3 with randomized MACs | Unknown devices would be easy to miss without an inventory | 🟢 Low |

**Positive controls observed:** HTTP redirects to HTTPS, a ModSecurity WAF is in place, registrar locks are set, a `Permissions-Policy` header is present, and the session cookie uses the `Secure` and `HttpOnly` flags.

## 7. Recommendations

1. **Reduce exposed version information.** Remove or hide the generator metadata that reveals CMS and plugin versions.
2. **Keep software updated.** Update WordPress core and plugins promptly, and review security advisories for them.
3. **Limit REST API exposure** where it is not needed, and remove the discovery header if it is unnecessary.
4. **Add security headers:** `Strict-Transport-Security`, `Content-Security-Policy`, `X-Frame-Options`, and `X-Content-Type-Options`.
5. **Consider DNSSEC** for the domain, if the DNS host supports it.
6. **Keep the WAF enabled and tuned.** ModSecurity is already in place and should stay current.
7. **Protect the contact address** with a form or obfuscation to reduce harvesting.
8. **Inventory the local network.** Run host discovery regularly, and investigate any device that is not recognized.
9. **Always test with authorization,** and stay inside the written scope.

## 8. Limitations

- This was information gathering and host discovery only. **No vulnerability was validated or exploited.**
- Version strings come from tool fingerprints and page metadata. They can be wrong or deliberately misleading, and a version number alone does not mean a system is vulnerable.
- The results are a snapshot of one moment on 12 November 2026.
- A ping scan finds only hosts that respond to host-discovery probes. A device that ignores them would not appear.
- Further security testing would need separate, explicit authorization.

## 9. Conclusion

This exercise showed how much can be learned about a target from public information and simple network responses, before any exploitation is attempted. Each tool answered a different question: who owns the domain, what software runs the site, where it lives, what the server reveals about itself, and what protects it. Scanning my own network showed the same principle from the inside: one ping scan produced a complete list of devices and a topology.

I also learned that the value of a finding depends on how it is reported. A good report states what was done, what was found, what it means, how risky it is, and how to fix it, and it keeps observations separate from confirmed vulnerabilities. Above all, reconnaissance and scanning are only appropriate inside a clearly authorized scope.

## 10. Command log

Times are in the VM's local time (UTC−05:00).

| Time | Phase | Command | Evidence |
| --- | --- | --- | --- |
| 16:33 | 1 | `whois networkwalks.com` | Figure 1 |
| 16:36 | 1 | `whatweb networkwalks.com` | Figure 2 |
| 16:37 | 1 | `nslookup networkwalks.com` | Figure 3 |
| 16:39 | 1 | `curl -I https://networkwalks.com` | Figure 4 |
| 16:41 | 1 | `wafw00f networkwalks.com` | Figure 5 |
| 17:02 | 2 | `nmap -sn 192.168.1.0/24` (Zenmap, Ping scan profile) | Figure 6 |
| 17:06 | 2 | Zenmap topology view | Figure 7 |

---

## Repository structure

```
.
├── README.md
├── assets/
│   └── banner.png
├── screenshots/
│   ├── 01-whois.png
│   ├── 02-whatweb.png
│   ├── 03-nslookup.png
│   ├── 04-curl.png
│   ├── 05-wafw00f.png
│   ├── 07-zenmap-ping-scan.png
│   └── 08-zenmap-topology.png
└── tools/                      # optional helper scripts
```

## Author

**Karibwende Blair** · [LinkedIn](https://www.linkedin.com/in/karibwende-blair-088012287)

<sub>Educational use only. Activities were limited to systems I own or was authorized in writing to test.</sub>
