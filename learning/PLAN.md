# learning/PLAN.md

> This is my one-page learning plan for the month. I will complete and commit this file during the 15-minute selection clinic. It records the technology I chose to learn, why I chose it for my capstone, the three focused tasks I will complete, and the proof I will capture to show I did the work.

---

## Student commitment

-   **Name: Roman Shubin**
-   **Date created:** 2025-10-01

I commit to treat this plan as my personal roadmap: I will keep dates realistic, finish each small task, capture evidence of success, and update this file if anything changes.

---

## Chosen technology

-   **Technology name: Trivy**
-   **Technology version: 0.67**

### Why I chose this technology

Trivy is an all in one security scanner. I am implementing this technology beacause it is an open source software that matches the same goals as my project. Trivy's expansive use cases and easy to use software is why I choose it.

---

## First-day actions (complete in the 15-minute selection clinic)

1. Finalize the **Chosen technology** and **Why I chose this technology** fields above.
2. Draft three small integration tasks below with realistic start and target completion dates.
3. Commit this file to the repository at `learning/PLAN.md` before the end of the 15-minute clinic.
4. Record where I will start Task 1 (for example: local branch name or workspace folder) under Task 1.
5. If a task feels too large, I will make it smaller and update the dates here.

---

## My three integration tasks (small, testable, dated)

For each task include Title, Description, Start date, Target completion date, a clear Success criterion, and the Proof method I will capture to show success.

**Task 1 — Install and test Trivy:**

-   **Description:** For this task I will download and integrate trivy into my CLI tool
-   **Start date:** 2025-10-01
-   **Target completion date:** 2025-10-02
-   **Success criterion:** Trivy is downloaded and works when called within my project. The code used contains no errors and has proper syntax.
-   **Proof method (what I will capture to show success):** a screenshot of Trivy being ran from my tool, capturing, and displaying the results.
-   **Where I will start Task 1:** Within the vuln.py file of my CLI tool.

**Task 2 — Run a local folder scan with Trivy:**

-   **Description:** For this task I will use Trviy to scan a local folder for insecure depenencies.
-   **Start date:** 2025-10-06
-   **Target completion date:** 2025-10-09
-   **Success criterion:** Running mytool vuln --fs ./project_folder lists vulnerabilities in dependencies.
-   **Proof method:** Screenshot of scan output showing detected CVEs.

**Task 3 — Generate a report with Trivy:**

-   **Description:** For this task I will use Trivy's JSON capabilities to export the scan results into a JSON file.
-   **Start date:** 2025-10-13
-   **Target completion date:** 2025-10-16
-   **Success criterion:** A JSON file should be generated from Trivy with the info from the scan in the file.
-   **Proof method:** Upload and commit the generated JSON/HTML report.

---

## Risks, assumptions, and blockers

-  Need a vulnerable local folder to text the scan in task 2.
-  Need to use the file generation in CLI tool and integrate it. 

---

## My weekly timeline (one-line plan)

-   **Week 1:** Commit this PLAN and start Task 1.
-   **Week 2:** Continue Task 1; produce a draft PR or demo; start Task 2.
-   **Week 3:** Continue Task 2; add tests/logging and peer review; start Task 3.
-   **Week 4:** Finalize PR(s) or demo(s); draft `learning/README.md` and `learning/REFLECTION.md`.

I will replace the above with exact dates in the tasks section once I finalize them.

---