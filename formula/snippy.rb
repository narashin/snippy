class Snippy < Formula
    desc "CLI tool for Git commit templates with emoji support"
    homepage "https://github.com/narashin/snippy"
    url "https://github.com/narashin/snippy/releases/download/v0.1/snippy"
    sha256 "4952ecbe6dee6ec00664e19839743f9f4946dea91fc4a9007ae3d2b8505fbf83"
    license "MIT"

    def install
      bin.install "snippy"
    end

    test do
      system "#{bin}/snippy", "--help"
    end
  end
