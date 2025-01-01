class Snippy < Formula
  desc "CLI tool for Git commit templates with emoji support"
  homepage "https://github.com/narashin/snippy"
  url "https://github.com/narashin/snippy/releases/download/v0.4/snippy"
  sha256 "972afc1b44c49e98c573c6de9f577a8d431694bc2452cc552d39d0ee5973cc80"
  license "MIT"

  def install
    bin.install "snippy"
  end

  test do
    system "#{bin}/snippy", "--help"
  end
  end