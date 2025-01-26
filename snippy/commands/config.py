import json

import click

from snippy.constants import CONFIG_PATH, OFF_RED, ON_GREEN, RAW_COMMIT_TYPES, SEPARATOR
from snippy.utils.emoji_utils import emojize_commit_types, emojize_if_valid
from snippy.utils.io_utils import get_input, run_async


def get_default_config():
    return {
        "commit_template": "<type>: <emoji> <subject>",
        "commit_types": emojize_commit_types(RAW_COMMIT_TYPES),
    }


async def load_config_async():
    try:
        with open(CONFIG_PATH, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        default_config = get_default_config()
        save_config(default_config)
        return default_config


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
            "Do you want to configure (t)emplate, (c)ommit types, (r)eset to default, or (q)uit? "
        ).lower()
        if option == "q":
            break
        elif option == "t":
            show_current_template(config)
            configure_template(config)
        elif option == "c":
            configure_commit_types(config)
        elif option == "r":
            reset_config()
            config = run_async(load_config_async)
            click.echo("🔄 Configuration reset to default values. ")
        else:
            click.echo(
                click.style(
                    "Invalid option. Please choose 't', 'c', 'r', or 'q'.", fg="red"
                )
            )
    save_config(config)


def show_current_configuration(config):
    click.echo(click.style("Current Configuration:", bold=True))
    click.echo(click.style(SEPARATOR, dim=True))
    click.echo()

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
        click.style("on", fg="green", bold=True)
        if include_emoji
        else click.style("off", fg="red", bold=True)
    )
    type_status = (
        click.style("on", fg="green", bold=True)
        if include_type
        else click.style("off", fg="red", bold=True)
    )

    click.echo("Template:")
    click.echo(f"  {config['commit_template']} (e.g: {example_commit})")
    click.echo()
    click.echo("Commit types:")
    click.echo(f"  <emoji> option is {emoji_status}")
    click.echo(f"  <type> option is {type_status}")
    click.echo()

    if include_type and include_emoji:
        for commit_type, emoji_code in config["commit_types"].items():
            print(f"  {commit_type.split('_')[0]}: {emojize_if_valid(emoji_code)}")
    elif include_type:
        for commit_type in config["commit_types"].keys():
            print(f"  {commit_type.split('_')[0]}")
    elif include_emoji:
        for emoji_code in config["commit_types"].values():
            print(f"  {emojize_if_valid(emoji_code)}")

    click.echo(click.style(SEPARATOR, dim=True))


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

        click.echo(click.style(SEPARATOR, dim=True))
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
        click.echo(click.style(SEPARATOR, dim=True))


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
            f"  1. <emoji>: {click.style('on', fg='green', bold=True) if config.get('include_emoji', True) else click.style('off', fg='red', bold=True)}"
        )
        click.echo(
            f"  2. <type>: {click.style('on', fg='green', bold=True) if config.get('include_type', True) else click.style('off', fg='red', bold=True)}"
        )
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
            show_current_template(config)

            while True:
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

                if new_template.lower() == "b":
                    break

                errors = []
                if "<subject>" not in new_template:
                    errors.append("Template must include <subject>.")
                if config.get("include_emoji", True) and "<emoji>" not in new_template:
                    errors.append("<emoji> must be included when emoji is enabled.")
                if config.get("include_type", True) and "<type>" not in new_template:
                    errors.append("<type> must be included when type is enabled.")

                if errors:
                    click.echo(click.style(" ".join(errors), fg="red", bold=True))
                    continue

                # 템플릿 유효하면 저장
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
        config["commit_types"] = emojize_commit_types(RAW_COMMIT_TYPES)

    while True:
        include_emoji = config.get("include_emoji", True)
        include_type = config.get("include_type", True)

        click.echo(click.style("Commit Types Configuration:", bold=True))
        click.echo(click.style(SEPARATOR, dim=True))

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
        click.echo(click.style(SEPARATOR, dim=True))

        option = click.prompt(
            click.style(
                "Choose an option or enter number to select a type (or 'b' to go back)",
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
                    "Enter emoji for new type (use :emoji: format, leave empty to skip)",
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
                    "Enter the number of the commit type to delete (or 'b' to go back)",
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
