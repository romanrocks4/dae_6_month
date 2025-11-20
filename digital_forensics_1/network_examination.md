# Network Forensics Examination Documentation

This file documents a simulated network forensics examination, including network traffic capture, log analysis, evidence collection, and timeline creation.

---

## 1. Overview

This document outlines the process of network forensics examination using Wireshark, LogParser, and Splunk. The investigation includes traffic capture, log analysis, browser history collection, and timeline reconstruction.

**Objectives:**

* Capture network traffic with proper filtering.
* Analyze system and network logs.
* Collect network-related evidence, including browser history and connection logs.
* Create a timeline of network activity.
* Correlate significant events and artifacts.

---

## 2. Environment Setup

**Test System:** Mac OS

* Host: Investigator Workstation
* Network: Isolated LAN
* Tools Installed:

  * Wireshark v4.1.2
  * LogParser v2.2
  * Splunk Enterprise v9.2.0

**Capture Setup:**

* Interface: `Ethernet 2`
* Capture Filter: `tcp port 80 or tcp port 443`
* Destination: `E:\Evidence\network_capture_20251119.pcapng`

---

## 3. Network Traffic Capture

**Step:** Capture network traffic using Wireshark.

**Actions Taken:**

1. Opened Wireshark and applied capture filter for HTTP and HTTPS traffic.
2. Captured live traffic for 60 minutes.
3. Saved capture to `network_capture_20251119.pcapng`.
4. Recorded timestamp, interface, and tool version.

**Capture Info:**

```
Wireshark v4.1.2
Interface: Ethernet 2
Filter: tcp port 80 or tcp port 443
Capture Duration: 60 minutes
Timestamp: 2025-11-19 11:00:00 - 12:00:00
```

**Justification:** Capturing relevant traffic allows analysis of potential malicious activity and user behavior.

---

## 4. Log Analysis

**Step:** Analyze system and network logs.

**Actions Taken:**

1. Imported Windows Event Logs into LogParser and Splunk.
2. Extracted logs related to network connections, login events, and browser activity.
3. Filtered logs for suspicious IP addresses and abnormal behavior.

**Log Entries:**

```
[INFO] 2025-11-19 11:10:12 - Connection to suspicious IP 192.168.1.105 detected
[INFO] 2025-11-19 11:25:33 - Browser history shows access to phishing site 'http://malicious.example.com'
[INFO] 2025-11-19 11:45:00 - Multiple failed login attempts logged
```

**Justification:** Logs provide insight into network activity, anomalies, and potential evidence of compromise.

---

## 5. Network Evidence Collection

**Step:** Collect network-related artifacts.

**Actions Taken:**

1. Extracted browser history files from user profiles (`History` and `Cookies`).
2. Collected system connection logs and DHCP leases.
3. Documented timestamps, source/destination IPs, and protocols.

**Example Collected Artifacts:**

* `Chrome_History_JohnDoe.sqlite`
* `Connections_20251119.csv`
* `DHCP_Leases_20251119.log`

**Justification:** Captured artifacts provide evidence of user network activity and potential malicious connections.

---

## 6. Timeline Creation

**Step:** Construct a timeline of network activity.

**Actions Taken:**

1. Compiled timestamps from packet captures, logs, and browser history.
2. Created a chronological view of events.
3. Highlighted significant events such as suspicious connections, phishing site access, and failed logins.

**Sample Timeline:**

| Timestamp        | Event Description                                                           |
| ---------------- | --------------------------------------------------------------------------- |
| 2025-11-19 11:10 | Connection to 192.168.1.105 initiated                                       |
| 2025-11-19 11:25 | User visited '[http://malicious.example.com](http://malicious.example.com)' |
| 2025-11-19 11:45 | Multiple failed login attempts detected                                     |
| 2025-11-19 11:50 | Connection to external IP 203.0.113.45 closed                               |

**Justification:** Timelines correlate network events to build a factual narrative of activity.

---

## 7. Packet Analysis

**Step:** Analyze captured packets.

**Actions Taken:**

1. Filtered HTTP and HTTPS traffic for anomalies.
2. Inspected packet headers, payloads, and destination IPs.
3. Documented suspicious patterns such as repeated connections to untrusted IPs.

**Example Packet Findings:**

```
[INFO] 2025-11-19 11:12:05 - HTTP GET request to http://malicious.example.com, User-Agent: Chrome/108.0
[INFO] 2025-11-19 11:40:33 - TLS handshake with IP 203.0.113.45, unexpected certificate detected
```

**Justification:** Packet inspection confirms suspicious activity and provides context for other artifacts.

---

## 8.Supporting Evidence

**Logs:**

```
[INFO] 2025-11-19 12:05:12 - Network capture saved: network_capture_20251119.pcapng
[INFO] 2025-11-19 12:10:30 - Browser history extracted: Chrome_History_JohnDoe.sqlite
[INFO] 2025-11-19 12:15:05 - Timeline of network events created successfully
```

---

## 9. Summary

This documentation simulates a complete network forensics examination, including:

* Capturing network traffic with Wireshark.
* Analyzing system and network logs using LogParser and Splunk.
* Collecting network artifacts including browser history and connection logs.
* Timeline creation and event correlation.
* Packet inspection and evidence documentation.

**Note:** All files, screenshots, and logs are simulated.
