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
    return {
        key: {
            "emoji": emoji.emojize(value["emoji"], language="alias"),
            "description": value["description"],
        }
        for key, value in commit_types.items()
    }
