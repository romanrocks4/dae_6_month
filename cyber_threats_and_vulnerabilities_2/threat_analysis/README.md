# Advanced Threat Analysis

## Executive Summary
This threat analysis examines a simulated enterprise network targeted by a sophisticated threat actor using multi‑stage intrusion techniques. The goal is to demonstrate the student’s mastery of malware analysis, packet forensics, log review, and threat modeling using MITRE ATT&CK.

## Scope
- Malware sample reverse engineering  
- PCAP forensic analysis  
- Log correlation  
- IOC extraction  
- MITRE mapping  
- Kill chain reconstruction  
- Threat model generation  

## Findings Overview
- An APT-level intrusion leveraged spear-phishing with a malicious payload exploiting CVE‑2023‑23397.
- Lateral movement performed via stolen NTLM credentials.
- Persistence was maintained through Scheduled Tasks and a malicious DLL sideload.
- Data exfiltration observed through HTTPS (port 443) to an external C2.
