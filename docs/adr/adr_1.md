# ADR_1 Decision to use Click for CLI Framework
Date: 2025-09-10 - Decider: Roman Shubin

**Status:** Accepted

---

### Context

I am building an all in one Python CLI tool for penetration testing automation. For this, I need robust and reliable framework.
The tool requires:
- Nested commands
- Argument parsing
- Ease of maintenance
- Community support and documentation

---

### Decision

I have decided to use **Click** as the proper framework for the project.

---

### Alternatives Considered

- **Typer**: Modern, type-safe, built on top of Click. 
    * Pros: type hints, concise syntax. 
    * Cons: newer, less established, adds dependency on Typer itself.  

- **argparse**: Built-in to Python. 
    * Pros: no external dependencies. 
    * Cons: verbose, less modern syntax, harder to maintain complex CLIs.  

- **docopt**: Declarative CLI definition. 
    * Pros: minimal boilerplate. 
    * Cons: less flexible, smaller community, harder for nested commands.

---

### Consequences

Positive

- Mature, stable, and widely used in the Python community  
- Supports nested commands and complex argument parsing  
- Extensive documentation and examples  

Negative

- Slightly more verbose compared to newer frameworks like Typer  
- No built-in type hint-based argument validation (requires manual type handling)  
- Adds an external dependency to the project

---

### Implementation Plan

To implement the framework into my project I will be using Python 3.11+. I will also need the technical capabilities listed below.
- Modular command structure (subcommands)
- Support for arguments and options
- Logging to file

---

## References

- [Click Documentation](https://click.palletsprojects.com/)