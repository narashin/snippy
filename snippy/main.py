import sys

import click

from snippy.commands.commit import commit_with_warning, select_commit_type
from snippy.commands.config import configure, load_config_async, reset_config
from snippy.commands.update import (
    check_version,
    fetch_installed_version_with_animation,
    load_installed_version,
    update_snippy,
    version_check_in_background,
)
from snippy.utils.emoji_utils import emojize_if_valid
from snippy.utils.io_utils import get_input, run_async


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
    update_snippy()


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
            filtered_commit_types = commit_types
        elif include_type and not include_emoji:
            filtered_commit_types = {k: "" for k in commit_types.keys()}
        elif include_emoji and not include_type:
            filtered_commit_types = dict(commit_types.items())
        else:
            filtered_commit_types = {}

        if include_type or include_emoji:
            select_commit_type(filtered_commit_types, include_type, include_emoji)
            option = get_input("Choose an option to select a type: ")

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

        while True:
            subject = get_input("Enter commit message: ").strip()

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
                    break
                else:
                    click.echo(
                        click.style(
                            "Commit message cannot be empty. Please provide a message.",
                            fg="red",
                        )
                    )
            else:
                break

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
    version_check_in_background()
    try:
        check_version()
        cli()
    except click.Abort:
        click.echo("\nExecution aborted by user. Exiting... Bye!")
        sys.exit(1)
    except Exception as e:
        click.echo(click.style(f"An unexpected error occurred: {e}", fg="red"))
        sys.exit(1)
