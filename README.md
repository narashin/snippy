# Snippy

Snippy는 Git 커밋 메시지를 쉽게 작성할 수 있도록 도와주는 CLI 도구입니다. 이 도구는 커밋 메시지에 이모지를 추가하여 가독성을 높이고, 커밋 타입을 선택할 수 있는 기능을 제공합니다.

Snippy is a CLI tool that helps you easily write Git commit messages. This tool enhances readability by adding emojis to commit messages and allows you to select commit types.

## 특징 / Features

- 커밋 메시지에 이모지 추가 / Add emojis to commit messages
- 커밋 타입 선택 / Select commit types
- 커밋 템플릿 구성 / Configure commit templates
- 사용자 정의 커밋 타입 추가 및 삭제 / Add and delete custom commit types
- 검색 기능을 통한 커밋 타입 선택 / Select commit types through search functionality

## 설치 방법 / How To Install

repository의 root에 있는 `install.sh`을 실행하거나 스크립트의 내용을 참고하여 실행하세요.

You can either download the install.sh script from the repository root or refer to its contents to run the commands manually.

만약 `install.sh`를 다운로드 받았다면 해당 파일에 실행 권한을 부여해주세요.

If you have downloaded install.sh, make sure to give it execute permission:

```
chmod +x install.sh
```

실행권한이 부여되었다면, 스크립트를 실행하세요.

Then, run the script:

```
./install.sh
```

## 사용 방법 / Usage

Snippy를 사용하여 커밋 메시지를 작성하는 방법은 다음과 같습니다.

To write a commit message using Snippy, follow these steps:

1. Snippy를 실행합니다. / Run Snippy.

```
snippy
```

2. 커밋 타입을 검색하여 선택합니다. / Search and select a commit type.

```
Select commit type:
----------------------------------------
Type to search commit types...
feat (✨) - A new feature
fix (🐛) - A bug fix
docs (📝) - Documentation only changes
style (💄) - Changes that do not affect the meaning of the code
refactor (♻️) - A code change that neither fixes a bug nor adds a feature
perf (⚡) - A code change that improves performance
test (✅) - Adding missing tests or correcting existing tests
chore (🔧) - Changes to the build process or auxiliary tools
```

3. 커밋 메시지를 입력합니다. / Enter the commit message.

```
Enter commit message:
```

4. Snippy가 커밋 메시지를 생성하고, Git 커밋을 수행합니다. / Snippy generates the commit message and performs the Git commit.

## 설정 / Configuration

Snippy의 설정을 변경하려면 다음 명령어를 사용합니다.

To change Snippy's configuration, use the following subcommand:

```
snippy config
```

설정 메뉴에서 커밋 템플릿과 커밋 타입을 구성할 수 있습니다.

In the configuration menu, you can configure commit templates and commit types.

```
Current Configuration:
----------------------------------------
Template:
  <type>: <emoji> <subject> (e.g: feat: ✨ This is example comment.)

Commit types:
  <emoji> option is on
  <type> option is on

  feat: ✨
  fix: 🐛
  docs: 📝
  style: 💄
  refactor: ♻️
  perf: ⚡
  test: ✅
  chore: 🔧
----------------------------------------
Do you want to configure (t)emplate, (c)ommit types, (r)eset to default, or (q)uit? :
```

## 초기화 / Reset

```
snippy reset
```

snippy의 설정을 처음으로 되돌릴 수 있습니다.

You can reset Snippy's configuration values to their default settings.

## 업데이트 / Update

```
snippy update
```

Snippy를 최신 버전으로 업데이트할 수 있습니다.

You can update Snippy to the latest version.

## 기여 / Contributing

Snippy에 기여하고 싶다면, GitHub 저장소를 포크하고 풀 리퀘스트를 제출해주세요.

If you want to contribute to Snippy, fork the GitHub repository and submit a pull request.

GitHub 저장소 / GitHub repository: https://github.com/narashin/snippy

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="http://nara.dev"><img src="https://avatars.githubusercontent.com/u/16604401?v=4?s=100" width="100px;" alt="nara"/><br /><sub><b>nara</b></sub></a><br /><a href="#maintenance-narashin" title="Maintenance">🚧</a><a href="#code-narashin" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://tigeryoo-portfolio.web.app/"><img src="https://avatars.githubusercontent.com/u/6271133?v=4?s=100" width="100px;" alt="TigerYoo"/><br /><sub><b>TigerYoo</b></sub></a><br /><a href="#bug-MTGVim" title="Bug reports">🐛</a><a href="#code-MTGVim" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
