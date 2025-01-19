import asyncio
import readline


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
