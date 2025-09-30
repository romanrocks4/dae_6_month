# Risk Management

## Summary
This Risk Management document summarizes critical risks identified from the vulnerability/asset discovery scans performed against host **192.168.1.239** on **Tue Sep 16 2025**. All scan outputs are included as evidence files: `239_baseline.nmap` / `239_baseline.xml`, `239_rdp_info.txt`, and `239_smb_info.txt`.

## Risk Identification
Based on the results of the Nmap scans (see evidence files above), the following two critical risks were identified:

### Risk 1
- **Vulnerability Name/ID:** Exposed SMB / Microsoft-DS and NetBIOS services (ports 445 & 139).  
- **Description:** Nmap shows ports **139/tcp (netbios-ssn)** and **445/tcp (microsoft-ds)** open on 192.168.1.239. SMB2 security indicates *message signing enabled but not required* (smb2-security-mode), which weakens integrity guarantees. Open SMB services can expose file shares, user information, and allow SMB-based exploits if an exploitable service/version exists.  
- **Evidence (scan output):**  
  - From `239_baseline.nmap` / XML: `139/tcp open netbios-ssn`, `445/tcp open microsoft-ds`.  
  - From `239_smb_info.txt`: `smb2-security-mode: Message signing enabled but not required`.  
- **Potential Impact:** An attacker on the network could enumerate SMB shares, access improperly protected files, and — if host is vulnerable to known SMB exploits — gain remote code execution or lateral movement capability. This poses a high risk of data exfiltration and compromise of other assets.  
- **CVSS Score (indicative):** 9.8 (Critical) for SMB remote code execution class vulnerabilities (e.g., EternalBlue class CVEs) — treat as high-critical until the host is validated/patched.

### Risk 2
- **Vulnerability Name/ID:** Exposed RDP (Remote Desktop) service (port 3389).  
- **Description:** Nmap shows **3389/tcp open ms-wbt-server (Microsoft Terminal Services)** on 192.168.1.239. `rdp-ntlm-info` reveals the hostname `WIN-FVANFN2P7CG` and `Product_Version: 10.0.19041`. RDP exposure to internal (or external) networks enables brute-force, credential-stuffing, and exploitation of RDP-specific vulnerabilities if present.  
- **Evidence (scan output):**  
  - From `239_baseline.nmap` / XML: `3389/tcp open ms-wbt-server`.  
  - From `239_rdp_info.txt` (rdp-ntlm-info): `Target_Name: WIN-FVANFN2P7CG`, `Product_Version: 10.0.19041`. RDP security layer tests returned CredSSP (NLA) SUCCESS.  
- **Potential Impact:** Remote attacker could gain unauthorized interactive access, elevate privileges, pivot internally, or perform ransomware deployment if credentials are compromised or the host is vulnerable. RDP is a common initial access vector and should be tightly controlled.  
- **CVSS Score (indicative):** High (7.0–9.0) for many RDP-related remote code execution or authentication bypass vulnerabilities depending on specific CVE.

---

## Risk Treatment & Mitigation

### Risk 1 – Exposed SMB / microsoft-ds (ports 139/445)
- **Recommendation:**  
  1. Restrict SMB access to only authorized internal subnets (apply firewall rules to block SMB from untrusted networks).  
  2. Enforce SMB signing (require message signing) and disable SMBv1 if still enabled.  
  3. Audit SMB shares and permissions; remove or lock down any guest/anonymous shares.  
  4. Ensure host is fully patched with the latest Windows updates.  
  5. If SMB must be remotely accessible, require access via VPN or other authenticated tunnels only.  
- **Mitigation Steps (planned / in-progress):**  
  - Conducted SMB enumeration and verified `message signing enabled but not required`. (Evidence: `239_smb_info.txt`)  
  - Planned: Disable SMBv1, set policy to *require* SMB signing, and restrict port 445/139 at perimeter and host firewall to authorized ranges.  
- **Mitigation Status:** In Progress

### Risk 2 – Exposed RDP (port 3389)
- **Recommendation:**  
  1. Remove direct RDP exposure to untrusted networks. Enforce access through VPN or jump host.  
  2. Enforce Network Level Authentication (NLA) and strong authentication policies (complex passwords + MFA where possible).  
  3. Implement account lockout policies and monitoring for RDP auth failures.  
  4. Apply latest Windows patches for the `10.0.19041` image and verify no public RDP CVEs are unpatched.  
  5. Consider limiting RDP to specific management IPs via firewall rules or moving RDP off the default port only as a temporary obfuscation (not a true mitigation).  
- **Mitigation Steps (planned / in-progress):**  
  - Verified NLA/CredSSP success via `rdp-ntlm-info` (evidence: `239_rdp_info.txt`).  
  - Planned: Restrict RDP via firewall to management subnet, enable MFA for remote desktop authentication where possible, and review event logs for brute-force attempts.  
- **Mitigation Status:** In Progress

---

## Risk Monitoring Procedure
To ensure ongoing tracking and re-evaluation of the risks above, the following procedure will be used:

| Risk ID | Vulnerability                                | Risk Level | Mitigation Status | Next Review Date | Responsible Party |
|---------|----------------------------------------------|------------|-------------------|------------------|-------------------|
| 1       | SMB (ports 139/445) — message signing weak   | Critical   | In Progress       | 2025-10-16       | Roman Shubin      |
| 2       | RDP (port 3389) exposed                       | Critical   | In Progress       | 2025-10-16       | Roman Shubin      |

**Monitoring activities & cadence**
- **Weekly**: Review host logs (Windows Event Viewer) for repeated authentication failures or suspicious SMB/RDP activity.  
- **Monthly**: Re-run targeted Nmap scan (same options used originally) against 192.168.1.239 and compare results to baseline. Save new output as `239_baseline_followup_<YYYYMMDD>.nmap`.  
- **Immediately**: If any new critical vulnerabilities are discovered (via patch alerts or vendor advisories), trigger an ad-hoc review and adjust mitigation priority.

**Detection & Alerting**
- Add IDS/host-based rules to detect:
  - Unusual SMB session creation or file access volumes.
  - Repeated RDP authentication failures from the same source IP.
  - New listening services or changed service banners on 192.168.1.239.

---

## Evidence & References
- Nmap baseline scan: `239_baseline.nmap` / `239_baseline.xml` — performed Tue Sep 16 2025, shows ports 135, 139, 445, 3389 open.  
- RDP detail script output: `239_rdp_info.txt` — contains `rdp-ntlm-info` and `rdp-enum-encryption` results (Product_Version: 10.0.19041).  
- SMB scripts output: `239_smb_info.txt` — shows `smb2-security-mode` with message signing enabled but not required.  
- (Optional) Attach screenshots of scan output or paste the key snippets under an `evidence/` folder in your repo.

---

## Notes & Next Steps
1. **Immediate action:** Restrict external access to ports 445 and 3389 at the perimeter. Require management access via VPN only.  
2. **Hardening:** Enforce SMB signing, disable SMBv1 if present, and apply Windows updates for `10.0.19041`.  
3. **Verification:** After mitigation steps, re-run the same Nmap commands and update the monitoring table to `Mitigated` once confirmed.  
4. **Documentation:** Add remediation logs (commands run, patch KB numbers, firewall rules applied) to the project repository for traceability.

