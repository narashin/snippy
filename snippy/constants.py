import os

import click

# File paths
CONFIG_PATH = os.path.expanduser("~/.snippy_config.json")

# ANSI Colors
ANSI_GREEN_BOLD = "\033[1;32m"
ANSI_RED_BOLD = "\033[1;31m"
ANSI_RESET = "\033[0m"

# Common Strings
SEPARATOR = "-" * 40

# Styled Texts
NOTE_YELLOW = click.style("Note:", fg="yellow")
ON_GREEN = click.style("on", fg="green")
OFF_RED = click.style("off", fg="red")
OFF_RED = click.style("off", fg="red")

# Commit Types
RAW_COMMIT_TYPES = {
    "feat": ":sparkles:",
    "fix": ":bug:",
    "docs": ":memo:",
    "style": ":lipstick:",
    "refactor": ":recycle:",
    "perf": ":zap:",
    "test": ":white_check_mark:",
    "chore": ":wrench:",
}
