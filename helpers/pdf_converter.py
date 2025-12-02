"""PDF conversion functionality"""

import pypandoc
from io import BytesIO
import tempfile
import os
from typing import Optional, Dict
from .pandoc_sanitizer import sanitize_for_pandoc
from .mermaid_pdf_handler import prepare_markdown_with_mermaid_images, cleanup_temp_images
from .obsidian_preprocessor import preprocess_obsidian_syntax, get_enhanced_latex_header
from .template_manager import TemplateManager
from .header_footer_processor import HeaderFooterProcessor, create_processor_from_preset


def convert_to_pdf(markdown_content, render_mermaid=True, obsidian_mode=True,
                   use_header_footer=True, header_footer_preset=None,
                   custom_variables=None):
    """Convert Markdown content to PDF format using pypandoc

    Args:
        markdown_content: The markdown content to convert
        render_mermaid: Whether to render Mermaid diagrams (default: True)
        obsidian_mode: Whether to preprocess Obsidian syntax (default: True)
        use_header_footer: Whether to include headers/footers (default: True)
        header_footer_preset: Preset name to use (default: None, uses current preset)
        custom_variables: Dictionary of custom variables for header/footer (default: None)
    """
    # Preprocess Obsidian syntax if enabled
    if obsidian_mode:
        markdown_content = preprocess_obsidian_syntax(markdown_content)

    # Handle Mermaid diagrams if enabled
    mermaid_image_files = []
    if render_mermaid:
        try:
            markdown_content, mermaid_image_files = prepare_markdown_with_mermaid_images(markdown_content)
        except Exception as e:
            print(f"Warning: Mermaid rendering disabled due to error: {e}")

    # Initialize header/footer processor if enabled
    header_footer_latex = ""
    if use_header_footer:
        try:
            template_manager = TemplateManager()

            # Use specified preset or current default
            if header_footer_preset:
                template_manager.set_current_preset(header_footer_preset)

            processor = create_processor_from_preset(
                template_manager.get_current_preset(),
                template_manager
            )

            # Extract frontmatter from markdown
            processor.extract_frontmatter(markdown_content)

            # Generate header/footer LaTeX code
            header_footer_latex = processor.generate_latex_header(custom_variables)
        except Exception as e:
            print(f"Warning: Header/footer generation failed: {e}")
            header_footer_latex = ""

    # Sanitize content to avoid YAML parsing errors
    cleaned_content = sanitize_for_pandoc(markdown_content)

    # Create temporary files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as temp_md:
        temp_md.write(cleaned_content)
        temp_md_path = temp_md.name

    # Create enhanced LaTeX header with Obsidian support
    temp_header = tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False, encoding='utf-8')
    if obsidian_mode:
        # Use LuaLaTeX-compatible header (avoids soul package conflict)
        temp_header.write(get_enhanced_latex_header(use_lualatex=True))
    else:
        # Basic header without Obsidian features
        temp_header.write('\\usepackage{float}\n')
        temp_header.write('\\let\\origfigure\\figure\n')
        temp_header.write('\\let\\endorigfigure\\endfigure\n')
        temp_header.write('\\renewenvironment{figure}[1][]{\\origfigure[H]}{\\endorigfigure}\n')

    # Add header/footer configuration if enabled
    if header_footer_latex:
        temp_header.write('\n')
        temp_header.write(header_footer_latex)

    temp_header_path = temp_header.name
    temp_header.close()

    # Create secure temporary file for PDF output
    temp_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    temp_pdf_path = temp_pdf.name
    temp_pdf.close()

    try:
        # Convert using pypandoc with error handling
        # Use lualatex for better Unicode/emoji support
        pypandoc.convert_file(
            temp_md_path,
            'pdf',
            outputfile=temp_pdf_path,
            extra_args=[
                '--pdf-engine=lualatex',
                '--from=markdown-yaml_metadata_block',
                '--variable=geometry:margin=0.75in',
                '--variable=colorlinks:true',
                '--include-in-header=' + temp_header_path,
                '--syntax-highlighting=tango'
            ]
        )

        # Read PDF into buffer
        with open(temp_pdf_path, 'rb') as pdf_file:
            buffer = BytesIO(pdf_file.read())

        buffer.seek(0)
        return buffer

    finally:
        # Clean up temporary files
        if os.path.exists(temp_md_path):
            os.remove(temp_md_path)
        if os.path.exists(temp_header_path):
            os.remove(temp_header_path)
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)
        # Clean up Mermaid image files
        cleanup_temp_images(mermaid_image_files)
