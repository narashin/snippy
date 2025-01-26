import json
import os
import subprocess
import threading

import click

from snippy.constants import BASE_DIR, LATEST_VERSION_PATH, VERSION_CACHE_PATH


def save_update_info(latest_version):
    os.makedirs(BASE_DIR, exist_ok=True)
    with open(LATEST_VERSION_PATH, "w") as f:
        json.dump({"latest_version": latest_version}, f)


def save_installed_version(installed_version):
    os.makedirs(BASE_DIR, exist_ok=True)
    with open(VERSION_CACHE_PATH, "w") as f:
        json.dump({"installed_version": installed_version}, f)


def load_latest_version():
    if os.path.exists(LATEST_VERSION_PATH):
        with open(LATEST_VERSION_PATH, "r") as f:
            return json.load(f).get("latest_version")
    return None


def load_installed_version():
    if os.path.exists(VERSION_CACHE_PATH):
        with open(VERSION_CACHE_PATH, "r") as f:
            return json.load(f).get("installed_version")
    return None


def get_latest_version():
    result = subprocess.Popen(
        ["brew", "info", "--json=v2", "snippy"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode == 0:
        brew_info = json.loads(result.stdout)
        latest_version = brew_info[0]["versions"]["stable"]
        save_update_info(latest_version)
        return latest_version
    return None


def get_installed_version():
    result = subprocess.Popen(
        ["brew", "list", "--versions", "snippy"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode == 0:
        installed_version = result.stdout.decode().strip().split()[1]
        save_installed_version(installed_version)
        return installed_version
    return None


version_check_done = threading.Event()


def check_version():
    installed_version = load_installed_version() or get_installed_version()
    latest_version = load_latest_version() or get_latest_version()

    if installed_version != latest_version:
        click.echo(
            f"Current installed version: {installed_version}, Latest version: {latest_version} 🤨"
        )
        update = click.prompt("Would you like to update? (y/n)", type=str)
        if update.lower() == "y":
            subprocess.run(["brew", "upgrade", "snippy"])
            click.echo("Update completed.")
        else:
            click.echo("Update cancelled. Run `snippy update` to update later. 👋")


def version_check_in_background():
    def check():
        try:
            get_installed_version()
            get_latest_version()
        except Exception as e:
            click.echo(f"Error occurred while checking for updates: {e}")

    thread = threading.Thread(target=check, daemon=True)
    thread.start()


def check_version_and_prompt():
    installed_version = load_installed_version()
    latest_version = load_latest_version()

    if not installed_version or not latest_version:
        return

    if installed_version != latest_version:
        click.echo(
            f"C🆕urrent installed version: {installed_version}, Latest version: {latest_version} "
        )
        update = click.prompt(
            "Would you like to update? (y/N)", type=str, default="n", show_default=True
        )
        if update.lower() == "y":
            subprocess.run(["brew", "upgrade", "snippy"])
            click.echo("Update completed. 🎉")
        else:
            click.echo("Update cancelled. Run `snippy update` to update later. 👋")
