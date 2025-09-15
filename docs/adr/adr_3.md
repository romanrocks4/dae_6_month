# ADR_3 Decision on Tool Integration Strategy
Date: 2025-09-17 - Decider: Roman Shubin

**Status:** Accepted

---

### Context
The tool must orchestrate multiple external pentesting utilities (e.g., Nmap, sqlmap, Metasploit). Each has different integration options: some provide APIs or Python wrappers, others only expose CLI output. We need a consistent approach.

The tool requires:
- Reliable execution of external tools
- Structured, parseable results
- Ability to support new tools with minimal effort
- Error handling and timeouts

---

### Decision
I have decided to adopt a **Hybrid Integration Strategy**:  
- Use APIs/SDKs where available (e.g., Nessus API, python-nmap, msfrpc).  
- Use subprocess execution with JSON/XML parsing for tools without APIs.  

---

### Alternatives Considered
- **Pure Subprocess Wrappers**  
    * Pros: Works for any tool.  
    * Cons: Fragile, parsing inconsistencies, harder error handling.  

- **Pure API/SDK Approach**  
    * Pros: Structured data, stable integrations.  
    * Cons: Limited availability across tools.  

- **Service-Based (local daemons)**  
    * Pros: Scalability, separation of concerns.  
    * Cons: Adds orchestration complexity.  

---

### Consequences
Positive
- Robustness by leveraging APIs where possible  
- Broad compatibility with CLI-only tools  
- Easier error handling and consistent data schema  

Negative
- Requires maintaining parsers for non-API tools  
- Increased complexity in testing integration paths  

---

### Implementation Plan
- Build abstraction layer for all integrations  
- Normalize outputs into a common JSON schema  
- Enforce timeouts and logging on all subprocess calls  
- Document how to add new tool integrations  

---

## References
- [python-nmap](https://xael.org/pages/python-nmap-en.html)
- [Metasploit RPC API](https://docs.rapid7.com/metasploit/msfrpcd/)
