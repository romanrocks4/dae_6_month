# Incident Response & Security Monitoring

## Summary
This document describes the security monitoring setup and an incident response scenario for an **SMB exploitation attempt** against host **192.168.1.239**, based on Nmap scan results. The scenario demonstrates alert prioritization and response documentation.

**Evidence files:**  
- `239_baseline.nmap` / `239_baseline.xml`  
- `239_smb_info.txt`  
- `239_rdp_info.txt`  

---

## Security Monitoring Setup

**Monitoring goals**
- Detect suspicious SMB activity using baseline Nmap scan results.
- Identify unusual SMB access patterns for host **192.168.1.239**.

**Detection use case (simulated)**
- Based on Nmap and SMB service enumeration, the following conditions would indicate suspicious activity:  
  - Unexpected SMB connections from unknown hosts.  
  - SMB services exposed with weak configurations (e.g., message signing not required).  

**Alert prioritization**
- **High:** Unexpected SMB connections to critical hosts.  
- **Medium:** Repeated share enumeration or high-volume file access.  
- **Low:** Single, expected connections from known admin IPs.

---

## Incident Response Scenario — SMB exploitation attempt

**Scenario summary**
- **Date/time:** `2025-09-17T03:14:00Z`  
- **Trigger:** Suspicious SMB connection identified in Nmap/SMB scan results.  
- **Context:** SMB service on `192.168.1.239` exposed with message signing not required.  

### 1) Identification
- **What was observed:**  
  - Nmap scan: SMB open on `192.168.1.239`  
  - SMB info (`239_smb_info.txt`): message signing enabled but not required.  
- **Classification:** Confirmed potential intrusion attempt. Severity: **High**  

**Evidence:**  
- `239_baseline.nmap` / `239_baseline.xml`  
- `239_smb_info.txt`  

### 2) Containment
- Documented containment steps based on scan findings:  
  - Isolate host **192.168.1.239** for analysis.  
  - Record current SMB configuration and open ports for forensic purposes.  

**Evidence of actions:**  
- Nmap scan snapshots stored under `evidence/192.168.1.239/`  

### 3) Eradication
- Review SMB service configuration and network exposure.  
- No active exploit observed; planned remediation would include:  
  - Adjust SMB configuration (require signing, disable SMBv1).  

### 4) Recovery
- Confirm host configuration after analysis.  
- Validate no unexpected services remain open via follow-up Nmap scan.  

### 5) Lessons Learned
- Regular SMB service enumeration is critical to identify weak configurations.  
- Maintaining a pre-incident baseline allows for quick anomaly detection.  
- Documented configuration weaknesses guide future hardening and monitoring priorities.

---

## Evidence of Functionality
- **Nmap baseline:** `239_baseline.nmap`  
- **SMB service info:** `239_smb_info.txt`  
- **Follow-up scans:** `239_rdp_info.txt` (used to confirm host state)  

> Screenshots or log snippets can be placed under `evidence/` with timestamps for all scans.

---

## Post-Incident Reporting (template)
- **Incident ID:** IR-2025-09-17-001  
- **Start Time:** 2025-09-17T03:14:00Z  
- **Scope:** Host 192.168.1.239 examined; no active compromise detected.  
- **Root cause (summary):** SMB exposed with message signing not required.  
- **Remediation actions:** Documented in lessons learned.  
- **Attachments:** Nmap scan and SMB info files.
