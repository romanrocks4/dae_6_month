#!/usr/bin/env python3
"""
Main CLI entry point for the pentesting tool.
"""

import click
from rich.console import Console
from rich.panel import Panel

# Import simplified modules
from cli_tool.modules import recon

console = Console()

@click.group()
@click.version_option(version="0.1.0", prog_name="pentestctl")
@click.option("--config", "-c", help="Config file path")
@click.option("--project", "-p", help="Project name")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.pass_context
def main(ctx, config, project, verbose):
    """
    All-in-One CLI Pentesting Tool
    
    A comprehensive command-line tool that automates target reconnaissance,
    active fuzzing of web applications, and other steps of a pentest workflow.
    """
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['project'] = project
    ctx.obj['verbose'] = verbose
    
    if verbose:
        console.print(Panel.fit("🛡️  PentestCTL - Starting...", style="bold blue"))

# Add command groups (only recon for now)
main.add_command(recon.recon)

# Simple placeholder commands
@main.command()
def init():
    """Initialize a new project (placeholder)."""
    console.print("🔧 Project initialization not fully implemented yet")

@main.command()
def scan():
    """Network scanning (placeholder)."""
    console.print("🔍 Scanning not fully implemented yet")

@main.command()
def vuln():
    """Vulnerability analysis (placeholder)."""
    console.print("🛡️  Vulnerability analysis not fully implemented yet")

if __name__ == "__main__":
    main()