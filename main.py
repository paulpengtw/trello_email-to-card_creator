#!/usr/bin/env python3
import os
import sys
import subprocess
import platform

def init_venv():
    venv_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv')
    if not os.path.exists(venv_dir):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, '-m', 'venv', venv_dir])
        
        # Determine the pip path based on the platform
        pip_path = os.path.join(venv_dir, 'bin' if platform.system() != 'Windows' else 'Scripts', 'pip')
        
        print("Installing requirements...")
        subprocess.check_call([pip_path, 'install', '-r', 'requirements.txt'])
        print("Virtual environment setup complete!")

# Activate virtual environment
venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv', 'bin', 'activate_this.py')
if not os.path.exists(venv_path):
    init_venv()
elif os.path.exists(venv_path):
    with open(venv_path) as file:
        exec(file.read(), dict(__file__=venv_path))

import os
import pickle
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import click
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich import print as rprint
import yaml
import os.path

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
console = Console()

def load_config():
    """Load configuration from config.yml."""
    config_path = os.path.join(os.path.dirname(__file__), 'config.yml')
    if not os.path.exists(config_path):
        console.print("[red]Error: config.yml not found. Please create it with your Trello settings.[/red]")
        exit(1)
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_gmail_service():
    """Get or create Gmail API service."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, message_text, cc=None):
    """Create a message for an email."""
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    if cc:
        message['cc'] = cc
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def format_trello_subject(title, labels):
    """Format the subject line with Trello labels."""
    if not labels:
        return title
    label_str = ' '.join(labels)
    return f'{title} {label_str}'

@click.group()
def cli():
    """Trello Card Creator - Create Trello cards via email."""
    pass

@cli.command()
def new():
    """Interactive prompt to create a Trello card."""
    config = load_config()
    trello_config = config['trello']

    # Display welcome message
    console.print("[bold blue]Welcome to Trello Card Creator![/bold blue]")
    console.print("Let's create a new card for your board.\n")

    # Get card title
    title = Prompt.ask("[bold]Enter card title[/bold]")

    # Display available labels
    console.print("\n[bold]Available labels:[/bold]")
    label_options = list(trello_config['labels'].items())
    for idx, (label_name, label_value) in enumerate(label_options, 1):
        console.print(f"{idx}. {label_name} ({label_value})")

    # Select one label
    label_idx = Prompt.ask(
        "\nSelect label number", 
        choices=[str(i) for i in range(1, len(label_options) + 1)]
    )
    label_name, label_value = label_options[int(label_idx) - 1]
    selected_labels = [label_value]
    console.print(f"Selected label: {label_name}")

    # Get card description
    console.print("\n[bold]Enter card description[/bold] (press Enter twice to finish):")
    description_lines = []
    while True:
        line = input()
        if line == "" and (not description_lines or description_lines[-1] == ""):
            break
        description_lines.append(line)
    description = "\n".join(description_lines[:-1])

    # Format subject with labels
    subject = format_trello_subject(title, selected_labels)

    # Select CC members
    cc_members = []
    if trello_config['cc_members']:
        console.print("\n[bold]Available members to CC:[/bold]")
        cc_options = list(enumerate(trello_config['cc_members'], 1))
        for idx, member in cc_options:
            console.print(f"{idx}. {member}")
        
        member_idx = Prompt.ask(
            "\nSelect member number to CC", 
            choices=[str(i) for i in range(1, len(cc_options) + 1)]
        )
        cc_members = [cc_options[int(member_idx) - 1][1]]

    # Show confirmation
    console.print("\n[bold yellow]Please review your card details:[/bold yellow]")
    console.print(f"[bold]Title:[/bold] {title}")
    console.print(f"[bold]Labels:[/bold] {', '.join(selected_labels)}")
    console.print(f"[bold]Description:[/bold]\n{description}")
    console.print(f"[bold]Board Email:[/bold] {trello_config['board_email']}")
    if cc_members:
        console.print(f"[bold]CC'd Members:[/bold] {', '.join(cc_members)}")

    if not Confirm.ask("\n[bold]Send this card to Trello?[/bold]", default=True):
        console.print("[yellow]Card creation cancelled.[/yellow]")
        return

    # Send email to create card
    try:
        service = get_gmail_service()
        user_info = service.users().getProfile(userId='me').execute()
        sender = user_info['emailAddress']
        
        message = create_message(
            sender=sender,
            to=trello_config['board_email'],
            subject=subject,
            message_text=description,
            cc=', '.join(cc_members) if cc_members else None
        )
        
        sent_message = service.users().messages().send(
            userId='me', body=message).execute()
        
        console.print("\n[green]✓ Trello card created successfully![/green]")
        
    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {str(e)}")

if __name__ == '__main__':
    cli()
