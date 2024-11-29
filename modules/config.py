"""
Configuration management module.
"""
import os
import yaml
from rich.console import Console

console = Console()

def load_config():
    """Load configuration from config.yml."""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yml')
    if not os.path.exists(config_path):
        console.print("[red]Error: config.yml not found. Please create it with your Trello settings.[/red]")
        exit(1)
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)
