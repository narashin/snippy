class Snippy < Formula
  desc "CLI tool for Git commit templates with emoji support"
  homepage "https://github.com/narashin/snippy"
  url "https://github.com/narashin/snippy/releases/download/v0.2/snippy"
  sha256 "10d61d5f0e106b06cf85baa2a98e961a94777d743f664403e6c575949b9308ef"
  license "MIT"

  def install
    bin.install "snippy"
  end

  test do
    system "#{bin}/snippy", "--help"
  end
end
