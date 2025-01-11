import asyncio
import json
import os
import sys
import time

import click

CONFIG_PATH = os.path.expanduser("~/.snippy_config.json")


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
    return {key: emoji.emojize(value, language="alias") for key, value in commit_types.items()}

raw_commit_types = {
    "feat": ":sparkles:",
    "fix": ":bug:",
    "docs": ":memo:",
    "style": ":lipstick:",
    "refactor": ":recycle:",
    "perf": ":zap:",
    "test": ":white_check_mark:",
    "chore": ":wrench:"
}

def run_async(func, *args, **kwargs):
    return asyncio.run(func(*args, **kwargs))

def get_input(prompt: str) -> str:
    try:
        sys.stdout.write(prompt)
        sys.stdout.flush()
        return sys.stdin.buffer.readline().decode("utf-8", "ignore").strip()
    except KeyboardInterrupt:
        sys.stdout.flush()
        raise

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
    print("-" * 40)

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

    emoji_status = "\033[1;32mon\033[0m" if include_emoji else "\033[1;31moff\033[0m"
    type_status = "\033[1;32mon\033[0m" if include_type else "\033[1;31moff\033[0m"

    print("Template: ")
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

    print("-" * 40)


def select_commit_type(
    commit_types,
    include_type=True,
    include_emoji=True,
    show_add_new=False,
    show_delete=False,
):
    print("Select commit type:")
    print("-" * 40)
    for idx, (commit_type, emoji_code) in enumerate(commit_types.items()):
        base_type = commit_type.split("_")[0]
        if include_type and include_emoji:
            print(f"{idx + 1}. {base_type} ({emojize_if_valid(emoji_code)})")
        elif include_type:
            print(f"{idx + 1}. {base_type}")
        elif include_emoji:
            print(f"{idx + 1}. {emojize_if_valid(emoji_code)}")
    if show_add_new:
        print("a. + Add a new type")
    if show_delete:
        print("d. - Delete a type")


def configure_template(config):
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
    if config.get("include_emoji", True):
        example_commit = example_commit.replace("<emoji>", emojize_if_valid(first_commit_type[1]))
    else:
        example_commit = example_commit.replace("<emoji>", "")
    example_commit = example_commit.replace("<subject>", "This is example comment.")
    while True:
        show_current_template(config)
        choice = get_input(
            "\033[1;34mDo you want to configure (o)ptions or comment (t)emplate, or 'b' to go back:\033[0m "
        ).lower()
        if choice == "b":
            return
        elif choice == "o":
            option = get_input(
                "\033[1;34mChoose an option to toggle (1-2) or 'b' to go back:\033[0m "
            ).lower()
            if option == "b":
                continue
            elif option == "1":
                include_emoji = not config.get("include_emoji", True)
                config["include_emoji"] = include_emoji
                print(f"<emoji> set to {'on' if include_emoji else 'off'}")
            elif option == "2":
                include_type = not config.get("include_type", True)
                config["include_type"] = include_type
                print(f"<type> set to {'on' if include_type else 'off'}")
            else:
                print("Invalid option. Please choose '1', '2', or 'b'.")

            commit_template = "<type>: <emoji> <subject>"
            if not config.get("include_type", True):
                commit_template = commit_template.replace("<type>: ", "")
            if not config.get("include_emoji", True):
                commit_template = commit_template.replace("<emoji> ", "")
            config["commit_template"] = commit_template
            save_config(config)
        elif choice == "t":
            print("Template: ")
            print(f"  {config['commit_template']} (e.g: {example_commit})")
            new_template = get_input(
                f"\033[1;34mEnter new commit template (use {'<type>,' if config.get('include_type', True) else ''} {'<emoji>,' if config.get('include_emoji', True) else ''} and <subject>, or 'b' to go back):\033[0m "
            )
            if new_template == "b":
                continue
            if "<subject>" not in new_template:
                print("Template must include <subject>")
            else:
                config["commit_template"] = new_template
                save_config(config)
                print(f"Template updated to: {new_template}")
                break
        else:
            print("Invalid choice. Please choose 'o', 't', or 'b'.")


def configure_commit_types(config):
    if "commit_types" not in config:
        config["commit_types"] = emojize_commit_types(raw_commit_types)
    include_emoji = config.get("include_emoji", True)
    include_type = config.get("include_type", True)
    while True:
        if not include_type and not include_emoji:
            for idx, (commit_type, emoji_code) in enumerate(config["commit_types"].items()):
                print(f"{idx + 1}. {commit_type.split('_')[0]} ({emojize_if_valid(emoji_code)})")
            print("a. + Add a new type")
            print("d. - Delete a type")
            print(
                "\033[1;33mNote: You can still modify existing commit types, but they won't be used in the template.\033[0m"
            )
        elif include_type and not include_emoji:
            print("Options: <type> is \033[1;32mon\033[0m. <emoji> is \033[1;31moff\033[0m.")
            for idx, (commit_type, emoji_code) in enumerate(config["commit_types"].items()):
                print(f"{idx + 1}. {commit_type.split('_')[0]} ({emojize_if_valid(emoji_code)})")
            print("a. + Add a new type")
            print("d. - Delete a type")
            print(
                "\033[1;33mNote: You can still modify existing commit types, but emojis won't be used in the template.\033[0m"
            )
        elif not include_type and include_emoji:
            print("Options: <type> is \033[1;31moff\033[0m. <emoji> is \033[1;32mon\033[0m.")
            for idx, (commit_type, emoji_code) in enumerate(config["commit_types"].items()):
                print(f"{idx + 1}. {commit_type.split('_')[0]} ({emojize_if_valid(emoji_code)})")
            print("a. + Add a new type")
            print("d. - Delete a type")
            print(
                "\033[1;33mNote: You can still modify existing commit types, but they won't be used in the template.\033[0m"
            )
        else:
            print("Options: <type> is \033[1;32mon\033[0m. <emoji> is \033[1;32mon\033[0m.")
            select_commit_type(config["commit_types"], show_add_new=True, show_delete=True)

        option = get_input(
            "\033[1;34mChoose an option or enter number to select a type (or 'b' to go back):\033[0m "
        ).lower()
        if option == "q" or option == "b":
            break
        elif option == "a":
            type_key = get_input("\033[1;34mEnter commit type key (e.g., feat, fix, ...):\033[0m ")
            while True:
                new_emoji = get_input(
                    "\033[1;34mEnter emoji for new type (use :emoji: format, leave empty to skip):\033[0m "
                )
                if not new_emoji or (new_emoji.startswith(":") and new_emoji.endswith(":")):
                    break
                else:
                    print("Emoji must be in :emoji: format.")
            if type_key in config["commit_types"]:

                suffix = 1
                new_type_key = f"{type_key}_{suffix}"
                while new_type_key in config["commit_types"]:
                    suffix += 1
                    new_type_key = f"{type_key}_{suffix}"
                type_key = new_type_key
            config["commit_types"][type_key] = new_emoji
            print(
                f"Added new type: {type_key.split('_')[0]} with emoji: {emojize_if_valid(new_emoji)}"
            )
            print()
        elif option == "d":
            while True:
                delete_option = get_input(
                    "\033[1;34mEnter the number of the commit type to delete (or 'b' to go back):\033[0m "
                )
                if delete_option == "b":
                    break
                try:
                    delete_option = int(delete_option)
                    if 1 <= delete_option <= len(config["commit_types"]):
                        type_key = list(config["commit_types"].keys())[delete_option - 1]
                        confirm = get_input(
                            f"\033[1;34mAre you sure you want to delete '{type_key.split('_')[0]}'? (Y/n):\033[0m "
                        ).lower()
                        if confirm in ["", "y", "yes"]:
                            del config["commit_types"][type_key]
                            print(f"Deleted commit type '{type_key.split('_')[0]}'.")
                        else:
                            print("Deletion cancelled.")
                        break
                    else:
                        print("Invalid option. Please choose a valid number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        else:
            try:
                option = int(option)
                if 1 <= option <= len(config["commit_types"]):
                    type_key = list(config["commit_types"].keys())[option - 1]
                    print(
                        f"Editing commit type: \033[1;34m{type_key.split('_')[0]}\033[0m ({emojize_if_valid(config['commit_types'][type_key])})"
                    )
                    new_type = get_input(
                        f"\033[1;34mEnter new name for \033[1;32m{type_key.split('_')[0]}\033[1;34m (leave empty to keep the current name):\033[0m "
                    )
                    if new_type:
                        config["commit_types"][new_type] = config["commit_types"].pop(type_key)
                        type_key = new_type
                        print(f"Updated commit type name to: {type_key.split('_')[0]}")
                    else:
                        print("Commit type name unchanged.")
                    while True:
                        new_emoji = get_input(
                            f"\033[1;34mEnter new emoji for \033[1;32m{type_key.split('_')[0]}\033[1;34m (current: {emojize_if_valid(config['commit_types'][type_key])}) (use :emoji: format, leave empty to keep current, type 'remove' to delete):\033[0m "
                        )
                        if new_emoji.lower() == "remove":
                            config["commit_types"][type_key] = ""
                            print("Commit Type Emoji removed.")
                            break
                        elif not new_emoji:
                            print("Commit Type Emoji unchanged.")
                            break
                        elif new_emoji.startswith(":") and new_emoji.endswith(":"):
                            config["commit_types"][type_key] = new_emoji
                            print(
                                f"Updated {type_key.split('_')[0]} to {emojize_if_valid(new_emoji)}"
                            )
                            break
                        else:
                            print("Invalid emoji format. Must be in :emoji: format.")
                else:
                    print("Invalid option. Please choose a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        save_config(config)
        config = run_async(load_config_async)


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
        print("-" * 40)
        print("Template:")
        print(f"  {current_template} (e.g: {example_commit})")
        print(" ")
        print("Options:")
        print(
            f"1. <emoji> (optional): {'\033[1;32mon\033[0m' if include_emoji else '\033[1;31moff\033[0m'}"
        )
        print(
            f"2. <type> (optional): {'\033[1;32mon\033[0m' if include_type else '\033[1;31moff\033[0m'}"
        )
        print("   <subject> (*required): on")
        print("-" * 40)


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
        start_time = time.time()

        # 설정 로드
        config_start = time.time()
        config = run_async(load_config_async)
        config_end = time.time()
        click.echo(f"Config load time: {config_end - config_start:.2f} seconds")

        # 커밋 템플릿 생성
        template_start = time.time()
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
        template_end = time.time()
        click.echo(f"Template render time: {template_end - template_start:.2f} seconds")

        # 커밋 타입 선택
        select_start = time.time()
        include_type = config.get("include_type", True)
        include_emoji = config.get("include_emoji", True)

        commit_type = ""
        emoji_code = ""

        if include_type and include_emoji:
            select_commit_type(commit_types, include_type, include_emoji)
        elif include_type:
            select_commit_type({k: "" for k in commit_types.keys()}, include_type, False)
        elif include_emoji:
            select_commit_type(dict(commit_types.items()), False, include_emoji)
        select_end = time.time()
        click.echo(f"Select commit type time: {select_end - select_start:.2f} seconds")

        # 사용자 입력 처리
        input_start = time.time()
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
        input_end = time.time()
        click.echo(f"User input time: {input_end - input_start:.2f} seconds")

        # 커밋 메시지 입력
        subject_start = time.time()
        subject = get_input("\033[1;32mEnter commit message:\033[0m ")

        commit_message = commit_template.replace("<type>", commit_type).replace(
            "<subject>", subject
        )
        if "<emoji>" in commit_template:
            commit_message = commit_message.replace("<emoji>", emojize_if_valid(emoji_code))
        else:
            commit_message = commit_message.replace("<emoji>", "")
        subject_end = time.time()
        click.echo(f"Commit message creation time: {subject_end - subject_start:.2f} seconds")

        # Git 커밋 실행
        git_start = time.time()
        get_subprocess_module().run(["git", "commit", "-m", commit_message])
        git_end = time.time()
        click.echo(f"Git commit execution time: {git_end - git_start:.2f} seconds")

        end_time = time.time()
        click.echo(f"Total execution time: {end_time - start_time:.2f} seconds")

    except KeyboardInterrupt:
        click.echo("\nSay Good bye to Snippy. Bye Bye!", err=True)
        raise click.Abort()

if __name__ == "__main__":
    try:
        cli()
    except click.Abort:
        click.echo("\nExecution aborted by user. Exiting... Bye!")
        sys.exit(1)
