#!/usr/bin/env python3
"""
Main CLI entry point for the pentesting tool.
"""

import click
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

# Import modules
from cli_tool.modules import recon, vuln
from cli_tool.core import project

console = Console()

@click.group(invoke_without_command=True)
@click.version_option(version="0.1.0", prog_name="pentestctl")
@click.option("--config", "-c", help="Config file path")
@click.option("--project-name", "-p", help="Project name")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.option("--no-shell", is_flag=True, help="Don't start interactive shell")
@click.pass_context
def main(ctx, config, project_name, verbose, no_shell):
    """
    All-in-One CLI Pentesting Tool
    
    A comprehensive command-line tool that automates target reconnaissance,
    active fuzzing of web applications, and other steps of a pentest workflow.
    """
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['project'] = project_name
    ctx.obj['verbose'] = verbose
    
    if verbose:
        console.print(Panel.fit("🛡️  PentestCTL - Starting...", style="bold blue"))
    
    # If no subcommand was invoked and --no-shell not specified, start the shell
    if ctx.invoked_subcommand is None and not no_shell:
        shell.callback()

# Add command groups
main.add_command(project.init)
main.add_command(project.profile)
main.add_command(recon.recon)
main.add_command(vuln.vuln)

# Simple placeholder commands for other modules
@main.command()
def scan():
    """Network scanning (placeholder)."""
    console.print("🔍 Scanning not fully implemented yet")

@main.command()
def exploit():
    """Exploitation (placeholder)."""
    console.print("💥 Exploitation not fully implemented yet")

@main.command()
def ai():
    """AI-powered analysis (placeholder)."""
    console.print("🤖 AI module not fully implemented yet")

@main.command()
def report():
    """Report generation (placeholder)."""
    console.print("📄 Report generation not fully implemented yet")

@main.command()
def shell():
    """Start interactive pentestctl shell."""
    console.print(Panel.fit("🛡️  PentestCTL Interactive Shell", style="bold blue"))
    console.print("Type 'help' for available commands or 'exit' to quit.\n")
    
    while True:
        try:
            # Get user input
            command_input = Prompt.ask("[bold cyan]pentestctl[/bold cyan]")
            
            # Handle exit commands
            if command_input.lower() in ['exit', 'quit', 'q']:
                console.print("👋 Goodbye!")
                break
            
            # Handle help
            if command_input.lower() in ['help', 'h']:
                show_help()
                continue
            
            # Handle empty input
            if not command_input.strip():
                continue
            
            # Parse and execute command
            try:
                # Split command into parts
                parts = command_input.strip().split()
                if not parts:
                    continue
                
                # Execute the command by calling the main CLI with the parsed arguments
                # We need to temporarily modify sys.argv to make Click work
                original_argv = sys.argv.copy()
                sys.argv = ['pentestctl'] + parts
                
                try:
                    # Create a new context and invoke the command
                    ctx = click.Context(main)
                    with ctx:
                        main.main(parts, standalone_mode=False)
                except SystemExit:
                    # Click raises SystemExit on completion, catch it to continue the shell
                    pass
                except click.ClickException as e:
                    console.print(f"❌ Error: {e.message}")
                except Exception as e:
                    console.print(f"❌ Unexpected error: {str(e)}")
                finally:
                    # Restore original argv
                    sys.argv = original_argv
                    
            except Exception as e:
                console.print(f"❌ Failed to parse command: {str(e)}")
                
        except KeyboardInterrupt:
            console.print("\n👋 Goodbye!")
            break
        except EOFError:
            console.print("\n👋 Goodbye!")
            break

def show_help():
    """Display help information for the interactive shell."""
    help_text = Text()
    help_text.append("Available Commands:\n\n", style="bold")
    help_text.append("📋 Project Management:\n", style="cyan")
    help_text.append("  init create --project <name>    Create new project\n")
    help_text.append("  profile create --name <name>    Create profile\n")
    help_text.append("  profile list                    List profiles\n\n")
    
    help_text.append("🕵️  Reconnaissance:\n", style="green")
    help_text.append("  recon run --target <domain>     Run reconnaissance\n")
    help_text.append("  recon emails --target <domain>  Extract emails\n\n")
    
    help_text.append("🔍 Other Modules:\n", style="yellow")
    help_text.append("  scan                            Network scanning\n")
    help_text.append("  vuln                            Vulnerability analysis\n")
    help_text.append("  exploit                         Exploitation\n")
    help_text.append("  ai                              AI analysis\n")
    help_text.append("  report                          Report generation\n\n")
    
    help_text.append("🚪 Shell Commands:\n", style="magenta")
    help_text.append("  help, h                         Show this help\n")
    help_text.append("  exit, quit, q                   Exit shell\n")
    
    console.print(help_text)

if __name__ == "__main__":
    main()