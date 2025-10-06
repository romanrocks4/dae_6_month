"""
Project management and configuration for pentestctl.
"""

import os
import json
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

import click
import yaml
from rich.console import Console
from sqlmodel import SQLModel, create_engine, Session, Field, Relationship
from typing import List, Optional

console = Console()

# Define the profiles directory
PROFILES_DIR = Path.home() / ".pentestctl" / "profiles"

class Project(SQLModel, table=True):
    """Project model for storing project information."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    scope_file: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    findings: List["Finding"] = Relationship(back_populates="project")

class Finding(SQLModel, table=True):
    """Finding model for storing scan results and vulnerabilities."""
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    tool: str  # e.g., "nmap", "theharvester", "trivy"
    target: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    data: str  # JSON string of the raw results
    project: Optional[Project] = Relationship(back_populates="findings")

class ProjectManager:
    """Manages pentestctl projects and profiles."""
    
    def __init__(self, project_name: Optional[str] = None):
        self.project_name = project_name
        self.project_dir = Path.cwd() / ".pentestctl" if not project_name else Path.cwd() / f".pentestctl-{project_name}"
        self.db_path = self.project_dir / "project.db"
        self.config_path = self.project_dir / "config.yaml"
        self.findings_dir = self.project_dir / "findings"
        
    def init_project(self, scope_file: Optional[str] = None, config: Optional[Dict] = None):
        """Initialize a new pentestctl project."""
        try:
            self.project_dir.mkdir(parents=True, exist_ok=True)
            self.findings_dir.mkdir(parents=True, exist_ok=True)
            
            # Create project database
            engine = create_engine(f"sqlite:///{self.db_path}")
            SQLModel.metadata.create_all(engine)
            
            # Create default config
            default_config = {
                "project": {
                    "name": self.project_name or "default",
                    "created": str(datetime.now()),
                    "scope_file": scope_file
                },
                "tools": {
                    "nmap": {"default_flags": "-sV"},
                    "theharvester": {"default_source": "duckduckgo", "default_limit": 100}
                },
                "ai": {
                    "enabled": True,
                    "provider": "openai",
                    "offsite": False,
                    "model": "gpt-3.5-turbo"
                },
                "safety": {
                    "scope_check": True,
                    "excluded_networks": ["127.0.0.0/8", "10.0.0.0/8"]
                }
            }
            
            if config:
                default_config.update(config)
                
            with open(self.config_path, 'w') as f:
                yaml.dump(default_config, f, default_flow_style=False)
                
            # Create initial project record in database
            with Session(engine) as session:
                existing_project = session.query(Project).filter(Project.name == (self.project_name or "default")).first()
                if not existing_project:
                    project = Project(
                        name=self.project_name or "default",
                        scope_file=scope_file
                    )
                    session.add(project)
                    session.commit()
                
            console.print(f"✅ Project '{self.project_name or 'default'}' initialized in {self.project_dir}")
            return True
            
        except Exception as e:
            console.print(f"❌ Failed to initialize project: {e}")
            return False
    
    def load_config(self) -> Dict[str, Any]:
        """Load project configuration."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def save_finding(self, tool: str, target: str, data: Dict[str, Any]):
        """Save a finding to the project database."""
        try:
            engine = create_engine(f"sqlite:///{self.db_path}")
            with Session(engine) as session:
                # Get the project
                project = session.query(Project).filter(Project.name == (self.project_name or "default")).first()
                if not project:
                    # Create project if it doesn't exist
                    project = Project(name=self.project_name or "default")
                    session.add(project)
                    session.commit()
                    session.refresh(project)
                
                # Create finding
                finding = Finding(
                    project_id=project.id,
                    tool=tool,
                    target=target,
                    data=json.dumps(data)
                )
                session.add(finding)
                session.commit()
                
            console.print(f"💾 Finding saved for {tool} scan on {target}")
            return True
        except Exception as e:
            console.print(f"❌ Failed to save finding: {e}")
            return False
    
    def get_all_findings(self) -> List[Dict[str, Any]]:
        """Retrieve all findings for this project."""
        try:
            # Check if project directory exists
            if not self.project_dir.exists():
                console.print(f"⚠️  Project directory does not exist: {self.project_dir}")
                return []
            
            # Check if database file exists
            if not self.db_path.exists():
                console.print(f"⚠️  Project database does not exist: {self.db_path}")
                return []
            
            engine = create_engine(f"sqlite:///{self.db_path}")
            with Session(engine) as session:
                project = session.query(Project).filter(Project.name == (self.project_name or "default")).first()
                if not project:
                    return []
                
                findings = session.query(Finding).filter(Finding.project_id == project.id).all()
                return [
                    {
                        "id": finding.id,
                        "tool": finding.tool,
                        "target": finding.target,
                        "timestamp": finding.timestamp.isoformat(),
                        "data": json.loads(finding.data)
                    }
                    for finding in findings
                ]
        except Exception as e:
            console.print(f"❌ Failed to retrieve findings: {e}")
            return []

def create_profile(name: str, config: Optional[str] = None):
    """Create a new profile."""
    # Create profiles directory if it doesn't exist
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    
    # Define profile file path
    profile_file = PROFILES_DIR / f"{name}.yaml"
    
    # Check if profile already exists
    if profile_file.exists():
        console.print(f"⚠️  Profile '{name}' already exists")
        return False
    
    # Create default profile config
    profile_config = {
        "name": name,
        "created": str(datetime.now()),
        "tools": {
            "nmap": {"default_flags": "-sV"},
            "theharvester": {"default_source": "duckduckgo", "default_limit": 100}
        },
        "ai": {
            "enabled": True,
            "provider": "openai",
            "offsite": False,
            "model": "gpt-3.5-turbo"
        },
        "safety": {
            "scope_check": True,
            "excluded_networks": ["127.0.0.0/8", "10.0.0.0/8"]
        }
    }
    
    # Load custom config if provided
    if config and os.path.exists(config):
        with open(config, 'r') as f:
            custom_config = yaml.safe_load(f)
            profile_config.update(custom_config)
    
    # Save profile
    try:
        with open(profile_file, 'w') as f:
            yaml.dump(profile_config, f, default_flow_style=False)
        console.print(f"✅ Profile '{name}' created successfully")
        return True
    except Exception as e:
        console.print(f"❌ Failed to create profile: {e}")
        return False

def list_profiles():
    """List all profiles."""
    # Create profiles directory if it doesn't exist
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    
    console.print("📋 Available profiles:")
    
    # Always show default profile
    console.print("• default")
    
    # List all YAML files in profiles directory
    profiles = list(PROFILES_DIR.glob("*.yaml"))
    
    # Show custom profiles
    for profile in profiles:
        profile_name = profile.stem  # Get filename without extension
        if profile_name != "default":
            console.print(f"• {profile_name}")

@click.group()
def init():
    """Initialize a new pentestctl project."""
    pass

@init.command()
@click.option("--project", "-p", help="Project name")
@click.option("--scope", "-s", help="Scope file (targets.txt)")
@click.option("--config", "-c", help="Config file")
def create(project, scope, config):
    """Create a new pentestctl project."""
    config_data = {}
    if config and os.path.exists(config):
        with open(config, 'r') as f:
            config_data = yaml.safe_load(f)
    
    pm = ProjectManager(project)
    pm.init_project(scope, config_data)

@init.command()
@click.option("--project", "-p", help="Project name")
def show(project):
    """Show project details and findings."""
    pm = ProjectManager(project)
    findings = pm.get_all_findings()
    
    console.print(f"📁 Project: {project or 'default'}")
    console.print(f"📍 Findings count: {len(findings)}")
    
    if findings:
        console.print("\n🔍 Findings:")
        for finding in findings:
            console.print(f"  • {finding['tool']} scan on {finding['target']} ({finding['timestamp']})")
    else:
        console.print("  No findings found.")

@click.group()
def profile():
    """Manage pentestctl profiles."""
    pass

@profile.command("create")
@click.option("--name", "-n", required=True, help="Profile name")
@click.option("--config", "-c", help="Config file path")
def create_profile_command(name, config):
    """Create a new profile."""
    console.print(f"🔧 Creating profile: {name}")
    create_profile(name, config)

@profile.command("list")
def list_profiles_command():
    """List all profiles."""
    list_profiles()

@profile.command("show")
@click.option("--name", "-n", required=True, help="Profile name")
def show_profile(name):
    """Show profile details."""
    profile_file = PROFILES_DIR / f"{name}.yaml"
    if not profile_file.exists():
        console.print(f"❌ Profile '{name}' not found")
        return
    
    try:
        with open(profile_file, 'r') as f:
            config = yaml.safe_load(f)
            console.print(f"📄 Profile '{name}' details:")
            console.print(json.dumps(config, indent=2))
    except Exception as e:
        console.print(f"❌ Failed to read profile: {e}")
