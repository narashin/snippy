import asyncio
import json
import os
import readline
import sys

import click

CONFIG_PATH = os.path.expanduser("~/.snippy_config.json")

ANSI_GREEN_BOLD = "\033[1;32m"
ANSI_RED_BOLD = "\033[1;31m"
ANSI_RESET = "\033[0m"
SEPARATOR = "-" * 40
NOTE_YELLOW = click.style("Note:", fg="yellow")
ON_GREEN = click.style("on", fg="green")
OFF_RED = click.style("off", fg="red")
SEPARATOR = "-" * 40


def get_subprocess_module():
    import subprocess

    return subprocess


_emoji = None


def get_emoji_module():
    global _emoji
    if _emoji is None:
        import emoji

        _emoji = emoji
    return _emoji


def emojize_if_valid(emoji_code):
    try:
        return get_emoji_module().emojize(emoji_code, language="alias")
    except KeyError:
        return emoji_code


def emojize_commit_types(commit_types):
    emoji = get_emoji_module()
    return {
        key: emoji.emojize(value, language="alias")
        for key, value in commit_types.items()
    }


raw_commit_types = {
    "feat": ":sparkles:",
    "fix": ":bug:",
    "docs": ":memo:",
    "style": ":lipstick:",
    "refactor": ":recycle:",
    "perf": ":zap:",
    "test": ":white_check_mark:",
    "chore": ":wrench:",
}


def run_async(func, *args, **kwargs):
    return asyncio.run(func(*args, **kwargs))


def get_input(prompt: str) -> str:
    # 기존 readline의 hook을 비활성화
    readline.set_startup_hook(lambda: readline.insert_text(""))
    try:
        user_input = input(prompt)
        return user_input.strip()
    finally:
        # readline hook을 복구
        readline.set_startup_hook(None)


def get_default_config():
    return {
        "commit_template": "<type>: <emoji> <subject>",
        "commit_types": emojize_commit_types(raw_commit_types),
    }


async def load_config_async():
    try:
        with open(CONFIG_PATH, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return get_default_config()


def save_config(config):
    with open(CONFIG_PATH, "w") as file:
        json.dump(config, file, indent=4)


def reset_config():
    default_config = get_default_config()
    save_config(default_config)


def configure(config):
    while True:
        show_current_configuration(config)
        option = get_input(
            "\033[1;34mDo you want to configure (t)emplate, (c)ommit types, (r)eset to default, or (q)uit?\033[0m "
        ).lower()
        if option == "q":
            break
        elif option == "t":
            configure_template(config)
        elif option == "c":
            configure_commit_types(config)
        elif option == "r":
            reset_config()
            config = run_async(load_config_async)
        else:
            print("Invalid option. Please choose 't', 'c', 'r', or 'q'.")
    save_config(config)


def show_current_configuration(config):
    print("Current Configuration:")
    print(SEPARATOR)

    if config["commit_types"]:
        first_commit_type = next(iter(config["commit_types"].items()))
        example_commit = config["commit_template"]
        include_type = config.get("include_type", True)
        include_emoji = config.get("include_emoji", True)

        if include_type:
            example_commit = example_commit.replace("<type>", first_commit_type[0])
        else:
            example_commit = example_commit.replace("<type>", "")

        if include_emoji:
            example_commit = example_commit.replace(
                "<emoji>", emojize_if_valid(first_commit_type[1])
            )
        else:
            example_commit = example_commit.replace("<emoji>", "")

        example_commit = example_commit.replace("<subject>", "This is example comment.")

    emoji_status = (
        f"{ANSI_GREEN_BOLD}on{ANSI_RESET}"
        if include_emoji
        else f"{ANSI_RED_BOLD}off{ANSI_RESET}"
    )
    type_status = (
        f"{ANSI_GREEN_BOLD}on{ANSI_RESET}"
        if include_type
        else f"{ANSI_RED_BOLD}off{ANSI_RESET}"
    )

    print("Template:")
    print(f"  {config['commit_template']} (e.g: {example_commit})")
    print()
    print("Commit types:")
    print(f"  <emoji> option is {emoji_status}")
    print(f"  <type> option is {type_status}")
    print()

    if include_type and include_emoji:
        for commit_type, emoji_code in config["commit_types"].items():
            print(f"  {commit_type.split('_')[0]}: {emojize_if_valid(emoji_code)}")
    elif include_type:
        for commit_type in config["commit_types"].keys():
            print(f"  {commit_type.split('_')[0]}")
    elif include_emoji:
        for emoji_code in config["commit_types"].values():
            print(f"  {emojize_if_valid(emoji_code)}")

    print(SEPARATOR)


def format_commit_type(idx, base_type, emoji_code, include_type, include_emoji):
    if include_type and include_emoji:
        return f"{idx + 1}. {base_type} ({emojize_if_valid(emoji_code)})"
    elif include_type:
        return f"{idx + 1}. {base_type}"
    elif include_emoji:
        return f"{idx + 1}. {emojize_if_valid(emoji_code)}"
    return f"{idx + 1}. {base_type}"


def select_commit_type(
    commit_types,
    include_type=True,
    include_emoji=True,
    show_add_new=False,
    show_delete=False,
):
    print("Select commit type:")
    print(SEPARATOR)

    for idx, (commit_type, emoji_code) in enumerate(commit_types.items()):
        base_type = commit_type.split("_")[0]
        print(
            format_commit_type(idx, base_type, emoji_code, include_type, include_emoji)
        )

    if show_add_new:
        print("a. + Add a new type")
    if show_delete:
        print("d. - Delete a type")


def configure_template(config):
    def update_example_commit():
        if config["commit_types"]:
            first_commit_type = next(iter(config["commit_types"].items()))
            example = config["commit_template"]
            if config.get("include_type", True):
                example = example.replace("<type>", first_commit_type[0])
            else:
                example = example.replace("<type>", "")
            if config.get("include_emoji", True):
                example = example.replace(
                    "<emoji>", emojize_if_valid(first_commit_type[1])
                )
            else:
                example = example.replace("<emoji>", "")
            example = example.replace("<subject>", "This is example comment.")
            return example
        return ""

    while True:
        click.echo(click.style("Current Template Configuration:", bold=True))
        click.echo(
            f"Template: {config['commit_template']} (e.g: {update_example_commit()})"
        )
        click.echo("Options:")
        click.echo(
            f"  1. <emoji> {'on' if config.get('include_emoji', True) else 'off'}"
        )
        click.echo(f"  2. <type> {'on' if config.get('include_type', True) else 'off'}")
        click.echo("")

        choice = click.prompt(
            click.style(
                "Do you want to configure (o)ptions or comment (t)emplate, or 'b' to go back",
                fg="blue",
            ),
            type=str,
            default="b",
        ).lower()

        if choice == "b":
            return
        elif choice == "o":
            option = click.prompt(
                click.style(
                    "Choose an option to toggle (1-2) or 'b' to go back", fg="blue"
                ),
                type=str,
                default="b",
            ).lower()
            if option == "b":
                continue
            elif option == "1":
                include_emoji = not config.get("include_emoji", True)
                config["include_emoji"] = include_emoji
                click.echo(f"<emoji> set to {'on' if include_emoji else 'off'}")
            elif option == "2":
                include_type = not config.get("include_type", True)
                config["include_type"] = include_type
                click.echo(f"<type> set to {'on' if include_type else 'off'}")
            else:
                click.echo(
                    click.style(
                        "Invalid option. Please choose '1', '2', or 'b'.", fg="red"
                    )
                )

            commit_template = "<type>: <emoji> <subject>"
            if not config.get("include_type", True):
                commit_template = commit_template.replace("<type>: ", "")
            if not config.get("include_emoji", True):
                commit_template = commit_template.replace("<emoji> ", "")
            config["commit_template"] = commit_template
            save_config(config)
        elif choice == "t":
            click.echo(
                click.style(
                    f"Current Template: {config['commit_template']} (e.g: {update_example_commit()})",
                    fg="yellow",
                )
            )
            new_template = click.prompt(
                click.style(
                    "Enter new commit template (use "
                    f"{'<type>, ' if config.get('include_type', True) else ''}"
                    f"{'<emoji>, ' if config.get('include_emoji', True) else ''}"
                    "<subject>, or 'b' to go back",
                    fg="blue",
                ),
                type=str,
                default="b",
            )
            if new_template == "b":
                continue
            if "<subject>" not in new_template:
                click.echo(click.style("Template must include <subject>", fg="red"))
            else:
                config["commit_template"] = new_template
                save_config(config)
                click.echo(
                    click.style(f"Template updated to: {new_template}", fg="green")
                )
                break
        else:
            click.echo(
                click.style("Invalid choice. Please choose 'o', 't', or 'b'.", fg="red")
            )


def configure_commit_types(config):
    if "commit_types" not in config:
        config["commit_types"] = emojize_commit_types(raw_commit_types)

    while True:
        include_emoji = config.get("include_emoji", True)
        include_type = config.get("include_type", True)

        click.echo(click.style("Commit Types Configuration:", bold=True))
        click.echo(SEPARATOR)

        if include_type and include_emoji:
            click.echo(f"Options: <type> is {ON_GREEN}. <emoji> is {ON_GREEN}.")
        elif include_type:
            click.echo(f"Options: <type> is {ON_GREEN}. <emoji> is {OFF_RED}.")
        elif include_emoji:
            click.echo(f"Options: <type> is {OFF_RED}. <emoji> is {ON_GREEN}.")
        else:
            click.echo(f"Options: <type> is {OFF_RED}. <emoji> is {OFF_RED}.")

        for idx, (commit_type, emoji_code) in enumerate(config["commit_types"].items()):
            base_type = commit_type.split("_")[0]
            emoji_display = emojize_if_valid(emoji_code) if include_emoji else ""
            click.echo(f"{idx + 1}. {base_type} {emoji_display}")

        click.echo("a. + Add a new type")
        click.echo("d. - Delete a type")
        click.echo(SEPARATOR)

        option = click.prompt(
            click.style(
                "Choose an option or enter number to select a type (or 'b' to go back):",
                fg="blue",
            ),
            type=str,
        ).lower()

        if option in ["b", "q"]:
            break

        elif option == "a":
            type_key = click.prompt(
                click.style("Enter commit type key (e.g., feat, fix, ...):", fg="blue")
            )
            new_emoji = click.prompt(
                click.style(
                    "Enter emoji for new type (use :emoji: format, leave empty to skip):",
                    fg="blue",
                ),
                default="",
            )
            if type_key in config["commit_types"]:
                suffix = 1
                new_type_key = f"{type_key}_{suffix}"
                while new_type_key in config["commit_types"]:
                    suffix += 1
                    new_type_key = f"{type_key}_{suffix}"
                type_key = new_type_key

            config["commit_types"][type_key] = new_emoji
            click.echo(
                f"Added new type: {click.style(type_key.split('_')[0], fg='green')} with emoji: {emojize_if_valid(new_emoji)}"
            )

        elif option == "d":
            delete_option = click.prompt(
                click.style(
                    "Enter the number of the commit type to delete (or 'b' to go back):",
                    fg="blue",
                ),
                default="b",
            )
            if delete_option.lower() == "b":
                continue
            try:
                delete_option = int(delete_option)
                if 1 <= delete_option <= len(config["commit_types"]):
                    type_key = list(config["commit_types"].keys())[delete_option - 1]
                    confirm = click.confirm(
                        f"Are you sure you want to delete '{type_key.split('_')[0]}'?",
                        default=False,
                    )
                    if confirm:
                        del config["commit_types"][type_key]
                        click.echo(f"Deleted commit type '{type_key.split('_')[0]}'.")
                else:
                    click.echo(
                        click.style(
                            "Invalid option. Please choose a valid number.", fg="red"
                        )
                    )
            except ValueError:
                click.echo(
                    click.style("Invalid input. Please enter a number.", fg="red")
                )

        else:
            try:
                option = int(option)
                if 1 <= option <= len(config["commit_types"]):
                    type_key = list(config["commit_types"].keys())[option - 1]
                    click.echo(
                        f"Editing commit type: {click.style(type_key.split('_')[0], fg='blue')} ({emojize_if_valid(config['commit_types'][type_key])})"
                    )
                    new_type = click.prompt(
                        click.style(
                            f"Enter new name for {type_key.split('_')[0]} (leave empty to keep current):",
                            fg="blue",
                        ),
                        default="",
                    )
                    if new_type:
                        config["commit_types"][new_type] = config["commit_types"].pop(
                            type_key
                        )
                        type_key = new_type
                        click.echo(
                            f"Updated commit type name to: {type_key.split('_')[0]}"
                        )
                    else:
                        click.echo("Commit type name unchanged.")

                    new_emoji = click.prompt(
                        click.style(
                            f"Enter new emoji for {type_key.split('_')[0]} (leave empty to keep current):",
                            fg="blue",
                        ),
                        default="",
                    )
                    if new_emoji:
                        config["commit_types"][type_key] = new_emoji
                        click.echo(
                            f"Updated {type_key.split('_')[0]} to {emojize_if_valid(new_emoji)}"
                        )
                    else:
                        click.echo("Commit Type Emoji unchanged.")
                else:
                    click.echo(
                        click.style(
                            "Invalid option. Please choose a valid number.", fg="red"
                        )
                    )
            except ValueError:
                click.echo(
                    click.style("Invalid input. Please enter a number.", fg="red")
                )

        save_config(config)


def check_staged_files():
    subprocess = get_subprocess_module()
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"], stdout=subprocess.PIPE, text=True
    )
    if not result.stdout.strip():
        return False
    return True


def warn_if_no_staged_files(commit_message):
    if not check_staged_files():
        click.echo(
            click.style("Warning: No staged files detected!", fg="yellow", bold=True)
        )
        click.echo(
            click.style("You can still commit manually using:", fg="yellow")
            + f' git commit -m "{commit_message}"'
        )
        raise click.Abort()


def commit_with_warning(commit_message):
    warn_if_no_staged_files(commit_message)
    subprocess = get_subprocess_module()
    subprocess.run(["git", "commit", "-m", commit_message])
    click.echo(click.style("Commit successful!", fg="green", bold=True))


def show_current_template(config):
    current_template = config.get("commit_template")
    include_type = config.get("include_type", True)
    include_emoji = config.get("include_emoji", True)

    if config["commit_types"]:
        first_commit_type = next(iter(config["commit_types"].items()))
        example_commit = current_template.replace("<type>", first_commit_type[0])
        if include_type:
            example_commit = example_commit.replace("<type>", first_commit_type[0])
        else:
            example_commit = example_commit.replace("<type>", "")
        if include_emoji:
            example_commit = example_commit.replace(
                "<emoji>", emojize_if_valid(first_commit_type[1])
            )
        else:
            example_commit = example_commit.replace("<emoji>", "")
        example_commit = example_commit.replace("<subject>", "This is example comment.")

        click.echo(click.style("-" * 40, dim=True))
        click.echo(click.style("Template:", bold=True))
        click.echo(f"  {current_template} (e.g: {example_commit})")
        click.echo(" ")
        click.echo(click.style("Options:", bold=True))
        click.echo(
            f"1. <emoji> (optional): {click.style('on', fg='green', bold=True) if include_emoji else click.style('off', fg='red', bold=True)}"
        )
        click.echo(
            f"2. <type> (optional): {click.style('on', fg='green', bold=True) if include_type else click.style('off', fg='red', bold=True)}"
        )
        click.echo(
            "   <subject> (*required): " + click.style("on", fg="green", bold=True)
        )
        click.echo(click.style("-" * 40, dim=True))


@click.group(invoke_without_command=True)
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


if __name__ == "__main__":
    try:
        cli()
    except click.Abort:
        click.echo("\nExecution aborted by user. Exiting... Bye!")
        sys.exit(1)
    except Exception as e:
        click.echo(click.style(f"An unexpected error occurred: {e}", fg="red"))
        sys.exit(1)
