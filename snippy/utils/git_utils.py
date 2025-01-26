import click


def get_subprocess_module():
    import subprocess

    return subprocess


def check_staged_files():
    subprocess = get_subprocess_module()
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return bool(result.stdout.strip())


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
