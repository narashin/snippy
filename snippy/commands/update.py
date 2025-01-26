import json
import os
import subprocess
import threading
import time

import click

from snippy.constants import (
    BASE_DIR,
    CACHE_EXPIRATION_TIME,
    LATEST_VERSION_PATH,
    VERSION_CACHE_PATH,
)
from snippy.utils.animation_utils import show_loading_animation


def save_latest_version(latest_version):
    os.makedirs(BASE_DIR, exist_ok=True)
    with open(LATEST_VERSION_PATH, "w") as f:
        json.dump({"latest_version": latest_version}, f)


def save_installed_version(installed_version):
    os.makedirs(BASE_DIR, exist_ok=True)
    with open(VERSION_CACHE_PATH, "w") as f:
        json.dump({"installed_version": installed_version}, f)


def is_cache_expired(file_path):
    if not os.path.exists(file_path):
        return True
    last_modified = os.path.getmtime(file_path)
    return (time.time() - last_modified) > CACHE_EXPIRATION_TIME


def fetch_latest_version():
    try:
        result = subprocess.run(
            ["brew", "info", "--json=v2", "snippy"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            latest_version = data["formulae"][0]["versions"]["stable"]
            save_latest_version(latest_version)
            return latest_version
        else:
            print(f"Error fetching latest version: {result.stderr}")
    except Exception as e:
        print(f"Failed to fetch the latest version: {e}")
    return None


def fetch_latest_version_in_background():
    def fetch():
        fetch_latest_version()

    thread = threading.Thread(target=fetch, daemon=True)
    thread.start()


def load_latest_version():
    if not os.path.exists(LATEST_VERSION_PATH) or is_cache_expired(LATEST_VERSION_PATH):
        fetch_latest_version_in_background()
        return None
    try:
        with open(LATEST_VERSION_PATH, "r") as f:
            return json.load(f).get("latest_version")
    except FileNotFoundError:
        return None


def fetch_installed_version():
    try:
        result = subprocess.run(
            ["brew", "list", "--versions", "snippy"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            installed_version = result.stdout.strip().split()[1]
            save_installed_version(installed_version)
            return installed_version
        else:
            print(f"Error fetching installed version: {result.stderr}")
    except Exception as e:
        print(f"Failed to fetch the installed version: {e}")
    return None


def fetch_installed_version_with_animation():
    stop_animation = show_loading_animation(
        message="🕵️  Checking for installed version..."
    )
    installed_version = fetch_installed_version()
    stop_animation.set()
    print("\n", end="")
    return installed_version


def load_installed_version():
    try:
        with open(VERSION_CACHE_PATH, "r") as f:
            return json.load(f).get("installed_version")
    except FileNotFoundError:
        return fetch_installed_version()


def check_version():
    installed_version = load_installed_version()
    latest_version = load_latest_version()

    if installed_version or latest_version is None:
        return

    if not installed_version:
        click.echo("Unable to fetch the installed version. 😢")
        return

    if installed_version != latest_version:
        click.echo(
            f"🆕✨ Current installed version: {installed_version}, Latest version: {latest_version} 🤨"
        )
        update = click.prompt("Would you like to update? (y/N)", type=str, default="n")
        if update.lower() == "y":
            subprocess.run(["brew", "upgrade", "snippy"])
            click.echo("Update completed. 🎉")
        else:
            click.echo(
                f"Update cancelled. Run {click.style('`snippy update`', fg='bright_yellow', bold=True)} to update later. 👋"
            )
    else:
        click.echo(f"Snippy is up-to-date! Installed version: {installed_version} 🎉")


def update_snippy():
    stop_animation = show_loading_animation(message="🕵️  Checking for updates...")
    try:
        result = subprocess.run(
            ["brew", "upgrade", "snippy"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stop_animation.set()
        if result.returncode == 0:
            click.echo(
                click.style(
                    "\nSnippy has been updated to the latest version! 🎉", fg="green"
                )
            )
        else:
            click.echo(
                click.style(f"\nFailed to update Snippy: {result.stderr}", fg="red")
            )
    except Exception as e:
        stop_animation.set()
        click.echo(click.style(f"\nAn error occurred during the update: {e}", fg="red"))


def version_check_in_background():
    def check():
        fetch_installed_version()
        fetch_latest_version()

    thread = threading.Thread(target=check, daemon=True)
    thread.start()
