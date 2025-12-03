"""Handle Mermaid diagrams in PDF conversion via Pandoc"""

import tempfile
import os
from PIL import Image
from .mermaid_detector import detect_mermaid_blocks
from .mermaid_renderer import render_mermaid_to_png


def prepare_markdown_with_mermaid_images(markdown_content):
    """
    Replace Mermaid code blocks with image references for Pandoc

    Returns:
        modified_markdown: Markdown with image references
        image_files: List of temporary image file paths to clean up later
    """
    mermaid_blocks = detect_mermaid_blocks(markdown_content)

    if not mermaid_blocks:
        return markdown_content, []

    image_files = []
    modified_content = markdown_content

    # Process blocks in reverse to maintain positions
    for idx, (start, end, code) in enumerate(reversed(mermaid_blocks)):
        diagram_id = len(mermaid_blocks) - idx - 1

        try:
            # Create temporary PNG file
            temp_png = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            temp_png_path = temp_png.name
            temp_png.close()

            # Render Mermaid to PNG
            render_mermaid_to_png(code, output_path=temp_png_path)
            image_files.append(temp_png_path)

            # Check diagram dimensions to prevent upscaling
            # With scale=2 rendering (2x resolution), images are 2x their natural size
            # Strategy: Display at half the pixel width (natural size), with max constraints
            img = Image.open(temp_png_path)
            img_width = img.width
            img.close()

            # Calculate the natural display size (scale 2 means divide by 2)
            # Then convert to points for LaTeX (assuming 96 DPI: 1px = 0.75pt)
            natural_width_pt = (img_width / 2) * 0.75

            # PDF text width is ~504pt (7 inches at 72pt/inch)
            max_width_pt = 504 * 0.85  # Use max 85% of text width

            if natural_width_pt > max_width_pt:
                # Large diagram - scale down to fit page (use percentage)
                size_attr = "{width=85%}"
            else:
                # Small/medium diagram - use natural size in points (prevents upscaling)
                size_attr = f"{{width={natural_width_pt:.0f}pt}}"

            # Replace with markdown image syntax using Pandoc's attribute format
            image_reference = f"\n\n![Figure {diagram_id + 1}: Mermaid Diagram]({temp_png_path}){size_attr}\n\n"
            modified_content = modified_content[:start] + image_reference + modified_content[end:]

        except Exception as e:
            # If rendering fails, replace with error message
            error_msg = f"\n\n*[Mermaid diagram rendering failed: {e}]*\n\n"
            modified_content = modified_content[:start] + error_msg + modified_content[end:]

    return modified_content, image_files


def cleanup_temp_images(image_files):
    """Clean up temporary image files"""
    for image_path in image_files:
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
            except Exception:
                pass  # Ignore cleanup errors
