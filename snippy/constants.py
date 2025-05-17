import os

import click

# Base Directory
BASE_DIR = os.path.expanduser("~/.snippy")

# File Paths
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
VERSION_CACHE_PATH = os.path.join(BASE_DIR, "installed_version.json")
LATEST_VERSION_PATH = os.path.join(BASE_DIR, "latest_version.json")
CACHE_EXPIRATION_TIME = 30

# ANSI Colors
ANSI_GREEN_BOLD = "\033[1;32m"
ANSI_RED_BOLD = "\033[1;31m"
ANSI_RESET = "\033[0m"

# Common Strings
SEPARATOR = "-" * 40

# Styled Texts
NOTE_YELLOW = click.style("Note:", fg="yellow")
ON_GREEN = click.style("on", fg="green")
OFF_RED = click.style("off", fg="red")
OFF_RED = click.style("off", fg="red")

# Commit Types
RAW_COMMIT_TYPES = {
    "feat": {"emoji": ":sparkles:", "description": "새로운 기능 추가 / New Feature"},
    "fix": {"emoji": ":bug:", "description": "버그 수정 / Bug Fix"},
    "docs": {"emoji": ":memo:", "description": "문서 수정 / Documentation"},
    "style": {
        "emoji": ":lipstick:",
        "description": "코드 포맷팅, 세미콜론 누락, 코드 변경이 없는 경우 / Code Style",
    },
    "refactor": {
        "emoji": ":recycle:",
        "description": "코드 리팩토링 / Code Refactoring",
    },
    "perf": {"emoji": ":zap:", "description": "성능 개선 / Performance Improvement"},
    "test": {
        "emoji": ":white_check_mark:",
        "description": "테스트 코드 추가 또는 수정 / Test Code",
    },
    "chore": {
        "emoji": ":wrench:",
        "description": "빌드 프로세스 또는 보조 도구 및 라이브러리 변경 / Build Process or Auxiliary Tools",
    },
}
