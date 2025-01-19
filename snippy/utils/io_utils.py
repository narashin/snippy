import asyncio

from prompt_toolkit import prompt
from prompt_toolkit.styles import Style


def run_async(func, *args, **kwargs):
    return asyncio.run(func(*args, **kwargs))

promptStyle = Style.from_dict({
    'prompt': 'ansiblue bold',  # 프롬프트 텍스트 스타일
    'input': 'ansiwhite bold',  # 입력 텍스트 스타일
})

def get_input(prompt_message: str) -> str:
    return prompt(prompt_message, style=promptStyle).strip()
