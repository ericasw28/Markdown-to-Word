#!/bin/bash

# Script to install required LaTeX packages for PDF conversion
# This installs packages needed for advanced formatting and code blocks

echo "==================================="
echo "LaTeX Package Installation Script"
echo "==================================="
echo ""

# Check if tlmgr is available
if ! command -v tlmgr &> /dev/null; then
    echo "❌ Error: tlmgr (TeX Live Manager) not found."
    echo "Please install TeX Live first:"
    echo "  - macOS: brew install --cask mactex"
    echo "  - Linux: sudo apt-get install texlive-full"
    exit 1
fi

echo "✅ tlmgr found"
echo ""

# Update tlmgr itself
echo "📦 Updating tlmgr..."
sudo tlmgr update --self

if [ $? -eq 0 ]; then
    echo "✅ tlmgr updated successfully"
else
    echo "⚠️  Warning: tlmgr update failed, continuing anyway..."
fi
echo ""

# Install required packages
PACKAGES=(
    "fvextra"          # Extended fancyvrb with line breaking for code blocks
    "ulem"             # Underline support
    "fontawesome5"     # Icon support for callouts
    "tcolorbox"        # Colored boxes for callouts
    "enumitem"         # Better list control
    "microtype"        # Typography improvements
    "fancyhdr"         # Headers and footers
    "lastpage"         # Page number reference
    "soul"             # Text highlighting
)

echo "📦 Installing LaTeX packages..."
echo ""

for package in "${PACKAGES[@]}"; do
    echo "Installing $package..."
    sudo tlmgr install "$package"

    if [ $? -eq 0 ]; then
        echo "  ✅ $package installed"
    else
        echo "  ⚠️  $package may already be installed or failed"
    fi
done

echo ""
echo "==================================="
echo "Installation Complete!"
echo "==================================="
echo ""
echo "Installed packages:"
for package in "${PACKAGES[@]}"; do
    echo "  - $package"
done
echo ""
echo "You can now run your PDF converter with advanced features enabled."
