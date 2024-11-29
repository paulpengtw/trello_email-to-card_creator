# Trello Card Creator

A command-line tool to create Trello cards via email using Gmail API. This tool allows you to quickly create Trello cards with labels, descriptions, and member assignments directly from your terminal.

## Features

- Create Trello cards via email
- Add labels and assign members
- Interactive command-line interface
- Automatic virtual environment management
- Gmail API integration for sending emails

## Installation

See [SETUP.md](SETUP.md) for detailed installation and configuration instructions. The setup guide covers:
- Installing dependencies
- Configuring your shell environment
- Setting up the `trello` command
- Troubleshooting common issues

## Quick Start

1. Follow the installation steps in [SETUP.md](SETUP.md)
2. Create a new Trello card:
   ```bash
   trello new
   ```

The tool will guide you through:
- Card title and description
- Label selection
- Member assignments
- Additional options

## Configuration

Create a `config.yml` file in the project directory with your Trello settings (or copy and modify `config.yml.example`):
```yaml
trello:
  # Your Trello board's email address
  board_email: your-trello-board-email@board.trello.com

  # Labels with their Trello identifiers
  labels:
    Bug: "#1._Bug"
    Feature: "#2._Feature"
    Documentation: "#3._Documentation"
    # Add more labels as needed

  # Team members to CC (optional)
  cc_members:
    - member1@example.com
    - member2@example.com
    # Add more members as needed
```

## Requirements

- Python 3.x
- Gmail account
- Trello board with email-to-board feature enabled
- Google Cloud Platform project with Gmail API enabled

## License

GPL License
