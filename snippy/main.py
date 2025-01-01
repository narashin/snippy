import argparse
import json
import os
import subprocess
import sys

from snippy.utils import emojize_if_valid, get_input

CONFIG_PATH = os.path.expanduser("~/.snippy_config.json")

def get_default_config():
    return {
        "commit_template": "<type>: <emoji> <subject>",
        "commit_types": {
            "feat": ":sparkles:",
            "fix": ":bug:",
            "docs": ":memo:",
            "style": ":lipstick:",
            "refactor": ":recycle:",
            "perf": ":zap:",
            "test": ":white_check_mark:",
            "chore": ":wrench:"
        }
    }

def load_config():
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
    print("Configuration has been reset to default values.")

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
            config = load_config()
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
            # Update commit_template based on the toggled options
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
        config["commit_types"] = {
            "feat": ":sparkles:",
            "fix": ":bug:",
            "docs": ":memo:",
            "style": ":lipstick:",
            "refactor": ":recycle:",
            "perf": ":zap:",
            "test": ":white_check_mark:",
            "chore": ":wrench:",
        }
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
        config = load_config()


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


def main():
    parser = argparse.ArgumentParser(description="Snippy! Templatize your git commit comments. <3")
    parser.add_argument("--config", action="store_true", help="Configure commit template and types")
    parser.add_argument(
        "--reset", action="store_true", help="Reset configuration to default values"
    )
    args = parser.parse_args()

    if args.reset:
        reset_config()
        sys.exit(0)

    config = load_config()

    try:
        if args.config:
            configure(config)
        else:
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
            print("Template: ")
            print(f"  {commit_template} (e.g: {example_commit})")
            print()

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
                        print("Invalid option. Exiting.")
                        sys.exit(1)
                else:
                    print("Invalid option. Exiting.")
                    sys.exit(1)

            subject = get_input("\033[1;32mEnter commit message:\033[0m ")

            commit_message = commit_template.replace("<type>", commit_type).replace(
                "<subject>", subject
            )
            if "<emoji>" in commit_template:
                commit_message = commit_message.replace("<emoji>", emojize_if_valid(emoji_code))
            else:
                commit_message = commit_message.replace("<emoji>", "")

            subprocess.run(["git", "commit", "-m", commit_message])
    except KeyboardInterrupt:
        print("\nSay Good bye to snippy. Bye Bye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
