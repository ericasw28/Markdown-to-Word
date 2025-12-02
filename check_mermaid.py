#!/usr/bin/env python3
"""Check if Mermaid CLI is properly installed"""

from helpers.mermaid_renderer import check_mermaid_cli_installed, get_mermaid_installation_instructions

if __name__ == "__main__":
    print("Checking Mermaid CLI installation...")
    print("-" * 50)

    if check_mermaid_cli_installed():
        print("✅ Mermaid CLI is installed and available!")
        print("\nYou can now use Mermaid diagram rendering in your conversions.")
    else:
        print("❌ Mermaid CLI is not installed or not in PATH")
        print(get_mermaid_installation_instructions())
