#!/bin/bash

# PyInstaller를 사용하여 snippy를 빌드합니다.
pyinstaller --onefile snippy/main.py --name snippy

# 빌드된 파일의 경로
DIST_FILE="dist/snippy"

# sha256 값을 계산합니다.
SHA256=$(shasum -a 256 "$DIST_FILE" | awk '{ print $1 }')

# sha256 값을 출력합니다.
echo "SHA256: $SHA256"

# snippy.rb 파일을 업데이트합니다.
cat <<EOF > snippy.rb
class Snippy < Formula
  desc "CLI tool for Git commit templates with emoji support"
  homepage "https://github.com/narashin/snippy"
  url "https://github.com/narashin/snippy/releases/download/v0.2/snippy"
  sha256 "$SHA256"
  license "MIT"

  def install
    bin.install "snippy"
  end

  test do
    system "#{bin}/snippy", "--help"
  end
end
EOF