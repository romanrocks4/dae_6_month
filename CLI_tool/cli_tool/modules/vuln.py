"""
Vulnerability analysis module for pentestctl.
"""

import click
import subprocess
import json
from rich.console import Console
from rich.table import Table
from typing import Dict, Any

console = Console()

def run_trivy(target: str, scan_type: str = "image", severity: str = "HIGH,CRITICAL") -> Dict[str, Any]:
    """Run Trivy vulnerability scanner against target."""
    console.print(f"🔍 Running Trivy {scan_type} scan on {target}")
    
    try:
        # Build the Trivy command
        if scan_type == "image":
            cmd = ["trivy", "image", "--severity", severity, "--format", "json", target]
        elif scan_type == "fs":
            cmd = ["trivy", "fs", "--severity", severity, "--format", "json", target]
        elif scan_type == "config":
            cmd = ["trivy", "config", "--severity", severity, "--format", "json", target]
        else:
            return {
                "status": "error",
                "error": f"Unsupported scan type: {scan_type}",
                "results": []
            }
        
        # Run Trivy
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            # Parse JSON output
            try:
                trivy_output = json.loads(result.stdout)
                return {
                    "status": "success",
                    "results": trivy_output,
                    "raw_output": result.stdout
                }
            except json.JSONDecodeError as e:
                return {
                    "status": "error",
                    "error": f"Failed to parse Trivy output: {str(e)}",
                    "results": []
                }
        else:
            error_msg = result.stderr.strip() if result.stderr.strip() else "Trivy execution failed"
            return {
                "status": "error", 
                "error": error_msg,
                "results": []
            }
            
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout", 
            "error": "Trivy timed out after 5 minutes",
            "results": []
        }
    except FileNotFoundError:
        return {
            "status": "error", 
            "error": "Trivy not found. Install with: brew install trivy",
            "results": []
        }
    except Exception as e:
        return {
            "status": "error", 
            "error": f"Unexpected error: {str(e)}",
            "results": []
        }

def display_trivy_results(results: Dict[str, Any]):
    """Display Trivy scan results in a nice table."""
    if results.get("status") != "success":
        console.print(f"❌ Trivy scan failed: {results.get('error', 'Unknown error')}")
        return
    
    trivy_data = results.get("results", {})
    
    # Display summary
    if "Results" in trivy_data:
        for target_result in trivy_data["Results"]:
            target_name = target_result.get("Target", "Unknown Target")
            vulnerabilities = target_result.get("Vulnerabilities", [])
            
            if vulnerabilities:
                console.print(f"\n🛡️  Vulnerabilities found in {target_name}:")
                vuln_table = Table(title=f"Vulnerabilities in {target_name}")
                vuln_table.add_column("ID", style="cyan")
                vuln_table.add_column("Severity", style="red")
                vuln_table.add_column("Title", style="yellow")
                vuln_table.add_column("Installed", style="green")
                vuln_table.add_column("Fixed", style="blue")
                
                for vuln in vulnerabilities:
                    vuln_id = vuln.get("VulnerabilityID", "N/A")
                    severity = vuln.get("Severity", "Unknown")
                    title = vuln.get("Title", vuln.get("Description", "N/A"))[:50] + "..." if len(vuln.get("Title", vuln.get("Description", "N/A"))) > 50 else vuln.get("Title", vuln.get("Description", "N/A"))
                    installed = vuln.get("InstalledVersion", "N/A")
                    fixed = vuln.get("FixedVersion", "N/A")
                    
                    # Color code severity
                    if severity == "CRITICAL":
                        severity_style = "bold red"
                    elif severity == "HIGH":
                        severity_style = "red"
                    elif severity == "MEDIUM":
                        severity_style = "yellow"
                    elif severity == "LOW":
                        severity_style = "green"
                    else:
                        severity_style = "white"
                    
                    vuln_table.add_row(
                        vuln_id,
                        f"[{severity_style}]{severity}[/{severity_style}]",
                        title,
                        installed,
                        fixed
                    )
                
                console.print(vuln_table)
            else:
                console.print(f"✅ No vulnerabilities found in {target_name}")
    else:
        console.print("ℹ️  No detailed results in Trivy output")

@click.group()
def vuln():
    """Vulnerability analysis commands."""
    pass

@vuln.command()
@click.option("--target", "-t", required=True, help="Target to analyze (image name, filesystem path, or config path)")
@click.option("--modules", "-m", default="trivy", help="Vulnerability modules (trivy, nikto, openvas)")
@click.option("--scan-type", "-s", default="image", help="Scan type (image, fs, config)")
@click.option("--severity", default="HIGH,CRITICAL", help="Severity levels to report")
@click.option("--output", "-o", help="Output file path (JSON format)")
def run(target, modules, scan_type, severity, output):
    """Run vulnerability analysis against target."""
    console.print(f"🛡️  Starting vulnerability analysis on {target}")
    
    module_list = [m.strip() for m in modules.split(',')]
    results = {}
    
    for module in module_list:
        if module == "trivy":
            results[module] = run_trivy(target, scan_type, severity)
            display_trivy_results(results[module])
        elif module == "nikto":
            console.print(f"⚠️  Nikto module not fully implemented yet for {target}")
            results[module] = {"status": "not_implemented", "results": []}
        elif module == "openvas":
            console.print(f"⚠️  OpenVAS module not fully implemented yet for {target}")
            results[module] = {"status": "not_implemented", "results": []}
        else:
            console.print(f"⚠️  Unknown module: {module}")
            results[module] = {"status": "unknown", "results": []}
    
    # Save results if output specified
    if output:
        with open(output, 'w') as f:
            json.dump(results, f, indent=2)
        console.print(f"💾 Results saved to {output}")