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
from pathlib import Path

# Import modules
from cli_tool.modules import recon, vuln, scan, ai
from cli_tool.core import project
from cli_tool.reporting import report

console = Console()

# Global variable to store last command output
last_command_output = ""

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
main.add_command(scan.scan)
main.add_command(ai.ai)
main.add_command(report.report)

# Simple placeholder commands for other modules
@main.command()
def exploit():
    """Exploitation (placeholder)."""
    output = "💥 Exploitation not fully implemented yet"
    console.print(output)
    save_last_command_output(output)

def save_last_command_output(output):
    """Save the last command output to a temporary file for AI module access."""
    global last_command_output
    last_command_output = output
    try:
        temp_output_file = Path(__file__).parent.parent / ".pentestctl_last_output"
        with open(temp_output_file, 'w') as f:
            f.write(output)
    except Exception:
        # Silently fail if we can't save the output
        pass

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
                    error_output = f"❌ Error: {e.message}"
                    console.print(error_output)
                    save_last_command_output(error_output)
                except Exception as e:
                    error_output = f"❌ Unexpected error: {str(e)}"
                    console.print(error_output)
                    save_last_command_output(error_output)
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
    
    help_text.append("🔍 Scanning:\n", style="yellow")
    help_text.append("  scan run --target <ip/domain> --ports <ports>  Run network scan\n\n")
    
    help_text.append("🛡️  Vulnerability Analysis:\n", style="red")
    help_text.append("  vuln run --target <ip/domain>   Run vulnerability scan\n\n")
    
    help_text.append("🤖 AI Analysis:\n", style="blue")
    help_text.append("  ai summarize <file|'.'>         Summarize findings (use '.' for last command)\n")
    help_text.append("  ai triage <file|'.'>            Triage vulnerabilities (use '.' for last command)\n")
    help_text.append("  ai ask <question>               Ask AI assistant\n\n")
    
    help_text.append("📑 Reporting:\n", style="magenta")
    help_text.append("  report generate --project <name>  Generate AI-powered pentest report\n")
    help_text.append("  report template                   Generate report from template\n\n")
    
    help_text.append("💣 Exploitation:\n", style="red")
    help_text.append("  exploit                         Exploitation tools\n\n")
    
    help_text.append("🚪 Shell Commands:\n", style="magenta")
    help_text.append("  help, h                         Show this help\n")
    help_text.append("  exit, quit, q                   Exit shell\n")
    
    console.print(help_text)

if __name__ == "__main__":
    main()