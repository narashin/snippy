import os

import click

# Base Directory
BASE_DIR = os.path.expanduser("~/.snippy")

# File Paths
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
VERSION_CACHE_PATH = os.path.join(BASE_DIR, "installed_version.json")
LATEST_VERSION_PATH = os.path.join(BASE_DIR, "latest_version.json")
CACHE_EXPIRATION_TIME = 60 * 60 * 6  # 6 hours

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
