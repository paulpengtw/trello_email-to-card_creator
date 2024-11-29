# Trello Card Creator Setup Guide

This guide explains how to set up and configure the Trello Card Creator on mac.

## Prerequisites

- Python 3.x installed
- Access to terminal/command line
- Zsh shell (default on modern macOS)

## Installation Steps

1. Clone the repository or download the project files to your local machine.

2. Make the main script executable:
   ```bash
   chmod +x main.py
   ```

3. Add the command alias to your shell:
   - Open your `.zshrc` file:
     ```bash
     nano ~/.zshrc
     ```
   - Add the following line (replace the path with your actual project path):
     ```bash
     alias trello='/path/to/project/directory/trello'
     ```
   - Save and exit (in nano: Ctrl+X, then Y, then Enter)
   - Reload your shell configuration:
     ```bash
     source ~/.zshrc
     ```

## Virtual Environment

The script will automatically:
- Create a virtual environment in the project directory (`./venv`)
- Install required dependencies from `requirements.txt`
- Activate the virtual environment when needed

You don't need to manually manage the virtual environment - the script handles this for you.

## Usage

After setup, you can create Trello cards from anywhere in your terminal by simply typing:
```bash
trello
```

## Troubleshooting

If the `trello` command isn't working:
1. Make sure you've reloaded your shell configuration (`source ~/.zshrc`)
2. Verify that the path in your alias matches your actual project location
3. Ensure `main.py` has execute permissions
4. Check that Python 3 is installed and accessible via `python3` command
