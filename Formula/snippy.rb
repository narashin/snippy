class Snippy < Formula
  desc "CLI tool for Git commit templates with emoji support"
  homepage "https://github.com/narashin/snippy"
  url "https://github.com/narashin/snippy/releases/download/v0.6/snippy"
  sha256 "a669d1aa598a100373011cebc0ca620a31dee81bdf0f9f6f798b3c9c73273ea4"
  license "MIT"

  def install
    bin.install "snippy"
  end

  test do
    system "#{bin}/snippy", "--help"
  end
  end