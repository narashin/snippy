import sys

import emoji


def get_input(prompt):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    return sys.stdin.buffer.readline().decode("utf-8", "ignore").strip()


def emojize_if_valid(emoji_code):
    try:
        return emoji.emojize(emoji_code, language="alias")
    except KeyError:
        return emoji_code
