class Snippy < Formula
  desc "CLI tool for Git commit templates with emoji support"
  homepage "https://github.com/narashin/snippy"
  url "https://github.com/narashin/snippy/releases/download/v0.5/snippy"
  sha256 "b689b33475858da1ad45ef21deaf8743ab02168ecb8d383338a36998d9da918a"
  license "MIT"

  def install
    bin.install "snippy"
  end

  test do
    system "#{bin}/snippy", "--help"
  end
  end