"""
AI integration module for pentestctl.
"""

import click
import json
import os
from pathlib import Path
from datetime import datetime
import google.generativeai as genai
from rich.console import Console
from cli_tool.core.project import ProjectManager

console = Console()

@click.group()
def ai():
    """AI-powered analysis commands."""
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

def get_last_command_output():
    """Get the output from the last pentestctl command."""
    # Try to get output from a temporary file where last command output is stored
    temp_output_file = Path(__file__).parent.parent.parent / ".pentestctl_last_output"
    if temp_output_file.exists():
        try:
            with open(temp_output_file, 'r') as f:
                return f.read()
        except Exception:
            pass
    return None

@ai.command()
@click.argument("input", type=click.STRING, required=False)
@click.option("--length", "-l", default="medium", help="Summary length")
def summarize(input, length):
    """AI-powered summarization of scan results.
    
    INPUT: Path to input file or '.' to use output from last command.
    """
    # Handle the special case of "." for last command output
    if input == ".":
        scan_data = get_last_command_output()
        if not scan_data:
            console.print("❌ No previous command output found. Run a command first or specify an input file.")
            return
        console.print("🔍 Using output from last command...")
    elif input:
        # Read from specified input file
        try:
            with open(input, 'r') as f:
                scan_data = f.read()
        except Exception as e:
            console.print(f"❌ Failed to read input file: {e}")
            return
    else:
        console.print("❌ Please specify an input file or use '.' for last command output.")
        return
    
    # Load API key
    gemini_api_key = load_api_key()
    if not gemini_api_key:
        console.print("❌ Gemini API key not provided. Set GEMINI_API_KEY in environment, .env file, or use --api-key option.")
        return
    
    try:
        # Initialize Gemini
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
    except Exception as e:
        console.print(f"❌ Failed to initialize Gemini: {e}")
        return
    
    # Map length option to descriptive text
    length_desc = {
        "short": "brief",
        "medium": "detailed but concise",
        "long": "comprehensive"
    }.get(length, "detailed")
    
    # Create prompt for summarization
    prompt = f"""
    You are a professional penetration tester and security expert. Please provide a {length_desc} summary of the following scan results.
    
    Scan Data:
    {scan_data}
    
    Please structure your summary with the following sections:
    
    ## Executive Summary
    - Overall security posture assessment
    - Key findings and risks identified
    
    ## Technical Overview
    - Types of scans performed
    - Scope of assessment
    - Methodology summary
    
    ## Critical Findings
    - Most severe vulnerabilities or issues
    - Immediate risk assessment
    
    ## Recommendations
    - Prioritized actions to address findings
    - Best practices for remediation
    
    Keep the summary focused on the most important security implications and actionable insights.
    """
    
    try:
        console.print(f"🤖 Summarizing scan results ({length} length)...")
        response = model.generate_content(prompt)
        
        # Save summary to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"summary_{timestamp}.md"
        with open(output_file, 'w') as f:
            f.write(response.text)
        
        console.print("✅ Summary generated successfully!")
        console.print(f"📄 Summary saved to {output_file}")
        console.print("\n📋 Summary preview:")
        console.print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
        
    except Exception as e:
        console.print(f"❌ Failed to generate summary: {e}")

@ai.command()
@click.argument("input", type=click.STRING, required=False)
def triage(input):
    """AI-powered vulnerability triage.
    
    INPUT: Path to input file or '.' to use output from last command.
    """
    # Handle the special case of "." for last command output
    if input == ".":
        vulnerabilities_data = get_last_command_output()
        if not vulnerabilities_data:
            console.print("❌ No previous command output found. Run a command first or specify an input file.")
            return
        console.print("🔍 Using output from last command...")
    elif input:
        # Read from specified input file
        try:
            with open(input, 'r') as f:
                vulnerabilities_data = f.read()
        except Exception as e:
            console.print(f"❌ Failed to read input file: {e}")
            return
    else:
        console.print("❌ Please specify an input file or use '.' for last command output.")
        return
    
    # Load API key
    gemini_api_key = load_api_key()
    if not gemini_api_key:
        console.print("❌ Gemini API key not provided. Set GEMINI_API_KEY in environment, .env file, or use --api-key option.")
        return
    
    try:
        # Initialize Gemini
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
    except Exception as e:
        console.print(f"❌ Failed to initialize Gemini: {e}")
        return
    
    # Create prompt for vulnerability triage
    prompt = f"""
    You are a professional cybersecurity expert specializing in vulnerability assessment and risk management. 
    Please analyze the following vulnerability data and provide a prioritized triage assessment.
    
    Vulnerability Data:
    {vulnerabilities_data}
    
    Please provide your analysis in the following format:
    
    ## Vulnerability Triage Report
    
    ### Critical Priority (Immediate Action Required)
    - List vulnerabilities that require immediate attention with brief justification
    
    ### High Priority (Address Within 24-72 Hours)
    - List high priority vulnerabilities with brief justification
    
    ### Medium Priority (Address Within 1 Week)
    - List medium priority vulnerabilities with brief justification
    
    ### Low Priority (Address During Next Maintenance Window)
    - List low priority vulnerabilities with brief justification
    
    ### Summary Recommendations
    - Overall risk assessment
    - Recommended remediation approach
    - Any additional security considerations
    
    For each vulnerability, include:
    - CVE ID (if applicable)
    - Risk level justification
    - Potential impact
    - Recommended remediation steps
    """
    
    try:
        console.print("🧠 Analyzing vulnerabilities with Gemini AI...")
        response = model.generate_content(prompt)
        
        # Save triage report to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"triage_report_{timestamp}.md"
        with open(output_file, 'w') as f:
            f.write(response.text)
        
        console.print("✅ Vulnerability triage completed successfully!")
        console.print(f"📄 Triage report saved to {output_file}")
        console.print("\n📊 Summary of findings:")
        console.print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
        
    except Exception as e:
        console.print(f"❌ Failed to triage vulnerabilities: {e}")

@ai.command()
@click.argument("question", nargs=-1)
@click.option("--length", "-l", default="short", help="Response length (short, medium, long)")
def ask(question, length):
    """Ask AI assistant a question."""
    # Join the question words into a single string
    question_text = " ".join(question)
    
    # Load API key
    gemini_api_key = load_api_key()
    if not gemini_api_key:
        console.print("❌ Gemini API key not provided. Set GEMINI_API_KEY in environment, .env file, or use --api-key option.")
        return
    
    try:
        # Initialize Gemini
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
    except Exception as e:
        console.print(f"❌ Failed to initialize Gemini: {e}")
        return
    
    # Map length option to descriptive text
    length_desc = {
        "short": "brief and direct",
        "medium": "detailed but concise",
        "long": "comprehensive with examples"
    }.get(length, "brief and direct")
    
    # Create prompt for the question
    prompt = f"""
    You are a professional cybersecurity expert and penetration tester. 
    Please answer the following question {length_desc}.
    
    Question: {question_text}
    
    Provide a {length_desc} answer without unnecessary formatting.
    """
    
    try:
        console.print(f"💭 Processing question: {question_text}")
        response = model.generate_content(prompt)
        
        console.print("✅ Response:")
        console.print(response.text.strip())
        
    except Exception as e:
        console.print(f"❌ Failed to get response: {e}")


