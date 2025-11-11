"""
Reconnaissance module for pentestctl.
"""

import subprocess
import json
import click
from rich.console import Console
from rich.table import Table
from typing import Dict, List, Any
from cli_tool.core.project import ProjectManager
from pathlib import Path

console = Console()

@click.group()
def recon():
    """Reconnaissance commands."""
    pass

def get_current_project():
    """Get the current project from the context file."""
    try:
        # Look for the project file in the current working directory
        project_file = Path.cwd() / ".pentestctl_current_project"
        if project_file.exists():
            with open(project_file, 'r') as f:
                return f.read().strip()
        # Also check in the CLI tool root directory
        cli_tool_root = Path(__file__).parent.parent
        project_file = cli_tool_root / ".pentestctl_current_project"
        if project_file.exists():
            with open(project_file, 'r') as f:
                return f.read().strip()
    except Exception:
        pass
    return None

@recon.command()
@click.option("--target", "-t", required=True, help="Target domain")
@click.option("--modules", "-m", default="theharvester", help="Comma-separated list of modules")
@click.option("--output", "-o", help="Output file path")
@click.option("--source", "-s", default="duckduckgo", help="theHarvester source")
@click.option("--limit", "-l", default=100, help="theHarvester limit")
@click.option("--project", "-p", help="Project name to save results to")
def run(target, modules, output, source, limit, project):
    """Run reconnaissance against target."""
    console.print(f"🕵️  Starting reconnaissance on {target}")
    
    # Use current project if none specified
    if not project:
        project = get_current_project()
    
    module_list = [m.strip() for m in modules.split(',')]
    results = {}
    
    for module in module_list:
        if module == "theharvester":
            results[module] = run_theharvester(target, source, limit)
        elif module == "amass":
            results[module] = run_amass(target)
        elif module == "sublist3r":
            results[module] = run_sublist3r(target)
        else:
            console.print(f"⚠️  Unknown module: {module}")
    
    # Display results
    display_recon_results(results)
    
    # Save results to project if specified
    if project:
        pm = ProjectManager(project)
        pm.save_finding("recon", target, results)
        # Save detailed log
        pm.save_detailed_log("recon", target, results, "recon")
    
    # Save results if output specified
    if output:
        with open(output, 'w') as f:
            json.dump(results, f, indent=2)
        console.print(f"💾 Results saved to {output}")
    
    # Save output to temporary file for AI module
    save_output_for_ai(results)

def save_output_for_ai(data):
    """Save command output to temporary file for AI module access."""
    try:
        # Convert data to a readable format
        output_str = json.dumps(data, indent=2)
        temp_output_file = Path(__file__).parent.parent / ".pentestctl_last_output"
        with open(temp_output_file, 'w') as f:
            f.write(output_str)
    except Exception:
        # Silently fail if we can't save the output
        pass

def run_theharvester(domain: str, source: str, limit: int) -> Dict[str, Any]:
    """Run theHarvester against target."""
    console.print(f"🌾 Running theHarvester on {domain}")
    
    try:
        cmd = ["theHarvester", "-d", domain, "-b", source, "-l", str(limit)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            # Parse theHarvester output
            output_lines = result.stdout.strip().split('\n')
            emails = []
            hosts = []
            
            # More robust parsing of theHarvester output
            for line in output_lines:
                line = line.strip()
                # Skip theHarvester banner/header lines and empty lines
                if ("@" in line and "." in line and 
                    not line.startswith("[") and 
                    not line.startswith("*") and
                    not "cmartorella@edge-security.com" in line and
                    not "theHarvester" in line and
                    line != "*" and
                    len(line) > 3):
                    # Basic email validation
                    if line.count("@") == 1 and "." in line.split("@")[1]:
                        emails.append(line)
                elif ((line.startswith(domain) or line.endswith(f".{domain}")) and 
                      ":" not in line and 
                      not line.startswith("*") and
                      not "theHarvester" in line and
                      len(line) > 3):
                    hosts.append(line)
            
            return {
                "status": "success",
                "emails": list(set(emails)),
                "hosts": list(set(hosts)),
                "raw_output": result.stdout
            }
        else:
            error_msg = result.stderr.strip() if result.stderr.strip() else "theHarvester execution failed"
            return {
                "status": "error", 
                "error": error_msg,
                "emails": [],
                "hosts": []
            }
            
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout", 
            "error": "theHarvester timed out after 5 minutes",
            "emails": [], 
            "hosts": []
        }
    except FileNotFoundError:
        return {
            "status": "error", 
            "error": "theHarvester not found. Install with: pip3 install theHarvester",
            "emails": [], 
            "hosts": []
        }
    except Exception as e:
        return {
            "status": "error", 
            "error": f"Unexpected error: {str(e)}",
            "emails": [], 
            "hosts": []
        }

def run_amass(domain: str) -> Dict[str, Any]:
    """Run Amass against target (placeholder)."""
    console.print(f"🔍 Amass not implemented yet for {domain}")
    return {"status": "not_implemented", "subdomains": []}

def run_sublist3r(domain: str) -> Dict[str, Any]:
    """Run Sublist3r against target (placeholder).""" 
    console.print(f"📝 Sublist3r not implemented yet for {domain}")
    return {"status": "not_implemented", "subdomains": []}

def display_recon_results(results: Dict[str, Dict[str, Any]]):
    """Display reconnaissance results in a nice table."""
    
    for module, data in results.items():
        console.print(f"\n📊 Results from {module.upper()}:")
        
        if data.get("status") == "success":
            if "emails" in data and data["emails"]:
                email_table = Table(title="Emails Found")
                email_table.add_column("Email", style="cyan")
                for email in data["emails"]:
                    email_table.add_row(email)
                console.print(email_table)
            
            if "hosts" in data and data["hosts"]:
                host_table = Table(title="Hosts Found")
                host_table.add_column("Host", style="green")
                for host in data["hosts"]:
                    host_table.add_row(host)
                console.print(host_table)
                    
            if "subdomains" in data and data["subdomains"]:
                subdomain_table = Table(title="Subdomains Found")
                subdomain_table.add_column("Subdomain", style="yellow")
                for subdomain in data["subdomains"]:
                    subdomain_table.add_row(subdomain)
                console.print(subdomain_table)
        else:
            console.print(f"❌ {module} failed: {data.get('error', 'Unknown error')}")

@recon.command()
@click.option("--target", "-t", required=True, help="Target domain")
@click.option("--source", "-s", default="duckduckgo", help="Source to use")
@click.option("--limit", "-l", default=100, help="Result limit")
@click.option("--project", "-p", help="Project name to save results to")
def emails(target, source, limit, project):
    """Extract emails for target domain."""
    # Use current project if none specified
    if not project:
        project = get_current_project()
    
    console.print(f"📧 Extracting emails for {target}")
    result = run_theharvester(target, source, limit)
    
    if result["status"] == "success" and result["emails"]:
        email_table = Table(title=f"Emails for {target}")
        email_table.add_column("Email", style="cyan")
        for email in result["emails"]:
            email_table.add_row(email)
        console.print(email_table)
    
    # Save results to project if specified
    if project:
        pm = ProjectManager(project)
        pm.save_finding("emails", target, result)
        # Save detailed log
        pm.save_detailed_log("emails", target, result, "recon")
    
    # Save output to temporary file for AI module
    save_output_for_ai(result)
