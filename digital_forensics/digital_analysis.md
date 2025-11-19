# Digital Evidence Analysis Documentation

This file documents a simulated digital evidence analysis, following forensic methodology, artifact extraction, timeline creation, and deleted file recovery.

---

## 1. Overview

This document outlines the process of analyzing digital evidence to extract relevant artifacts, create a timeline of events, recover deleted files, and correlate findings to establish factual timelines.

**Objectives:**

* Extract file system artifacts using Autopsy and FTK.
* Create event timelines from file timestamps, registry entries, and logs.
* Recover deleted files using data carving tools (Scalpel, Foremost).
* Document findings with methodology explanations and evidence correlation.

---

## 2. Environment Setup

**Test System:** Mac OS

* Host: Investigator Workstation
* Network: Isolated LAN
* Tools Installed:

  * Autopsy v4.19.1
  * FTK v7.4.2
  * Scalpel v2.1.1
  * Foremost v1.5.7

**Evidence:**

* Disk image: `disk_image_20251119.E01`
* Memory image: `memory_20251119.raw`

**Write-Blocking:** All evidence mounted read-only.

---

## 3. Artifact Extraction

**Step:** Extract relevant artifacts using Autopsy.

**Actions Taken:**

1. Opened `disk_image_20251119.E01` in Autopsy.
2. Indexed file system and recovered metadata, including file creation, modification, and access timestamps.
3. Exported registry hives for analysis of user activity.
4. Extracted system and application logs.

**Extracted Artifacts:**

* `C:\Users\JohnDoe\Documents\suspicious_file.docx`
* `C:\Windows\System32\config\SYSTEM` (registry hive)
* `ApplicationLog.evtx`

**Justification:** Extracting artifacts is necessary to identify actions performed on the system and reconstruct events.

---

## 4. Timeline Creation

**Step:** Build a timeline of events.

**Actions Taken:**

1. Collected timestamps from files, registry entries, and logs.
2. Created a chronological timeline of significant actions.
3. Included recovered artifacts and system activity.

**Sample Timeline:**

| Timestamp        | Event Description                   |
| ---------------- | ----------------------------------- |
| 2025-11-18 08:32 | User created `suspicious_file.docx` |
| 2025-11-18 09:15 | USB device connected (USB1234)      |
| 2025-11-18 10:05 | File deleted: `confidential.xlsx`   |
| 2025-11-18 10:06 | Registry key modified: RecentDocs   |

**Justification:** Timelines help establish a factual sequence of events for the investigation.

---

## 5. Deleted File Recovery

**Step:** Recover deleted files using Scalpel and Foremost.

**Actions Taken:**

1. Ran Scalpel on the disk image to recover deleted `.docx` and `.xlsx` files.
2. Ran Foremost to recover additional deleted media and documents.
3. Verified recovered files and logged recovery timestamps.

**Example Recovered Files:**

* `recovered_confidential.xlsx` (Scalpel)
* `recovered_image.jpg` (Foremost)

**Justification:** Data carving recovers evidence that may not be visible in the current file system, crucial for establishing missing actions.

---

## 6. Artifact Correlation

**Step:** Correlate artifacts to reconstruct user and system activity.

**Actions Taken:**

1. Linked file creation/modification events to registry entries.
2. Correlated log entries with recovered files.
3. Established a consistent timeline demonstrating user actions, deletions, and USB activity.

**Correlation Log:**

```
[INFO] 2025-11-19 15:20:12 - suspicious_file.docx created; registry RecentDocs updated
[INFO] 2025-11-19 15:25:43 - USB device USB1234 inserted; confidential.xlsx deleted
[INFO] 2025-11-19 15:30:05 - recovered_confidential.xlsx verified using SHA-256: 2a1b3c4d5e6f7a8b9c0d1e2f3a4b5c6d
```

**Justification:** Artifact correlation allows a coherent reconstruction of events and validates findings.

---

## 7. Screenshots and Evidence

**Simulated Screenshots:**

* `autopsy_file_tree_20251119.png`
* `timeline_view_20251119.png`
* `recovery_results_20251119.png`

**Logs:**

```
[INFO] 2025-11-19 15:40:12 - Disk image loaded in Autopsy v4.19.1
[INFO] 2025-11-19 15:50:33 - Registry hive SYSTEM parsed
[INFO] 2025-11-19 16:00:05 - Deleted files recovered using Scalpel v2.1.1 and Foremost v1.5.7
```

---

## 8. Summary

This documentation simulates a complete digital evidence analysis process, including:

* Extraction of relevant file system and registry artifacts.
* Timeline creation from multiple evidence sources.
* Recovery of deleted files using data carving tools.
* Correlation of artifacts to establish factual timelines.
* Comprehensive logs and simulated screenshots.

**Note:** All files, logs, and screenshots are simulated for learning purposes.
