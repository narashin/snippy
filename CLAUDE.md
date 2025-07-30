# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

이 파일은 이 저장소에서 작업할 때 Claude Code (claude.ai/code)에 대한 가이드를 제공합니다.

## Project Overview / 프로젝트 개요

Snippy is a Python CLI tool that helps users create Git commit messages with emojis and commit types. It's built using Poetry for dependency management and Click for the CLI interface. The tool provides an interactive experience for selecting commit types and creating formatted commit messages.

Snippy는 사용자가 이모지와 커밋 타입을 사용하여 Git 커밋 메시지를 작성할 수 있도록 도와주는 Python CLI 도구입니다. 의존성 관리를 위해 Poetry를, CLI 인터페이스를 위해 Click을 사용하여 구축되었습니다. 이 도구는 커밋 타입을 선택하고 형식화된 커밋 메시지를 작성하는 대화형 경험을 제공합니다.

## Development Commands / 개발 명령어

### Building and Packaging / 빌드 및 패키징
- **Build executable / 실행 파일 빌드**: `./build.sh` - Uses PyInstaller to create a standalone executable / PyInstaller를 사용하여 독립 실행 파일 생성
- **Install dependencies / 의존성 설치**: `poetry install` - Install Python dependencies using Poetry / Poetry를 사용하여 Python 의존성 설치
- **Run locally / 로컬 실행**: `poetry run python -m snippy.main` or `./run_snippy.sh` (after building) / `poetry run python -m snippy.main` 또는 `./run_snippy.sh` (빌드 후)

### Key Commands / 주요 명령어
- **Main entry point / 메인 진입점**: `snippy` or `poetry run snippy`
- **Configuration / 설정**: `snippy config` - Interactive configuration menu / 대화형 설정 메뉴
- **Update / 업데이트**: `snippy update` - Update via Homebrew / Homebrew를 통한 업데이트
- **Reset / 재설정**: `snippy reset` - Reset configuration to defaults / 설정을 기본값으로 재설정

## Architecture / 아키텍처

### Core Structure / 핵심 구조
- **Main entry / 메인 진입점**: `snippy/main.py` - CLI command definitions and main execution flow / CLI 명령어 정의 및 메인 실행 흐름
- **Commands / 명령어**: `snippy/commands/` - Individual command implementations / 개별 명령어 구현
  - `commit.py` - Commit type selection and Git commit execution / 커밋 타입 선택 및 Git 커밋 실행
  - `config.py` - Configuration management and interactive menus / 설정 관리 및 대화형 메뉴
  - `update.py` - Version checking and update functionality / 버전 확인 및 업데이트 기능
- **Utils / 유틸리티**: `snippy/utils/` - Utility modules / 유틸리티 모듈
  - `git_utils.py` - Git operations and staged file checking / Git 작업 및 스테이지된 파일 확인
  - `emoji_utils.py` - Emoji processing and validation / 이모지 처리 및 검증
  - `animation_utils.py` - Loading animations / 로딩 애니메이션
  - `io_utils.py` - Async utilities / 비동기 유틸리티

### Configuration System / 설정 시스템
- Configuration stored in `~/.snippy/config.json` / 설정은 `~/.snippy/config.json`에 저장
- Default commit types defined in `constants.py` as `RAW_COMMIT_TYPES` / 기본 커밋 타입은 `constants.py`의 `RAW_COMMIT_TYPES`에 정의
- Template system supports `<type>`, `<emoji>`, and `<subject>` placeholders / 템플릿 시스템은 `<type>`, `<emoji>`, `<subject>` 플레이스홀더 지원
- Configurable options: template format, commit types, emoji/type inclusion / 설정 가능한 옵션: 템플릿 형식, 커밋 타입, 이모지/타입 포함 여부

### Key Components / 주요 구성 요소
- **Interactive menus / 대화형 메뉴**: Uses InquirerPy for fuzzy search and selection / 퍼지 검색 및 선택을 위해 InquirerPy 사용
- **Commit workflow / 커밋 워크플로**: Validates staged files before committing / 커밋 전 스테이지된 파일 검증
- **Version management / 버전 관리**: Homebrew-based updates with local caching / 로컬 캐싱을 통한 Homebrew 기반 업데이트
- **Template engine / 템플릿 엔진**: Dynamic commit message generation from templates / 템플릿에서 동적 커밋 메시지 생성

### Data Flow / 데이터 흐름
1. Load configuration from JSON file or create defaults / JSON 파일에서 설정 로드 또는 기본값 생성
2. Present interactive commit type selection with fuzzy search / 퍼지 검색을 통한 대화형 커밋 타입 선택 제공
3. Collect commit message from user / 사용자로부터 커밋 메시지 수집
4. Generate final commit message using template system / 템플릿 시스템을 사용하여 최종 커밋 메시지 생성
5. Validate Git staged files and execute commit / Git 스테이지된 파일 검증 및 커밋 실행

## Important Notes / 중요 사항

- The tool requires Homebrew for installation and updates / 이 도구는 설치 및 업데이트를 위해 Homebrew가 필요합니다
- Git staged files are validated before committing / 커밋 전 Git 스테이지된 파일이 검증됩니다
- Configuration supports both emoji and text-based commit types / 설정은 이모지 및 텍스트 기반 커밋 타입을 모두 지원합니다
- Fuzzy search is available for commit type selection / 커밋 타입 선택 시 퍼지 검색이 가능합니다
- The build process creates a distributable tarball with version timestamps / 빌드 프로세스는 버전 타임스탬프가 포함된 배포 가능한 tarball을 생성합니다