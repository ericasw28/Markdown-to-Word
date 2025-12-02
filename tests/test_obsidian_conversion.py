"""Test script for Obsidian formatting conversion"""

import sys
sys.path.insert(0, '.')

from helpers import convert_to_pdf

# Read the Obsidian Formatting markdown file
with open('Obsidian Formatting.md', 'r', encoding='utf-8') as f:
    markdown_content = f.read()

print("🔄 Converting Obsidian Formatting.md to PDF...")
print("=" * 60)

try:
    # Convert to PDF with Obsidian mode enabled
    pdf_buffer = convert_to_pdf(markdown_content, render_mermaid=True, obsidian_mode=True)

    # Save the output
    with open('Obsidian_Formatting_Test.pdf', 'wb') as f:
        f.write(pdf_buffer.getvalue())

    print("✅ Success! PDF generated: Obsidian_Formatting_Test.pdf")
    print("📄 File size:", len(pdf_buffer.getvalue()), "bytes")

except Exception as e:
    print("❌ Error during conversion:")
    print(f"   {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=" * 60)
print("✨ Test completed!")
