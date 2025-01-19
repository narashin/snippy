import os
import sys

import click

from snippy.commands.commit import commit_with_warning, select_commit_type
from snippy.commands.config import configure, load_config_async, reset_config
from snippy.utils.emoji_utils import emojize_if_valid
from snippy.utils.git_utils import get_git_version
from snippy.utils.io_utils import get_input, run_async


def capture_input():
    while True:
        char = sys.stdin.read(1)
        print(f"Key pressed: {repr(char)}")


@click.group(invoke_without_command=True)
@click.version_option(version=get_git_version(), prog_name="Snippy")
@click.version_option(version="2.1.1", prog_name="Snippy")
@click.option("--config", is_flag=True, help="Configure commit template and types.")
@click.option("--reset", is_flag=True, help="Reset configuration to default values.")
@click.pass_context
def cli(ctx, config, reset):
    """Snippy! Templatize your git commit comments. <3"""
    if config:
        ctx.invoke(config_command)
        ctx.exit()

    if reset:
        ctx.invoke(reset_command)
        ctx.exit()

    if ctx.invoked_subcommand is None:
        run()


@cli.command(name="config")
def config_command():
    """Configure commit template and types."""
    config = run_async(load_config_async)
    configure(config)


@cli.command(name="reset")
def reset_command():
    """Reset configuration to default values."""
    reset_config()
    click.echo("Configuration reset to default values.")


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
                "<emoji>", emojize_if_valid(first_commit_type[1])
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
            select_commit_type(commit_types, include_type, include_emoji)
        elif include_type:
            select_commit_type(
                {k: "" for k in commit_types.keys()}, include_type, False
            )
        elif include_emoji:
            select_commit_type(dict(commit_types.items()), False, include_emoji)

        if include_type or include_emoji:
            option = get_input(
                "\033[1;34mChoose an option or enter number to select a type:\033[0m "
            ).lower()
            if option.isdigit():
                option = int(option)
                if 1 <= option <= len(commit_types):
                    commit_type = list(commit_types.keys())[option - 1]
                    emoji_code = commit_types[commit_type]
                else:
                    click.echo("Invalid option. Exiting.")
                    sys.exit(1)
            else:
                click.echo("Invalid option. Exiting.")
                sys.exit(1)

        subject = get_input("\033[1;32mEnter commit message:\033[0m ")

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


def debug_environment():
    print("stdin isatty:", sys.stdin.isatty())
    print("stdout isatty:", sys.stdout.isatty())
    print("TERM:", os.environ.get("TERM", "Not Set"))


if __name__ == "__main__":
    try:
        print("Welcome to Snippy!")
        click.echo("끄아아아아아아아악!!!")
        debug_environment()
        cli()
    except click.Abort:
        click.echo("\nExecution aborted by user. Exiting... Bye!")
        sys.exit(1)
    except Exception as e:
        click.echo(click.style(f"An unexpected error occurred: {e}", fg="red"))
        sys.exit(1)
