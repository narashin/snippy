class Snippy < Formula
    desc "CLI tool for Git commit templates with emoji support"
    homepage "https://github.com/narashin/snippy"
    url "https://github.com/narashin/snippy/releases/download/v0.2/snippy"
    sha256 "6cf1587f4fa1d698025e89a0048a43cc08179e2621175869cc84c4d9834bd636"
    license "MIT"

    def install
      bin.install "snippy"
    end

    test do
      system "#{bin}/snippy", "--help"
    end
  end
