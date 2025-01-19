import click

from snippy.constants import SEPARATOR
from snippy.utils.emoji_utils import emojize_if_valid
from snippy.utils.git_utils import get_subprocess_module, warn_if_no_staged_files


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


def commit_with_warning(commit_message):
    warn_if_no_staged_files(commit_message)

    subprocess = get_subprocess_module()

    subprocess.run(["git", "commit", "-m", commit_message])
    click.echo(click.style("Commit successful!", fg="green", bold=True))
