#!/bin/bash

echo "🐧 Snippy Installer Script 🛠️"

# Check if Homebrew is installed
if ! command -v brew &>/dev/null; then
    echo "🚨 Homebrew is not installed! Installing now... 🍺"

    # Install Homebrew
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Verify installation
    if ! command -v brew &>/dev/null; then
        echo "❌ Homebrew installation failed! Please install it manually."
        exit 1
    fi

    echo "✅ Homebrew installed successfully!"
else
    echo "🎉 Homebrew is already installed!"
fi

# Install Snippy
echo "✨ Installing Snippy... 📝"
brew tap narashin/snippy
brew install snippy

echo "🎊 Snippy installation complete! 🚀 Enjoy using it!"
