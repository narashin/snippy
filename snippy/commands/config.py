import json

import click
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

from snippy.constants import CONFIG_PATH, OFF_RED, ON_GREEN, RAW_COMMIT_TYPES, SEPARATOR
from snippy.utils.emoji_utils import emojize_commit_types, emojize_if_valid
from snippy.utils.io_utils import run_async


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
        click.echo(click.style("\nSnippy Configuration", bold=True))
        click.echo(click.style(SEPARATOR, dim=True))

        choices = [
            Choice(value="t", name="📄 Edit Template (Toggle emoji and type)"),
            Choice(value="c", name="✏️  Configure Commit Types"),
            Choice(value="r", name="🧹  Reset to default"),
            Separator(),
            Choice(value="q", name="Quit"),
        ]

        option = inquirer.select(
            message="Select an option:",
            choices=choices,
            default=None,
            border=True,
            instruction="(Use arrow keys and Enter to select)",
        ).execute()

        if option == "q":
            break
        elif option == "t":
            configure_template(config)
        elif option == "c":
            configure_commit_types(config)
        elif option == "r":
            if inquirer.confirm(
                message="Are you sure you want to reset all settings to default?",
                default=False,
            ).execute():
                reset_config()
                config = run_async(load_config_async)
                click.echo("🔄 Configuration reset to default values. ")

    save_config(config)


def show_current_configuration(config):
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

    click.echo("\nTemplate:")
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
        example_commit = current_template
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

        click.echo("\nTemplate Configuration")
        click.echo(click.style(SEPARATOR, dim=True))
        click.echo(f"Current Comment Template: {current_template}")
        click.echo(f"Example: {example_commit}")
        click.echo()
        click.echo("Options:")
        click.echo(
            f"• <emoji>: {click.style('on', fg='green', bold=True) if include_emoji else click.style('off', fg='red', bold=True)}"
        )
        click.echo(
            f"• <type>: {click.style('on', fg='green', bold=True) if include_type else click.style('off', fg='red', bold=True)}"
        )
        click.echo("• <subject>: " + click.style("required", fg="yellow", bold=True))
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
        show_current_template(config)

        choices = [
            Choice(value="o", name="↔️  Toggle Options (Emoji and Type)"),
            Choice(value="t", name="✍️  Edit Comment Template"),
            Separator(),
            Choice(value="b", name="Go back"),
        ]

        choice = inquirer.select(
            message="Select an option:",
            choices=choices,
            default=None,
            border=True,
            instruction="(Use arrow keys and Enter to select)",
        ).execute()

        if choice == "b":
            return
        elif choice == "o":
            option_choices = [
                Choice(value="1", name="Toggle <emoji>"),
                Choice(value="2", name="Toggle <type>"),
                Separator(),
                Choice(value="b", name="Go back"),
            ]

            option = inquirer.select(
                message="Choose an option to toggle:",
                choices=option_choices,
                default=None,
                border=True,
                instruction="(Use arrow keys and Enter to select)",
            ).execute()

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

            commit_template = "<type>: <emoji> <subject>"
            if not config.get("include_type", True):
                commit_template = commit_template.replace("<type>: ", "")
            if not config.get("include_emoji", True):
                commit_template = commit_template.replace("<emoji> ", "")
            config["commit_template"] = commit_template
            save_config(config)
        elif choice == "t":
            while True:
                new_template = inquirer.text(
                    message="Enter new commit template:",
                    instruction=f"Use {'<type>, ' if config.get('include_type', True) else ''}"
                    f"{'<emoji>, ' if config.get('include_emoji', True) else ''}"
                    "<subject>, or press Enter to go back",
                    default="",
                ).execute()

                if not new_template:
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

                config["commit_template"] = new_template
                save_config(config)
                click.echo(
                    click.style(f"Template updated to: {new_template}", fg="green")
                )
                break


def configure_commit_types(config):
    if "commit_types" not in config:
        config["commit_types"] = emojize_commit_types(RAW_COMMIT_TYPES)

    while True:
        include_emoji = config.get("include_emoji", True)
        include_type = config.get("include_type", True)

        click.echo("\nCommit Types Configuration")
        click.echo(click.style(SEPARATOR, dim=True))

        if include_type and include_emoji:
            click.echo(f"Options: <type> is {ON_GREEN}. <emoji> is {ON_GREEN}.")
        elif include_type:
            click.echo(f"Options: <type> is {ON_GREEN}. <emoji> is {OFF_RED}.")
        elif include_emoji:
            click.echo(f"Options: <type> is {OFF_RED}. <emoji> is {ON_GREEN}.")
        else:
            click.echo(f"Options: <type> is {OFF_RED}. <emoji> is {OFF_RED}.")
        click.echo(click.style(SEPARATOR, dim=True))

        # 커밋 타입 선택지 생성
        type_choices = []
        for idx, (commit_type, emoji_code) in enumerate(config["commit_types"].items()):
            base_type = commit_type.split("_")[0]
            emoji_display = emojize_if_valid(emoji_code) if include_emoji else ""
            display_text = f"{base_type} {emoji_display}"
            type_choices.append(Choice(value=str(idx + 1), name=display_text))

        # 액션 선택지 생성
        action_choices = [
            Choice(value="a", name="+ Add a new type"),
            Choice(value="d", name="- Delete a type"),
            Choice(value="b", name="Go back"),
        ]

        # 모든 선택지를 하나의 리스트로 합치기
        all_choices = type_choices + action_choices

        option = inquirer.fuzzy(
            message="Select a commit type to edit or choose an action:",
            choices=all_choices,
            default=None,
            border=True,
            info=False,
            instruction="(Type to search, use arrow keys and Enter to select)",
            vi_mode=False,
            match_exact=False,
            long_instruction="↑↓ to move, Enter to select",
            filter=lambda result: result if result else "",
        ).execute()

        if option == "b" or option == "q":
            break

        if not option:
            continue

        elif option == "a":
            type_key = inquirer.text(
                message="Enter commit type key:",
                instruction="e.g., feat, fix, ...",
            ).execute()

            if not type_key:
                continue

            new_emoji = inquirer.text(
                message="Enter emoji for new type:",
                instruction="Use :emoji: format, press Enter to skip",
                default="",
            ).execute()

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
            delete_choices = [
                Choice(
                    value=str(idx),
                    name=f"{commit_type.split('_')[0]} {emojize_if_valid(emoji_code) if include_emoji else ''}",
                )
                for idx, (commit_type, emoji_code) in enumerate(
                    config["commit_types"].items()
                )
            ]
            delete_choices.append(Choice(value="b", name="Go back"))

            delete_option = inquirer.fuzzy(
                message="Select a commit type to delete:",
                choices=delete_choices,
                default=None,
                border=True,
                info=False,
                instruction="(Type to search, use arrow keys and Enter to select)",
                vi_mode=False,
                match_exact=False,
                long_instruction="↑↓ to move, Enter to select",
                filter=lambda result: result if result else "",
            ).execute()

            if delete_option == "b":
                continue

            if not delete_option:
                continue

            try:
                delete_idx = int(delete_option)
                type_key = list(config["commit_types"].keys())[delete_idx]
                confirm = inquirer.confirm(
                    message=f"Are you sure you want to delete '{type_key.split('_')[0]}'?",
                    default=False,
                ).execute()

                if confirm:
                    del config["commit_types"][type_key]
                    click.echo(f"Deleted commit type '{type_key.split('_')[0]}'.")
            except (ValueError, IndexError):
                click.echo(click.style("Invalid selection.", fg="red"))

        else:
            try:
                option_idx = int(option) - 1
                if 0 <= option_idx < len(config["commit_types"]):
                    type_key = list(config["commit_types"].keys())[option_idx]
                    click.echo(
                        f"Editing commit type: {click.style(type_key.split('_')[0], fg='blue')} ({emojize_if_valid(config['commit_types'][type_key])})"
                    )

                    new_type = inquirer.text(
                        message=f"Enter new name for {type_key.split('_')[0]}:",
                        instruction="Press Enter to keep current",
                        default="",
                    ).execute()

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

                    new_emoji = inquirer.text(
                        message=f"Enter new emoji for {type_key.split('_')[0]}:",
                        instruction="Use :emoji: format, press Enter to keep current",
                        default="",
                    ).execute()

                    if new_emoji:
                        config["commit_types"][type_key] = new_emoji
                        click.echo(
                            f"Updated {type_key.split('_')[0]} to {emojize_if_valid(new_emoji)}"
                        )
                    else:
                        click.echo("Commit Type Emoji unchanged.")
            except (ValueError, IndexError):
                click.echo(click.style("Invalid selection.", fg="red"))

        save_config(config)
