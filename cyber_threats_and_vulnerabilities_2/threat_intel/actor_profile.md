# APT29 Threat Actor Profile

## Overview
APT29 (Cozy Bear) is a nation‑state threat group known for intelligence collection operations.

## TTP Summary (MITRE)
| Tactic | Technique | Description |
|--------|-----------|-------------|
| Initial Access | Spearphishing Attachment | Weaponized macro documents |
| Persistence | Scheduled Task | Recurring C2 beacon |
| Privilege Escalation | Token Impersonation | Leveraging LSASS dump |
| C2 | HTTPS | Encrypted communication |
| Exfiltration | Cloud Storage | Using Azure blob |

## Campaign Details
- Target Sector: Government, Healthcare, R&D
- Goal: Credential theft, long‑term network persistence
