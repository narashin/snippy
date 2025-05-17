import sys

import click
import questionary

from snippy.commands.commit import commit_with_warning, select_commit_type
from snippy.commands.config import configure, load_config_async, reset_config
from snippy.commands.update import (
    fetch_installed_version_with_animation,
    load_installed_version,
    update_snippy,
)
from snippy.utils.emoji_utils import emojize_if_valid
from snippy.utils.io_utils import run_async


def lazy_version_fetch():
    return (
        load_installed_version()
        or fetch_installed_version_with_animation()
        or "Unknown"
    )


@click.group(invoke_without_command=True)
@click.version_option(
    version=lazy_version_fetch(),
    prog_name="Snippy",
)
@click.pass_context
def cli(ctx):
    """Snippy! Templatize your git commit comments. <3"""

    if ctx.invoked_subcommand is None:
        run()


@cli.command(name="config")
def config_command():
    config = run_async(load_config_async)
    configure(config)


@cli.command(name="reset")
def reset_command():
    reset_config()
    click.echo("Configuration reset to default values.")


@cli.command(name="update")
def update_command():
    click.echo(
        click.style(
            "Buy me a coffee! What do you think? 😝  @https://www.buymeacoffee.com/narashin",
            fg="cyan",
        )
    )

    # 버전 체크 및 공지사항
    current_version = load_installed_version()
    if current_version:
        try:
            from packaging import version

            if version.parse(current_version) <= version.parse("3.1.0"):
                click.echo(click.style("\n⚠️  Notice", fg="yellow", bold=True))
                click.echo(
                    click.style(
                        "If you're using version 3.1.0 or below, please run ",
                        fg="yellow",
                    )
                    + click.style("snippy reset", fg="yellow", bold=True)
                    + click.style(" after updating.", fg="yellow")
                )
                click.echo(
                    click.style(
                        "This is required to migrate to the new configuration format.",
                        fg="yellow",
                    )
                )
                click.echo()
        except ImportError:
            pass  # packaging 모듈이 없는 경우 무시

    update_snippy()


@cli.command(name="help")
def help_command():
    click.echo(
        click.style(
            "Buy me a coffee! What do you think? 😝  @https://www.buymeacoffee.com/narashin",
            fg="cyan",
        )
    )
    click.echo("\nSnippy! Templatize your git commit comments. <3")
    click.echo("\nAvailable commands:")
    click.echo("  run      - Start Snippy")
    click.echo("  config   - Configure Snippy")
    click.echo("  update   - Update Snippy")
    click.echo("  reset    - Reset configuration to default values")
    click.echo("  help     - Show this help message")


@cli.command()
def run():
    try:
        config = run_async(load_config_async)

        commit_template = config.get("commit_template")
        commit_types = config.get("commit_types")

        first_commit_type = next(iter(commit_types.items()))
        example_commit = commit_template.replace("<type>", first_commit_type[0])
        if config.get("include_emoji", True):
            example_commit = example_commit.replace(
                "<emoji>", emojize_if_valid(first_commit_type[1]["emoji"])
            )
        else:
            example_commit = example_commit.replace("<emoji>", "")
        example_commit = example_commit.replace("<subject>", "This is example comment.")
        click.echo("Template:")
        click.echo(f"  {commit_template} (e.g: {example_commit})")
        click.echo()

        include_type = config.get("include_type", True)
        include_emoji = config.get("include_emoji", True)

        commit_type = ""
        emoji_code = ""

        if include_type and include_emoji:
            filtered_commit_types = commit_types
        elif include_type and not include_emoji:
            filtered_commit_types = {
                k: {"emoji": "", "description": v["description"]}
                for k, v in commit_types.items()
            }
        elif include_emoji and not include_type:
            filtered_commit_types = {
                k: {"emoji": v["emoji"], "description": v["description"]}
                for k, v in commit_types.items()
            }
        else:
            filtered_commit_types = {}

        if include_type or include_emoji:
            result = select_commit_type(
                filtered_commit_types, include_type, include_emoji
            )
            if result in ["add", "delete"]:
                click.echo(
                    "Configuration options are not available in commit mode. Please use 'snippy config'."
                )
                sys.exit(1)
            elif result is None:
                click.echo("Commit cancelled.")
                sys.exit(1)
            else:
                commit_type, emoji_code = result

        subject = questionary.text("Enter commit message:").ask()
        if subject is None:
            click.echo("Commit cancelled.")
            sys.exit(1)

        if not subject:
            generated_message = commit_template
            if include_type:
                generated_message = generated_message.replace("<type>", commit_type)
            else:
                generated_message = generated_message.replace("<type>", "")

            if include_emoji:
                generated_message = generated_message.replace(
                    "<emoji>", emojize_if_valid(emoji_code)
                )
            else:
                generated_message = generated_message.replace("<emoji>", "")

            generated_message = generated_message.replace("<subject>", "").strip()

            if generated_message:
                click.echo(
                    click.style(
                        f"No commit message provided. Using default: {generated_message}",
                        fg="yellow",
                    )
                )
            else:
                click.echo(
                    click.style(
                        "Commit message cannot be empty. Please provide a message.",
                        fg="red",
                    )
                )
                sys.exit(1)

        commit_message = commit_template.replace("<type>", commit_type).replace(
            "<subject>", subject
        )
        if "<emoji>" in commit_template:
            commit_message = commit_message.replace(
                "<emoji>", emojize_if_valid(emoji_code)
            )
        else:
            commit_message = commit_message.replace("<emoji>", "")

        commit_with_warning(commit_message)

    except KeyboardInterrupt:
        click.echo("\nSay Good bye to Snippy. Bye Bye!", err=True)
        raise click.Abort()


if __name__ == "__main__":
    try:
        cli()
    except click.Abort:
        click.echo("\nExecution aborted by user. Exiting... Bye!")
        sys.exit(1)
    except Exception as e:
        click.echo(click.style(f"An unexpected error occurred: {e}", fg="red"))
        sys.exit(1)
