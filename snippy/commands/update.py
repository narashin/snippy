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


def update_brew():
    try:
        result = subprocess.run(
            ["brew", "update"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            click.echo("Homebrew updated successfully!")
        else:
            click.echo(f"Error updating Homebrew: {result.stderr}")
    except Exception as e:
        click.echo(f"Failed to update Homebrew: {e}")


def update_snippy():
    stop_animation = show_loading_animation(message="🕵️  Checking for updates...")
    try:
        update_brew()

        installed_version = fetch_installed_version()
        latest_version = fetch_latest_version()

        if installed_version is None or latest_version is None:
            stop_animation.set()
            click.echo("\nUnable to check versions. Please try again later. 😢")
            return

        if installed_version == latest_version:
            stop_animation.set()
            click.echo(
                f"\nSnippy is already up-to-date! Version: {installed_version} 🎉"
            )
            return

        stop_animation.set()
        click.echo(
            f"\n🆕✨ Current version: {installed_version}, Latest version: {latest_version}"
        )
        update = click.prompt("Would you like to update? (y/N)", type=str, default="n")

        if update.lower() != "y":
            click.echo(
                f"Update cancelled. Run {click.style('`snippy update`', fg='bright_yellow', bold=True)} to update later. 👋"
            )
            return

        result = subprocess.run(
            ["brew", "upgrade", "snippy"],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            click.echo(
                click.style(
                    f"\nSnippy has been updated from {installed_version} to {latest_version}! 🎉",
                    fg="green",
                )
            )
        else:
            click.echo(
                click.style(f"\nFailed to update Snippy: {result.stderr}", fg="red")
            )
    except Exception as e:
        stop_animation.set()
        click.echo(click.style(f"\nAn error occurred during the update: {e}", fg="red"))
    finally:
        if not stop_animation.is_set():
            stop_animation.set()


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
            capture_output=True,
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
    thread.join()


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
            capture_output=True,
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


def version_check_in_background():
    def check():
        try:
            installed_version = fetch_installed_version()
            latest_version = fetch_latest_version()

            if (
                installed_version
                and latest_version
                and installed_version != latest_version
            ):
                click.echo(
                    f"\n🆕✨ New version available! Current: {installed_version}, Latest: {latest_version}"
                )
                click.echo(
                    f"Run {click.style('`snippy update`', fg='bright_yellow', bold=True)} to update. 👋"
                )
        except Exception:
            pass

    thread = threading.Thread(target=check, daemon=True)
    thread.start()
