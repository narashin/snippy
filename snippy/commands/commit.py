import click
from InquirerPy import inquirer
from InquirerPy.separator import Separator
from InquirerPy.validator import EmptyInputValidator

from snippy.utils.emoji_utils import emojize_if_valid
from snippy.utils.git_utils import get_subprocess_module, warn_if_no_staged_files


def format_commit_type(base_type, emoji_code, include_type, include_emoji):
    if include_type and include_emoji:
        return f"{base_type} ({emojize_if_valid(emoji_code)})"
    elif include_type:
        return base_type
    elif include_emoji:
        return emojize_if_valid(emoji_code)
    return base_type


def create_search_filter(search_text: str, choice: dict) -> bool:
    """커스텀 검색 필터 함수"""
    if not search_text:
        return True

    # 타입 이름에서 이모지 부분을 제외하고 검색
    name = choice["name"].split(" (")[0] if " (" in choice["name"] else choice["name"]
    search_text = search_text.lower()
    name = name.lower()

    # startswith로 검색
    return name.startswith(search_text)


def select_commit_type(
    commit_types,
    include_type=True,
    include_emoji=True,
    show_add_new=False,
    show_delete=False,
):
    choices = []
    for commit_type, emoji_code in commit_types.items():
        base_type = commit_type.split("_")[0]
        display = format_commit_type(base_type, emoji_code, include_type, include_emoji)
        choices.append({"name": display, "value": (commit_type, emoji_code)})

    if show_add_new:
        choices.append(Separator())
        choices.append({"name": "+ Add a new type", "value": "add"})
    if show_delete:
        choices.append({"name": "- Delete a type", "value": "delete"})

    result = inquirer.fuzzy(
        message="Select commit type:",
        choices=choices,
        default="",
        border=True,
        info=False,
        instruction="(Type to search)",
        vi_mode=False,
        match_exact=False,
        long_instruction="↑↓ to move, Enter to select, ESC to cancel",
        validate=EmptyInputValidator(),
        mandatory=True,
    ).execute()

    return result


def commit_with_warning(commit_message):
    warn_if_no_staged_files(commit_message)
    subprocess = get_subprocess_module()
    subprocess.run(["git", "commit", "-m", commit_message])
    click.echo(click.style("Commit successful!", fg="green", bold=True))
