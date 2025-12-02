"""Test script for simple document conversion"""

import sys
sys.path.insert(0, '.')

from helpers import convert_to_pdf

# Read the simple test file
with open('test_simple.md', 'r', encoding='utf-8') as f:
    markdown_content = f.read()

print("🔄 Converting test_simple.md to PDF...")
print("=" * 60)

try:
    # Convert to PDF with Obsidian mode enabled
    pdf_buffer = convert_to_pdf(markdown_content, render_mermaid=True, obsidian_mode=True)

    # Save the output
    with open('test_simple_output.pdf', 'wb') as f:
        f.write(pdf_buffer.getvalue())

    print("✅ Success! PDF generated: test_simple_output.pdf")
    print("📄 File size:", len(pdf_buffer.getvalue()), "bytes")

except Exception as e:
    print("❌ Error during conversion:")
    print(f"   {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=" * 60)
print("✨ Test completed successfully!")
