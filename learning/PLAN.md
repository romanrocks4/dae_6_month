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
-   **Target completion date:** 2025-10-01
-   **Success criterion:** Trivy is downloaded and works when called within my project. The code used contains no errors and has proper syntax.
-   **Proof method (what I will capture to show success):** a screenshot of Trivy being ran from my tool, capturing, and displaying the results.
-   **Where I will start Task 1:** Within the vuln.py file of my CLI tool.

**Task 2 — :**

-   **Description:**
-   **Start date:** YYYY-MM-DD
-   **Target completion date:** YYYY-MM-DD
-   **Success criterion (explicit):**
-   **Proof method (what I will capture to show success):**

**Task 3 — Title:**

-   **Description:**
-   **Start date:** YYYY-MM-DD
-   **Target completion date:** YYYY-MM-DD
-   **Success criterion (explicit):**
-   **Proof method (what I will capture to show success):**

> Note: Keep each task small enough that one task = one focused change or one short demo.

---

## Risks, assumptions, and blockers (one-line each)

List any access or external requirements that could block completion. For example:

-   Requires remote DB credentials.
-   Needs API key for third-party service.
-   Depends on another repo update.

---

## My weekly timeline (one-line plan)

-   **Week 1:** Commit this PLAN and start Task 1.
-   **Week 2:** Continue Task 1; produce a draft PR or demo; start Task 2.
-   **Week 3:** Continue Task 2; add tests/logging and peer review; start Task 3.
-   **Week 4:** Finalize PR(s) or demo(s); draft `learning/README.md` and `learning/REFLECTION.md`.

I will replace the above with exact dates in the tasks section once I finalize them.

---

## Example (model entry — replace with my own)

**Name:** Alex Example  
**Date created:** 2025-09-01

**Chosen technology:** FastAPI 0.95

**Why:** FastAPI lets me add a small HTTP endpoint to our capstone API so I can demonstrate endpoint design and tests.

**Task 1 — Add user-summary endpoint**

-   **Description:** Add `GET /users/{id}/summary` returning aggregated profile data.
-   **Start date:** 2025-09-02
-   **Target completion date:** 2025-09-08
-   **Success criterion:** A unit or integration test demonstrates the endpoint returns expected JSON for sample data.
-   **Proof method:** I will capture a screenshot of the CI test passing and paste one curl example and expected JSON into `learning/README.md`.
-   **Where I will start Task 1:** local branch `feature/user-summary`

**Task 2 — Request counter & health-check**

-   **Description:** Add an in-memory counter for endpoint requests and expose `/health`.
-   **Start date:** 2025-09-09
-   **Target completion date:** 2025-09-15
-   **Success criterion:** Health-check test fails when service is down and passes when service is up.
-   **Proof method:** I will save a short terminal recording or screenshot showing the health-check response and note the test run in `learning/README.md`.

**Task 3 — Mini-tutorial**

-   **Description:** Write a one-page tutorial in `learning/README.md` showing how to call the endpoint with example response.
-   **Start date:** 2025-09-16
-   **Target completion date:** 2025-09-22
-   **Success criterion:** Tutorial includes a curl example and expected JSON and a screenshot or short recorded response.
-   **Proof method:** I will save the tutorial to `learning/README.md` with a screenshot or short recorded command output link.