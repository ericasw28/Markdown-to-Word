#!/usr/bin/env python3
"""
Test script for header/footer generation
"""

from helpers.pdf_converter import convert_to_pdf
import os

# Read test markdown file
with open('test_simple.md', 'r', encoding='utf-8') as f:
    markdown_content = f.read()

print("Testing header/footer generation...")
print("=" * 50)

# Test 1: Professional preset with custom variables
print("\n1. Testing 'professional' preset with custom variables...")
try:
    custom_vars = {
        'title': 'Test Document',
        'author': 'John Doe',
        'company': 'Acme Corp'
    }

    pdf_buffer = convert_to_pdf(
        markdown_content,
        use_header_footer=True,
        header_footer_preset='professional',
        custom_variables=custom_vars
    )

    # Save to file
    output_path = 'test_output_professional.pdf'
    with open(output_path, 'wb') as f:
        f.write(pdf_buffer.read())

    print(f"✅ Success! PDF saved to: {output_path}")
    print(f"   File size: {os.path.getsize(output_path)} bytes")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Academic preset
print("\n2. Testing 'academic' preset...")
try:
    custom_vars = {
        'title': 'Research Paper',
        'author': 'Dr. Smith'
    }

    pdf_buffer = convert_to_pdf(
        markdown_content,
        use_header_footer=True,
        header_footer_preset='academic',
        custom_variables=custom_vars
    )

    output_path = 'test_output_academic.pdf'
    with open(output_path, 'wb') as f:
        f.write(pdf_buffer.read())

    print(f"✅ Success! PDF saved to: {output_path}")
    print(f"   File size: {os.path.getsize(output_path)} bytes")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Minimal preset
print("\n3. Testing 'minimal' preset...")
try:
    pdf_buffer = convert_to_pdf(
        markdown_content,
        use_header_footer=True,
        header_footer_preset='minimal',
        custom_variables={}
    )

    output_path = 'test_output_minimal.pdf'
    with open(output_path, 'wb') as f:
        f.write(pdf_buffer.read())

    print(f"✅ Success! PDF saved to: {output_path}")
    print(f"   File size: {os.path.getsize(output_path)} bytes")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: No header/footer
print("\n4. Testing without headers/footers...")
try:
    pdf_buffer = convert_to_pdf(
        markdown_content,
        use_header_footer=False
    )

    output_path = 'test_output_no_header.pdf'
    with open(output_path, 'wb') as f:
        f.write(pdf_buffer.read())

    print(f"✅ Success! PDF saved to: {output_path}")
    print(f"   File size: {os.path.getsize(output_path)} bytes")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 50)
print("Testing complete!")
print("\nGenerated files:")
print("- test_output_professional.pdf")
print("- test_output_academic.pdf")
print("- test_output_minimal.pdf")
print("- test_output_no_header.pdf")
