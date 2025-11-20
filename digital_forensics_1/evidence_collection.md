# Evidence Collection & Preservation Documentation

This file documents the simulated collection and preservation of digital evidence from a running system, following best practices and forensic methodology.

---

## 1. Overview

This document outlines the evidence collection and preservation process, including disk imaging, memory acquisition, hash validation, and the use of write-blocking mechanisms. All steps are timestamped and documented to ensure integrity and reproducibility.

**Objectives:**

* Capture live data using FTK Imager and DumpIt.
* Create verified disk images with MD5 and SHA-1 hashes.
* Acquire system memory safely.
* Document tool versions, commands, timestamps, and hash verification.
* Ensure evidence integrity using write-blocking mechanisms.

---

## 2. Environment Setup

**Test System:** Mac OS

* Host: Investigator Workstation
* Network: Isolated LAN
* Tools Installed:

  * FTK Imager v4.5.1.3
  * DumpIt v1.9.0

**Write-Blocking:**

* Hardware write-blocker simulated for disk imaging.
* Read-only mounting enforced for all collected images.

---

## 3. Disk Image Acquisition

**Step:** Capture the system's disk image using FTK Imager.

**Actions Taken:**

1. Opened FTK Imager and selected source drive: `C:\`.
2. Selected destination: `E:\Evidence\disk_image_20251119.E01`.
3. Enabled verification with MD5 and SHA-1.
4. Clicked `Start` to create image.
5. Recorded timestamps and tool version.

**Command / Tool Info:**

```
FTK Imager v4.5.1.3
Source Drive: C:\
Destination: E:\Evidence\disk_image_20251119.E01
Verification: MD5 + SHA-1
Write-blocking: Enabled
Timestamp: 2025-11-19 14:05:00
```

**Hash Verification Results:**

| Artifact                | MD5                              | SHA-1                            |
| ----------------------- | -------------------------------- | -------------------------------- |
| disk_image_20251119.E01 | a1b2c3d4e5f67890123456789abcdef0 | f1e2d3c4b5a697887766554433221100 |

**Justification:** Verified disk imaging preserves original data and maintains integrity for legal or investigative purposes.

---

## 4. Memory Acquisition

**Step:** Capture volatile system memory using DumpIt.

**Actions Taken:**

1. Executed `DumpIt.exe`.
2. Saved memory image to `E:\Evidence\memory_20251119.raw`.
3. Logged tool version, timestamp, and system info.

**Command / Tool Info:**

```
DumpIt v1.9.0
Destination: E:\Evidence\memory_20251119.raw
Timestamp: 2025-11-19 14:15:30
```

**Hash Verification:**

| Artifact            | MD5                              | SHA-1                            |
| ------------------- | -------------------------------- | -------------------------------- |
| memory_20251119.raw | 0f1e2d3c4b5a69788776655443322111 | 9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d |

**Justification:** Capturing memory preserves volatile evidence for analysis of running processes, network connections, and malware activity.

---

## 5. Chain of Custody

| Artifact                | Collected By  | Date/Time        | Tool Used           | Purpose                 | Notes           |
| ----------------------- | ------------- | ---------------- | ------------------- | ----------------------- | --------------- |
| disk_image_20251119.E01 | Investigator1 | 2025-11-19 14:05 | FTK Imager v4.5.1.3 | Disk preservation       | Hashes verified |
| memory_20251119.raw     | Investigator1 | 2025-11-19 14:15 | DumpIt v1.9.0       | Volatile memory capture | Hashes verified |

**Explanation:** Logs every step and responsible handler to maintain evidence integrity.

---

## 6. Verification and Integrity Checks

* All acquired artifacts verified with MD5 and SHA-1.
* Verification logs stored in `E:\Evidence\verification_logs.txt`.

**Example Verification Log:**

```
[INFO] 2025-11-19 14:20:05 - disk_image_20251119.E01 verified: MD5=a1b2c3d4e5f67890123456789abcdef0, SHA-1=f1e2d3c4b5a697887766554433221100
[INFO] 2025-11-19 14:25:10 - memory_20251119.raw verified: MD5=0f1e2d3c4b5a69788776655443322111, SHA-1=9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d
```

---

## 7. Summary

This documentation simulates complete evidence collection and preservation, including:

* Disk imaging with FTK Imager and hash verification.
* Memory acquisition using DumpIt.
* Timestamps, tool versions, and command parameters recorded.
* Use of write-blocking mechanisms to preserve integrity.
* Comprehensive chain-of-custody tracking.
* Verification logs for all artifacts.

**Note:** All files and hashes are simulated for demonstration.
