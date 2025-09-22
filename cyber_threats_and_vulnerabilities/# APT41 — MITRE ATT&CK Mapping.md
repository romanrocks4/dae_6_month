# APT41 — MITRE ATT&CK Mapping

## Group Overview
APT41 (also known as BARIUM, Wicked Panda, Brass Typhoon) is a Chinese threat actor active since at least 2012. It conducts both **state-sponsored espionage** and **financially motivated operations**. Targets include governments, healthcare, telecom, education, video game companies, and software supply chains. [MITRE ATT&CK — APT41](https://attack.mitre.org/groups/G0096/)

---

## Representative MITRE ATT&CK Mapping

| Tactic | Technique (ATT&CK ID) | Observed Use / Evidence |
|---|---:|---|
| Initial Access | Exploit Public-Facing Application — **T1190** | Exploited vulnerabilities in Internet-facing web apps (ASP.NET deserialization, SQL injection, directory traversal) to gain access. [Google Threat Intel](https://cloud.google.com/blog/topics/threat-intelligence/apt41-us-state-governments) |
| Initial Access | Supply Chain Compromise — **T1195** | Inserted backdoors or malicious code in legitimate software for wider distribution. [Resecurity Report](https://www.resecurity.com/blog/article/apt-41-threat-intelligence-report-and-malware-analysis) |
| Execution | Command & Scripting Interpreter — **T1059** (PowerShell, scripts) | Launched post-exploitation tools and malware payloads using interpreters. [Resecurity Report](https://www.resecurity.com/blog/article/apt-41-threat-intelligence-report-and-malware-analysis) |
| Persistence | Bootkit / UEFI Rootkit — **T1547.003** | Used *MoonBounce* UEFI firmware implant to persist through reboots and bypass defenses. [MITRE Profile](https://attack.mitre.org/groups/G0096/) |
| Defense Evasion | Obfuscated Files or Information — **T1027** | Employed packers, custom malware, and steganography to avoid detection. [Resecurity Report](https://www.resecurity.com/blog/article/apt-41-threat-intelligence-report-and-malware-analysis) |
| Credential Access | Credential Dumping — **T1003** | Used tools like Mimikatz to obtain credentials for lateral movement. [Google Threat Intel](https://cloud.google.com/blog/topics/threat-intelligence/apt41-us-state-governments) |
| Discovery | Network Service Scanning — **T1046** | Scanned internal systems/databases for lateral movement and exfiltration targets. [MITRE Campaign C0040](https://attack.mitre.org/campaigns/C0040/) |
| Command & Control | Application Layer Protocol — **T1071.001** (HTTPS) | Used HTTPS for command-and-control traffic to blend with normal web activity. [MITRE Campaign C0040](https://attack.mitre.org/campaigns/C0040/) |
| Exfiltration | Archive Collected Data — **T1560.001** | Compressed (RAR) sensitive files before exfiltrating them. [MITRE Campaign C0040](https://attack.mitre.org/campaigns/C0040/) |

---

## Detection & Mitigation

- Apply regular patching of public-facing applications (frameworks, plugins).  
- Enforce supply chain security (code signing, vendor verification, monitoring).  
- Enable firmware integrity checking to detect UEFI/bootkit implants.  
- Monitor PowerShell and scripting activity (enable ScriptBlock logging, hunt for encoded commands).  
- Detect credential dumping (LSASS access, suspicious tooling).  
- Restrict outbound protocols; monitor anomalous HTTPS connections.  
- Apply least-privilege, enforce MFA, and rotate credentials after incidents.  

---

## References
- [MITRE ATT&CK Group Profile: APT41 (G0096)](https://attack.mitre.org/groups/G0096/)  
- [Google Threat Intelligence: APT41 State Government Intrusions](https://cloud.google.com/blog/topics/threat-intelligence/apt41-us-state-governments)  
- [Resecurity APT41 Threat Intelligence Report](https://www.resecurity.com/blog/article/apt-41-threat-intelligence-report-and-malware-analysis)  
- [MITRE ATT&CK Campaign: APT41 DUST (C0040)](https://attack.mitre.org/campaigns/C0040/)  
- [MoonBounce UEFI Malware](https://en.wikipedia.org/wiki/MoonBounce)  
