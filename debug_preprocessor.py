"""Debug script to see what the preprocessor outputs"""

import sys
sys.path.insert(0, '.')

from helpers import preprocess_obsidian_syntax

# Read the Obsidian Formatting markdown file
with open('Obsidian Formatting.md', 'r', encoding='utf-8') as f:
    markdown_content = f.read()

print("🔍 Preprocessing Obsidian syntax...")
print("=" * 60)

# Preprocess
processed = preprocess_obsidian_syntax(markdown_content)

# Save the preprocessed output
with open('Obsidian_Formatting_Preprocessed.md', 'w', encoding='utf-8') as f:
    f.write(processed)

print("✅ Preprocessed output saved to: Obsidian_Formatting_Preprocessed.md")
print("📄 You can review this file to see what Pandoc will receive")

# Show the LaTeX math section
lines = processed.split('\n')
in_latex_section = False
latex_section_lines = []

for i, line in enumerate(lines, 1):
    if 'Latex Math' in line:
        in_latex_section = True
        start = max(0, i - 5)
    elif in_latex_section and line.startswith('#'):
        # Found next section
        break

    if in_latex_section:
        latex_section_lines.append(f"{i}: {line}")

print("\n" + "=" * 60)
print("LaTeX Math section (preprocessed):")
print("=" * 60)
print("\n".join(latex_section_lines[:30]))  # First 30 lines
