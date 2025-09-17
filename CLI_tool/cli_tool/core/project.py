"""
Project management and configuration for pentestctl.
"""

import os
import json
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any

import click
import yaml
from rich.console import Console
from sqlmodel import SQLModel, create_engine, Session

console = Console()

class ProjectManager:
    """Manages pentestctl projects and profiles."""
    
    def __init__(self, project_name: str = None):
        self.project_name = project_name
        self.project_dir = Path.cwd() / ".pentestctl" if not project_name else Path.cwd() / f".pentestctl-{project_name}"
        self.db_path = self.project_dir / "project.db"
        self.config_path = self.project_dir / "config.yaml"
        
    def init_project(self, scope_file: Optional[str] = None, config: Optional[Dict] = None):
        """Initialize a new pentestctl project."""
        try:
            self.project_dir.mkdir(parents=True, exist_ok=True)
            
            # Create project database
            engine = create_engine(f"sqlite:///{self.db_path}")
            SQLModel.metadata.create_all(engine)
            
            # Create default config
            default_config = {
                "project": {
                    "name": self.project_name or "default",
                    "created": str(Path.cwd()),
                    "scope_file": scope_file
                },
                "tools": {
                    "nmap": {"default_flags": "-sS -sV -O"},
                    "theharvester": {"default_source": "google", "default_limit": 100}
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

@click.group()
def profile():
    """Manage pentestctl profiles."""
    pass

@profile.command("create")
@click.option("--name", "-n", required=True, help="Profile name")
@click.option("--config", "-c", help="Config file path")
def create_profile(name, config):
    """Create a new profile."""
    console.print(f"🔧 Creating profile: {name}")
    # TODO: Implement profile creation logic
    console.print("✅ Profile created successfully")

@profile.command("list")
def list_profiles():
    """List all profiles."""
    console.print("📋 Available profiles:")
    # TODO: Implement profile listing
    console.print("• default")