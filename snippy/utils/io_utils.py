import asyncio

import click


def run_async(func, *args, **kwargs):
    return asyncio.run(func(*args, **kwargs))


# def get_input(prompt: str) -> str:
#     return click.prompt(prompt, type=str, show_default=False).strip()


def filter_ansi_sequences(text: str) -> str:
    import re

    ansi_escape = re.compile(r"\x1b\[.*?[@-~]")
    return ansi_escape.sub("", text)


def get_input(prompt: str) -> str:
    user_input = click.prompt(prompt, type=str).strip()
    clean_input = filter_ansi_sequences(user_input)
    print(f"\r{prompt}{clean_input}", flush=True)
    return clean_input
