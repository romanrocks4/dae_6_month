# Vulnerability Management Program

## Methodology
This section demonstrates a full vulnerability management lifecycle following NIST 800‑40r4.

### Steps:
1. Asset Discovery (Nmap + OpenVAS)
2. Vulnerability Scanning
3. Prioritization Using CVSS + Threat Context
4. Patch Planning
5. Remediation & Verification

## High Severity Findings
| CVE | Service | Severity | Description | Fix |
|----|---------|----------|-------------|-----|
| CVE‑2024‑3094 | SSH | 10.0 | XZ backdoor vulnerability | Update to patched XZ version |
| CVE‑2023‑34362 | MOVEit | 9.8 | SQL injection leading to RCE | Apply patch from vendor |
| CVE‑2021‑44228 | Log4j | 10.0 | Remote code execution | Remove vulnerable jars |

## Risk Prioritization
Risk = CVSS × Threat Likelihood × Asset Value  
Critical assets receive immediate remediation within 48 hours.
