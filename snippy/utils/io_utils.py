import asyncio
import readline


def run_async(func, *args, **kwargs):
    return asyncio.run(func(*args, **kwargs))


def get_input(prompt: str) -> str:
    readline.set_startup_hook(lambda: readline.insert_text(""))
    try:
        return input(prompt).strip()
    finally:
        readline.set_startup_hook(None)
