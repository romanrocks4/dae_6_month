"""
Report generation module for pentestctl.
"""

import click
import json
import os
from rich.console import Console
from pathlib import Path
from cli_tool.core.project import ProjectManager

console = Console()

@click.group()
def report():
    """Report generation commands."""
    pass

def load_api_key():
    """Load API key from environment or .env file."""
    import sys
    from pathlib import Path
    
    # Check environment variable first
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return api_key
    
    # Check .env file in project root
    # Try multiple possible locations for the .env file
    project_root = Path(__file__).parent.parent.parent
    possible_paths = [
        project_root / ".env",  # Project root
        Path.cwd() / ".env",    # Current working directory
        Path.home() / ".env",   # Home directory
    ]
    
    # Remove duplicates and non-existent paths
    unique_paths = []
    for path in possible_paths:
        if path not in unique_paths and path.exists():
            unique_paths.append(path)
    
    for env_path in unique_paths:
        try:
            with open(env_path, 'r') as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        key = line.strip().split("=", 1)[1]
                        return key
        except Exception as e:
            print(f"Error reading .env file: {e}", file=sys.stderr)
    
    return None

@report.command()
@click.option("--project", "-p", required=True, help="Project name to generate report for")
@click.option("--output", "-o", default="report.md", help="Output file for the report")
@click.option("--api-key", "-k", help="Gemini API key (or set GEMINI_API_KEY environment variable)")
def generate(project, output, api_key):
    """Generate a pentesting report from project findings using AI."""
    # Try to import Google Generative AI
    try:
        import google.generativeai as genai
    except ImportError:
        console.print("❌ Google Generative AI library not available. Install with: pip install google-generativeai")
        return
    
    # Get API key from parameter, environment variable, or .env file
    gemini_api_key = api_key or load_api_key()
    if not gemini_api_key:
        console.print("❌ Gemini API key not provided. Set GEMINI_API_KEY in environment, .env file, or use --api-key option.")
        return
    
    # Initialize Gemini
    try:
        genai.configure(api_key=gemini_api_key)
        # Use a working model
        model = genai.GenerativeModel('gemini-2.0-flash')
    except Exception as e:
        console.print(f"❌ Failed to initialize Gemini: {e}")
        return
    
    # Get project findings
    pm = ProjectManager(project)
    findings = pm.get_all_findings()
    
    if not findings:
        console.print("⚠️  No findings found in the project.")
        return
    
    # Prepare the data for the AI
    console.print("🔍 Analyzing project findings...")
    project_data = {
        "project_name": project,
        "findings_count": len(findings),
        "findings": findings
    }
    
    # Create prompt for report generation
    prompt = f"""
    You are a professional penetration tester and security expert. Based on the following penetration testing findings, 
    create a comprehensive security report with the following structure:
    
    1. Executive Summary
    2. Methodology
    3. Findings Analysis
    4. Risk Assessment
    5. Recommendations
    6. Conclusion
    
    For each finding, include:
    - Description of the issue
    - Risk level (Critical, High, Medium, Low)
    - Technical details
    - Impact assessment
    - Remediation steps
    
    Project Data:
    {json.dumps(project_data, indent=2)}
    
    Please provide a professional, detailed security report in Markdown format.
    """
    
    try:
        # Generate report using Gemini
        console.print("🤖 Generating report with AI...")
        response = model.generate_content(prompt)
        
        # Save report to file
        with open(output, 'w') as f:
            f.write(response.text)
        
        console.print(f"✅ Report generated successfully and saved to {output}")
        
    except Exception as e:
        console.print(f"❌ Failed to generate report: {e}")

@report.command()
@click.option("--template", "-t", default="standard", help="Report template")
@click.option("--format", "-f", default="text", help="Output format")
@click.option("--output", "-o", help="Output file")
def template(template, format, output):
    """Generate pentest report from template."""
    console.print(f"📄 Generating {format} report using {template} template")
    console.print("⚠️  Template-based report generation not fully implemented yet")
    # TODO: Implement template-based report generation