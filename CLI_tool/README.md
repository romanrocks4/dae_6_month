# All-in-One CLI Pentesting Tool

> **Source:** Original design doc (v1). See original PDF for reference.

---

## 1. Project Title & Version Control
- **Project:** All-in-one CLI pentesting tool  
- **Version:** DRAFT  
- **Last updated:** September, 17, 2025 
- **Change log:** N/A

---

## 2. Project Summary
I am creating an all-in-one command-line tool that automates target reconnaissance, active fuzzing of web applications, and the other steps of a pentest workflow. The tool compresses commonly used pentesting software into a single, customizable CLI environment to help pentesters organize and speed up work.

---

## 3. Problem Statement / Use Case
Pentesting workflows contain many repetitive steps and often require switching between multiple tools and scripts. This tool combines the most useful tools for each phase into one environment with consistent commands, configurable workflows, and saveable project profiles — reducing context switching and speeding up engagement delivery.

---

## 4. Goals & Objectives
1. Provide a working, usable CLI that can run **at least two tools** per pentest phase.  
2. Offer clear commands and nested subcommands for discoverability and navigation.  
3. Create configurable, customizable, and saveable environments/profiles per user/project.  
4. Add **AI integration** to assist with guidance, and automated reporting (details below).

---

## 5. Key Features / Functions
- Single CLI binary that wraps and orchestrates established pentesting tools.  
- Nested commands and subcommands for each pentest phase (recon, scanning, vuln analysis, exploitation, reporting).  
- Saveable project profiles (targets, scope, credentials, excluded hosts, scan schedules).  
- Abstraction layers / adapters for tool compatibility to reduce integration issues.  
- Colorized, human-readable CLI output plus machine-readable export (JSON/Markdown/HTML/PDF).  
- **AI features:** automated result summarization, vulnerability triage & severity suggestions, guided exploit hints, interactive natural language assistant, and draft report generation.

---

## 6. Tech Stack & Tools
**Core:** Python (Click for CLI framework recommended), Linux for development/testing.

**Common tools to integrate (examples):**
- **Recon:** theHarvester, Shodan, Amass, Sublist3r, whois.  
- **Scanning:** Nmap, Masscan, WhatWeb.  
- **Vuln Analysis:** Nessus (API), OpenVAS, Nikto, sqlmap.  
- **Exploitation:** Metasploit (msfrpc), CrackMapExec, Hydra, Burp Suite API.  
- **Reporting:** Custom scripts → Markdown, PDF, HTML.

**AI & ML (new additions):**
- **Model access:** OpenAI API (for hosted LLMs) *and* support for local/self-hosted models via Hugging Face / Transformers / GGML backends for offline/air-gapped usage.  
- **Prompt orchestration / chains:** LangChain or a lightweight internal orchestration layer.  
- **Embeddings & vector DB:** For storing and searching previous findings, use FAISS / Annoy / Chroma (local option).  
- **NLP utils:** spaCy / NLTK for lightweight parsing, metadata extraction.  
- **Security & sandboxing:** strict rate-limits, request logging, and data redaction before sending to hosted APIs.  
- **Packaging:** Use Poetry for dependency and packaging management; provide an option to install as system/global CLI or user-level.

---

## 7. Architecture & Workflow (high level)
- **CLI Layer:** `cli` (Click) — top level commands and subcommands, profiles, and global flags.  
- **Controller / Orchestrator:** Central manager that coordinates tool adapters, job queues, and result collectors.  
- **Adapters / Wrappers:** One adapter per external tool (exec wrappers, API clients). Adapters normalize output to a common JSON schema.  
- **Data Layer:** Local project DB (lightweight SQLite) + optional vector DB (embeddings).  
- **AI Module:** pluggable connector that can run local models or call hosted APIs; provides summarization, triage, Q&A, and report drafting.  
- **Reporting Engine:** Transforms normalized results + AI summaries into desired export formats.  
- **Safety Layer:** Scope & rules engine to prevent out-of-scope scanning, credential leaks, and accidental destructive commands.

---

## 8. CLI UX — Example Commands & Structure
(Suggested top-level layout)

```
pentestctl init --project my-engagement --scope targets.txt
pentestctl profile create --name clientA --config config.yaml
pentestctl recon run --target example.com --modules amass,theHarvester --output project/recon.json
pentestctl scan run --target example.com --modules nmap,masscan --ports 1-65535
pentestctl vuln run --target example.com --modules nikto,openvas --credentials creds.json
pentestctl exploit run --target example.com --module metasploit --exploit CVE-XXXX-YYYY
pentestctl ai summarize --input project/recon.json --length short
pentestctl report generate --template standard --format pdf --include-ai-summary
```

**AI CLI examples**
```
# Quick natural language question (local or remote LLM)
pentestctl ai ask "Which assets appear most at risk in project/recon.json?"

# Auto-triage vulnerabilities and assign risk levels using AI + rules
pentestctl ai triage --input project/vulns.json --output project/vulns_triaged.json

# Draft a pentest report using AI to summarize findings
pentestctl ai report --input project/ --template pentest-template.md --output report/draft.pdf
```

---

## 9. Timeline / Weekly Milestones (updated)
- **Week 1:** Create initial CLI framework; research tools and AI options.  
- **Week 2:** Integrate recon tools & adapters; begin basic output system.  
- **Week 3:** Build output system; add project DB and normalized JSON schema.  
- **Week 4:** Integrate port scanning tools and flags; implement safe defaults.  
- **Week 5:** Add fingerprinting tools; persist results to DB.  
- **Week 6:** Add vulnerability scanning tools; log results.  
- **Week 7:** Label vulnerabilities with risk factors and group by asset.  
- **Week 8:** Build exploitation wrappers and test.  
- **Week 9:** Add safeguards, customization functionality.  
- **Week 10:** Design report builder.  
- **Week 11:** Polish CLI, error handling, colorized outputs, help menus.  
- **Week 12:** **AI integration finishing:** finalize AI module, prompts, embeddings index, user privacy options; troubleshoot and push to GitHub with docs.

---

## 10. Risks & Risk Mitigation (expanded)
**Original risk:** tool compatibility and integration issues. Mitigation: abstraction layers and extra troubleshooting time.

**New AI-related risks & mitigations:**
- **Data leakage to hosted APIs:** implement redaction filters (strip credentials, IPs if required), provide opt-in for cloud APIs, and support local LLM operation for sensitive environments.  
- **Incorrect AI guidance:** always label AI output as *suggestions*; require operator confirmation before performing destructive actions.  
- **Cost & rate limiting (hosted APIs):** add usage quotas per profile and local caching of AI responses/embeddings.  
- **Adversarial / hallucinated output:** validate AI summaries against raw data and present provenance (which logs, which scanner outputs were used).  
- **Regulatory / legal risks:** ensure the tool enforces scope checks and requires explicit acceptance of engagement rules before running intrusive modules.

---

## 11. Evaluation Criteria (updated)
1. Functional across reconnaissance, scanning, vuln analysis, exploitation, and reporting phases without catastrophic errors.  
2. Customizability for users (profiles, tool selection, config overrides).  
3. Speed and usability: faster than manual orchestration; clear help and error handling.  
4. **AI effectiveness:** AI should reliably summarize and triage outputs — measured by human reviewer agreement with AI triage on a test sample (e.g., >80% agreement target).

---

## 12. AI Integration — Design & Implementation Details (new)
### 12.1 Goals for AI features
- **Summarization:** compress long scan outputs into concise findings per asset.  
- **Triage & Prioritization:** suggest severity and exploitability rankings.  
- **Natural Language Assistant:** allow users to ask questions about results and receive context-aware answers.  
- **Report Drafting:** generate first-draft reports (Markdown/PDF) with findings, remediation suggestions, and evidence links.  
- **Workflow Automation:** suggest next steps (e.g., follow-up scans, fuzzing targets) and provide command snippets.

### 12.2 Components
- **AI Connector:** pluggable interface supporting:
  - Hosted LLMs (OpenAI, Anthropic, etc.) via API.
  - Local models via Hugging Face / transformers / ggml for air-gapped use.
- **Prompt Templates & Chains:** curated prompts for each AI task (summarize, triage, question answering). Store templates in `ai/prompts/`.
- **Embeddings & Search:** compute embeddings per finding to enable quick similarity search for repeated issues across engagements.
- **Explainability & Provenance:** include the list of source documents (scanner output lines) used to produce each summary/claim.
- **Permissions & Safety:** per-project toggles for sending data offsite; anonymization/redaction options; logs for all AI calls.

### 12.3 Example prompt templates (simplified)
- **Summarize scanner output**
  > "Summarize the following Nmap output into a short bulleted list of open services, suspicious banners, and recommended follow-up scans. Include raw evidence lines as references."

- **Triage vulnerabilities**
  > "Given the following vulnerability findings (JSON), assign a severity (Low/Med/High/Critical) and a short justification referencing CVE or common misconfigurations."

### 12.4 Data handling & privacy
- Local encryption for project DB (optional).  
- Redaction engine to remove or hash sensitive fields before sending to hosted LLMs.  
- Audit logs to show what was sent to which model and when.  
- Config options:
  - `ai.offsite=false` (do not call hosted APIs)
  - `ai.model=local-ggml` / `ai.model=openai-gpt-4o`
  - `ai.provenance=true` (attach evidence)

### 12.5 UX examples (AI)
- `pentestctl ai summarize --input project/recon.json --length medium --provenance` → returns a machine and human readable summary + evidence links.  
- `pentestctl ai triage --input project/vulns.json --format json` → outputs triaged vulnerabilities with severity and confidence.

---

## 13. Future Considerations
1. Keep integrated tools up to date; add new tools to stay relevant.  
2. Security mechanism to prevent vulnerabilities in the tool itself.  
3. Potential GUI and cross-platform support for broader user base.  
4. Expand AI features: automated remediation suggestions, continuous learning (with user approvals), community-shared prompt recipes, and telemetry (opt-in) to improve triage models.

---

## 14. Implementation Checklist (practical next steps)
- [ ] Pick CLI framework (Click recommended).  
- [ ] Define normalized JSON schema for all tool outputs.  
- [ ] Implement Adapter interface and a first adapter (e.g., Nmap).  
- [ ] Implement project DB (SQLite) + basic CLI `init` & `profile` commands.  
- [ ] Implement reporting templates (Markdown → PDF).  
- [ ] Build AI connector with:
  - local model fallback,
  - OpenAI (or chosen provider) connector,
  - prompt templates for summarize/triage/report.  
- [ ] Add AI privacy/redaction options and audit logs.  
- [ ] Add test suite and CI; document install & usage; push to GitHub.

---

## 15. Appendix — Suggested Libraries & Resources
- **CLI & packaging:** Click, Poetry.  
- **API & adapters:** Requests / httpx, python-msfrpc, python-nmap.  
- **AI/LLM:** openai, langchain, transformers, sentence-transformers (embeddings).  
- **Vector DB:** FAISS, Chroma.  
- **DB:** SQLite (SQLModel/SQLAlchemy).  
- **Reporting:** Markdown → Pandoc → PDF, WeasyPrint for HTML→PDF.  
- **Testing:** pytest.  
