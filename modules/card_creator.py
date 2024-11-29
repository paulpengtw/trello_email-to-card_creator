"""
Trello card creation module.
"""
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table

class CardCreator:
    """Handles the creation of Trello cards via email."""
    
    def __init__(self, config, gmail_service):
        self.config = config['trello']
        self.gmail_service = gmail_service
        self.console = Console()
    
    def _format_trello_subject(self, title, labels):
        """Format the subject line with Trello labels."""
        if not labels:
            return title
        label_str = ' '.join(labels)
        return f'{title} {label_str}'
    
    def _get_card_details(self):
        """Interactively get card details from user."""
        self.console.print("[bold blue]Welcome to Trello Card Creator![/bold blue]")
        self.console.print("Let's create a new card for your board.\n")

        # Get card title
        title = Prompt.ask("[bold]Enter card title[/bold]")

        # Display and select labels
        self.console.print("\n[bold]Available labels:[/bold]")
        label_options = list(self.config['labels'].items())
        for idx, (label_name, label_value) in enumerate(label_options, 1):
            self.console.print(f"{idx}. {label_name} ({label_value})")

        label_idx = Prompt.ask(
            "\nSelect label number",
            choices=[str(i) for i in range(1, len(label_options) + 1)]
        )
        label_name, label_value = label_options[int(label_idx) - 1]
        selected_labels = [label_value]
        self.console.print(f"Selected label: {label_name}")

        # Get description
        self.console.print("\n[bold]Enter card description[/bold] (press Enter twice to finish):")
        description_lines = []
        while True:
            line = input()
            if line == "" and (not description_lines or description_lines[-1] == ""):
                break
            description_lines.append(line)
        description = "\n".join(description_lines[:-1])

        # Select CC members
        cc_members = []
        if self.config['cc_members']:
            self.console.print("\n[bold]Available members to CC:[/bold]")
            cc_options = list(enumerate(self.config['cc_members'], 1))
            for idx, member in cc_options:
                self.console.print(f"{idx}. {member}")
            
            member_idx = Prompt.ask(
                "\nSelect member number to CC",
                choices=[str(i) for i in range(1, len(cc_options) + 1)]
            )
            cc_members = [cc_options[int(member_idx) - 1][1]]

        return {
            'title': title,
            'labels': selected_labels,
            'description': description,
            'cc_members': cc_members
        }
    
    def _display_confirmation(self, details):
        """Display card details for confirmation."""
        self.console.print("\n[bold yellow]Please review your card details:[/bold yellow]")
        self.console.print(f"[bold]Title:[/bold] {details['title']}")
        self.console.print(f"[bold]Labels:[/bold] {', '.join(details['labels'])}")
        self.console.print(f"[bold]Description:[/bold]\n{details['description']}")
        self.console.print(f"[bold]Board Email:[/bold] {self.config['board_email']}")
        if details['cc_members']:
            self.console.print(f"[bold]CC'd Members:[/bold] {', '.join(details['cc_members'])}")
    
    def new(self):
        """Interactive prompt to create a Trello card."""
        try:
            # Get card details
            details = self._get_card_details()
            
            # Show confirmation
            self._display_confirmation(details)
            
            if not Confirm.ask("\n[bold]Send this card to Trello?[/bold]", default=True):
                self.console.print("[yellow]Card creation cancelled.[/yellow]")
                return

            # Create and send email
            subject = self._format_trello_subject(details['title'], details['labels'])
            message = self.gmail_service.create_message(
                to=self.config['board_email'],
                subject=subject,
                message_text=details['description'],
                cc=', '.join(details['cc_members']) if details['cc_members'] else None
            )
            
            self.gmail_service.send_message(message)
            self.console.print("\n[green]✓ Trello card created successfully![/green]")
            
        except Exception as e:
            self.console.print(f"[red]An error occurred:[/red] {str(e)}")
