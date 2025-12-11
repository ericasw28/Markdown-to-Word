#!/usr/bin/env python3
"""Test PDF generation with the Proposition document"""

from helpers.pdf_converter import convert_to_pdf
from helpers.template_manager import TemplateManager
import os

# Read the proposition document
with open('tests/Proposition Mermaid pour Jira-Confluence.md', 'r', encoding='utf-8') as f:
    markdown_content = f.read()

print("Testing PDF generation with Proposition document...")
print("=" * 60)

# Test with logo enabled
try:
    # Setup template manager and enable logo
    template_manager = TemplateManager()

    # Enable logo in custom preset
    custom_preset = template_manager.get_preset('custom')
    custom_preset['logo']['enabled'] = True
    custom_preset['logo']['position'] = 'header_left'
    custom_preset['logo']['height'] = '0.8cm'
    template_manager.update_preset('custom', custom_preset)
    template_manager.save_template()

    custom_vars = {
        'title': 'Proposition Mermaid',
        'author': 'Eric Taylor',
        'company': 'Infogene',
        'version': '1'
    }

    pdf_buffer = convert_to_pdf(
        markdown_content,
        use_header_footer=True,
        header_footer_preset='custom',
        custom_variables=custom_vars
    )

    output_path = 'test_proposition_with_logo.pdf'
    with open(output_path, 'wb') as f:
        f.write(pdf_buffer.read())

    file_size = os.path.getsize(output_path)
    print(f"✅ Success! PDF saved to: {output_path}")
    print(f"   File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    print(f"   Logo enabled: {custom_preset['logo']['enabled']}")
    print(f"   Logo path: {custom_preset['logo']['path']}")
    print(f"   Logo position: {custom_preset['logo']['position']}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Testing complete!")
