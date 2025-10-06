"""
AI integration module for pentestctl.
"""

import click
import json
import os
from pathlib import Path
import google.generativeai as genai
from rich.console import Console
from cli_tool.core.project import ProjectManager

console = Console()

@click.group()
def ai():
    """AI-powered analysis commands."""
    pass

@ai.command()
@click.option("--input", "-i", required=True, help="Input file to summarize")
@click.option("--length", "-l", default="medium", help="Summary length")
def summarize(input, length):
    """AI-powered summarization of scan results."""
    console.print(f"🤖 Summarizing {input}")
    console.print("⚠️  AI module not fully implemented yet")
    # TODO: Implement AI summarization

@ai.command()
@click.option("--input", "-i", required=True, help="Input vulnerabilities")
def triage(input):
    """AI-powered vulnerability triage."""
    console.print(f"🧠 Triaging vulnerabilities from {input}")
    console.print("⚠️  AI triage not fully implemented yet")
    # TODO: Implement AI triage

@ai.command()
@click.argument("question")
def ask(question):
    """Ask AI assistant a question."""
    console.print(f"💭 Question: {question}")
    console.print("⚠️  AI assistant not fully implemented yet")
    # TODO: Implement AI Q&A

def load_api_key():
    """Load API key from environment or .env file."""
    # Check environment variable first
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return api_key
    
    # Check .env file in project root
    env_path = Path(__file__).parent.parent.parent / ".env"
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    return line.strip().split("=", 1)[1]
    
    return None

@ai.command()
@click.option("--project", "-p", required=True, help="Project name to generate report for")
@click.option("--output", "-o", default="report.md", help="Output file for the report")
@click.option("--api-key", "-k", help="Gemini API key (or set GEMINI_API_KEY environment variable)")
def report(project, output, api_key):
    """Generate a pentesting report from project findings using Gemini AI."""
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
        console.print("🤖 Generating report with Gemini AI...")
        response = model.generate_content(prompt)
        
        # Save report to file
        with open(output, 'w') as f:
            f.write(response.text)
        
        console.print(f"✅ Report generated successfully and saved to {output}")
        
    except Exception as e:
        console.print(f"❌ Failed to generate report: {e}")
