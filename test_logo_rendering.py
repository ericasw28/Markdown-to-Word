#!/usr/bin/env python3
"""
Test script for logo rendering in headers/footers
"""

from helpers.pdf_converter import convert_to_pdf
from helpers.template_manager import TemplateManager
import os

# Read test markdown file
with open('tests/test_simple.md', 'r', encoding='utf-8') as f:
    markdown_content = f.read()

print("Testing logo rendering in headers/footers...")
print("=" * 60)

# Initialize template manager
template_manager = TemplateManager()

# Test configurations
test_configs = [
    {
        'name': 'header_left',
        'preset': 'professional',
        'logo_position': 'header_left',
        'description': 'Logo in header left with professional layout'
    },
    {
        'name': 'header_center',
        'preset': 'academic',
        'logo_position': 'header_center',
        'description': 'Logo in header center with academic layout'
    },
    {
        'name': 'header_right',
        'preset': 'minimal',
        'logo_position': 'header_right',
        'description': 'Logo in header right with minimal layout'
    },
    {
        'name': 'footer_left',
        'preset': 'detailed',
        'logo_position': 'footer_left',
        'description': 'Logo in footer left with detailed layout'
    },
    {
        'name': 'footer_center',
        'preset': 'professional',
        'logo_position': 'footer_center',
        'description': 'Logo in footer center'
    },
    {
        'name': 'footer_right',
        'preset': 'professional',
        'logo_position': 'footer_right',
        'description': 'Logo in footer right'
    },
]

# Run tests
for config in test_configs:
    print(f"\n{'='*60}")
    print(f"Test: {config['name']}")
    print(f"Description: {config['description']}")
    print(f"Preset: {config['preset']}")
    print(f"Position: {config['logo_position']}")
    print(f"{'='*60}")

    try:
        # Get preset and update logo configuration
        preset = template_manager.get_preset(config['preset'])
        logo_config = {
            'enabled': True,
            'path': 'config/logo.svg',
            'position': config['logo_position'],
            'height': '0.5cm',
            'width': ''
        }

        # Update preset with logo config
        preset['logo'] = logo_config
        template_manager.update_preset(config['preset'], preset)

        # Custom variables
        custom_vars = {
            'title': 'Test Document',
            'author': 'John Doe',
            'company': 'Acme Corp',
            'version': '1.0'
        }

        # Convert to PDF
        pdf_buffer = convert_to_pdf(
            markdown_content,
            use_header_footer=True,
            header_footer_preset=config['preset'],
            custom_variables=custom_vars
        )

        # Save to file
        output_path = f'test_logo_{config["name"]}.pdf'
        with open(output_path, 'wb') as f:
            f.write(pdf_buffer.read())

        file_size = os.path.getsize(output_path)
        print(f"✅ Success! PDF saved to: {output_path}")
        print(f"   File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 60)
print("Testing complete!")
print("\nGenerated files:")
for config in test_configs:
    filename = f'test_logo_{config["name"]}.pdf'
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        print(f"  ✅ {filename} ({size/1024:.1f} KB)")
    else:
        print(f"  ❌ {filename} (not generated)")
