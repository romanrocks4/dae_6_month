"""
Scanning module for pentestctl.
"""

import click
import subprocess
import json
import xml.etree.ElementTree as ET
from rich.console import Console
from rich.table import Table
from typing import Dict, Any
from cli_tool.core.project import ProjectManager
from pathlib import Path

console = Console()

def run_nmap(target: str, ports: str = "1-1000", flags: str = "-sV") -> Dict[str, Any]:
    """Run Nmap scan against target."""
    console.print(f"🔍 Running Nmap scan on {target} (ports: {ports})")
    
    try:
        # Build the Nmap command
        # Split flags into separate arguments
        flag_list = flags.split()
        cmd = ["nmap", "-oX", "-"] + flag_list + ["-p", ports, target]
        
        # Run Nmap
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            # Parse XML output
            try:
                # Parse the XML output
                root = ET.fromstring(result.stdout)
                
                # Extract scan information
                scan_info = {
                    "nmap_version": root.get("version", "Unknown"),
                    "start_time": root.get("startstr", "Unknown"),
                    "scan_args": root.get("args", "Unknown"),
                }
                
                # Extract host information
                hosts = []
                for host in root.findall("host"):
                    host_info = {
                        "address": "",
                        "hostname": "",
                        "status": "",
                        "ports": []
                    }
                    
                    # Get address
                    addr_elem = host.find("address")
                    if addr_elem is not None:
                        host_info["address"] = addr_elem.get("addr", "Unknown")
                    
                    # Get hostname
                    hostnames_elem = host.find("hostnames")
                    if hostnames_elem is not None:
                        hostname_elem = hostnames_elem.find("hostname")
                        if hostname_elem is not None:
                            host_info["hostname"] = hostname_elem.get("name", "Unknown")
                    
                    # Get status
                    status_elem = host.find("status")
                    if status_elem is not None:
                        host_info["status"] = status_elem.get("state", "Unknown")
                    
                    # Get ports
                    ports_elem = host.find("ports")
                    if ports_elem is not None:
                        for port_elem in ports_elem.findall("port"):
                            port_info = {
                                "port": port_elem.get("portid", "Unknown"),
                                "protocol": port_elem.get("protocol", "Unknown"),
                                "state": "Unknown",
                                "service": "Unknown",
                                "version": ""
                            }
                            
                            # Get port state
                            state_elem = port_elem.find("state")
                            if state_elem is not None:
                                port_info["state"] = state_elem.get("state", "Unknown")
                            
                            # Get service info
                            service_elem = port_elem.find("service")
                            if service_elem is not None:
                                port_info["service"] = service_elem.get("name", "Unknown")
                                product = service_elem.get("product", "")
                                version = service_elem.get("version", "")
                                if product and version:
                                    port_info["version"] = f"{product} {version}"
                                elif product:
                                    port_info["version"] = product
                                elif version:
                                    port_info["version"] = version
                            
                            host_info["ports"].append(port_info)
                    
                    hosts.append(host_info)
                
                return {
                    "status": "success",
                    "scan_info": scan_info,
                    "hosts": hosts,
                    "raw_output": result.stdout
                }
            except ET.ParseError as e:
                return {
                    "status": "error",
                    "error": f"Failed to parse Nmap XML output: {str(e)}",
                    "hosts": []
                }
        else:
            error_msg = result.stderr.strip() if result.stderr.strip() else "Nmap execution failed"
            return {
                "status": "error", 
                "error": error_msg,
                "hosts": []
            }
            
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout", 
            "error": "Nmap timed out after 10 minutes",
            "hosts": []
        }
    except FileNotFoundError:
        return {
            "status": "error", 
            "error": "Nmap not found. Install with: brew install nmap (macOS) or apt install nmap (Linux)",
            "hosts": []
        }
    except Exception as e:
        return {
            "status": "error", 
            "error": f"Unexpected error: {str(e)}",
            "hosts": []
        }

def display_nmap_results(results: Dict[str, Any]):
    """Display Nmap scan results in a nice table."""
    if results.get("status") != "success":
        console.print(f"❌ Nmap scan failed: {results.get('error', 'Unknown error')}")
        return
    
    scan_info = results.get("scan_info", {})
    hosts = results.get("hosts", [])
    
    # Display scan summary
    console.print(f"\n📊 Nmap Scan Summary:")
    console.print(f"   Nmap Version: {scan_info.get('nmap_version', 'Unknown')}")
    console.print(f"   Start Time: {scan_info.get('start_time', 'Unknown')}")
    
    # Display host information
    for host in hosts:
        console.print(f"\n🖥️  Host: {host.get('address', 'Unknown')} ({host.get('hostname', 'No hostname')})")
        console.print(f"   Status: {host.get('status', 'Unknown')}")
        
        # Display open ports
        open_ports = [port for port in host.get("ports", []) if port.get("state") == "open"]
        if open_ports:
            port_table = Table(title="Open Ports")
            port_table.add_column("Port", style="cyan")
            port_table.add_column("Protocol", style="magenta")
            port_table.add_column("Service", style="green")
            port_table.add_column("Version", style="yellow")
            
            for port in open_ports:
                port_table.add_row(
                    port.get("port", "Unknown"),
                    port.get("protocol", "Unknown"),
                    port.get("service", "Unknown"),
                    port.get("version", "")
                )
            
            console.print(port_table)
        else:
            console.print("   🔒 No open ports found")

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

@click.group()
def scan():
    """Network scanning commands."""
    pass

@scan.command()
@click.option("--target", "-t", required=True, help="Target IP or domain")
@click.option("--modules", "-m", default="nmap", help="Scanning modules (nmap, masscan)")
@click.option("--ports", "-p", default="1-1000", help="Port range")
@click.option("--flags", "-f", default="-sV", help="Nmap flags (default: -sV for version detection)")
@click.option("--output", "-o", help="Output file path (JSON format)")
@click.option("--project", "-p", help="Project name to save results to")
def run(target, modules, ports, flags, output, project):
    """Run network scan against target."""
    console.print(f"🔍 Starting scan on {target}")
    
    module_list = [m.strip() for m in modules.split(',')]
    results = {}
    
    for module in module_list:
        if module == "nmap":
            results[module] = run_nmap(target, ports, flags)
            display_nmap_results(results[module])
        elif module == "masscan":
            console.print(f"⚠️  Masscan module not fully implemented yet for {target}")
            results[module] = {"status": "not_implemented", "hosts": []}
        else:
            console.print(f"⚠️  Unknown module: {module}")
            results[module] = {"status": "unknown", "hosts": []}
    
    # Save results to project if specified
    if project:
        pm = ProjectManager(project)
        pm.save_finding("nmap", target, results)
    
    # Save results to file if output specified
    if output:
        with open(output, 'w') as f:
            json.dump(results, f, indent=2)
        console.print(f"💾 Results saved to {output}")
    
    # Save output to temporary file for AI module
    save_output_for_ai(results)