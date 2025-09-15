# ADR_2 Decision to use Python for Primary Language
Date: 2025-09-15 - Decider: Roman Shubin

**Status:** Accepted

---

### Context
The CLI tool requires a language that is flexible, has strong library support for penetration testing tasks, and integrates with external tools easily. Development speed, community support, and available wrappers/APIs are also key.

The tool requires:
- Rich ecosystem of networking and security libraries
- Easy integration with subprocess calls
- Broad community adoption
- Cross-platform support

---

### Decision
I have decided to use **Python 3.11** as the primary implementation language.

---

### Alternatives Considered
- **Go (Golang)**  
    * Pros: High performance, single static binary builds, great concurrency.  
    * Cons: Fewer ready-made pentest wrappers, would require reimplementation.  

- **Rust**  
    * Pros: Memory safety, performance.  
    * Cons: Steeper learning curve, slower development cycle, fewer libraries.  

- **Hybrid (Python + Go modules)**  
    * Pros: Balance of ease and performance.  
    * Cons: More complex workflow and packaging.  

---

### Consequences
Positive
- Leverages a huge ecosystem of pentesting-related libraries  
- Rapid development and prototyping  
- Easy onboarding for new contributors  

Negative
- Slower runtime performance vs compiled languages  
- Larger distribution size if packaged into a binary  
- Requires dependency management and auditing  

---

### Implementation Plan
- Use Python 3.11+  
- Dependency pinning with `requirements.txt`  
- Static analysis with Bandit, linting with flake8  
- Package distribution with Docker and PyInstaller

---

## References
- [Python.org](https://www.python.org/)
