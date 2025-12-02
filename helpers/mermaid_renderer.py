"""Mermaid diagram rendering to images"""

import tempfile
import os
import subprocess
from io import BytesIO
from PIL import Image


def render_mermaid_to_png(mermaid_code, output_path=None):
    """
    Render Mermaid diagram code to PNG image

    Args:
        mermaid_code: The Mermaid diagram code
        output_path: Optional output path. If None, returns BytesIO

    Returns:
        BytesIO buffer or path to saved PNG

    Requires:
        - Node.js installed
        - @mermaid-js/mermaid-cli installed (npm install -g @mermaid-js/mermaid-cli)
    """
    # Create temporary file for mermaid code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, encoding='utf-8') as temp_mmd:
        temp_mmd.write(mermaid_code)
        temp_mmd_path = temp_mmd.name

    # Create temporary output file
    if output_path is None:
        temp_png = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        temp_png_path = temp_png.name
        temp_png.close()
    else:
        temp_png_path = output_path

    try:
        # Try to render using mmdc (mermaid-cli)
        result = subprocess.run(
            ['mmdc', '-i', temp_mmd_path, '-o', temp_png_path, '-b', 'transparent'],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            raise Exception(f"Mermaid rendering failed: {result.stderr}")

        # Read the PNG into a buffer
        if output_path is None:
            with open(temp_png_path, 'rb') as png_file:
                buffer = BytesIO(png_file.read())
            buffer.seek(0)
            return buffer
        else:
            return temp_png_path

    finally:
        # Clean up temporary files
        if os.path.exists(temp_mmd_path):
            os.remove(temp_mmd_path)
        if output_path is None and os.path.exists(temp_png_path):
            os.remove(temp_png_path)


def check_mermaid_cli_installed():
    """Check if mermaid-cli is installed"""
    try:
        result = subprocess.run(
            ['mmdc', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def get_mermaid_installation_instructions():
    """Get installation instructions for Mermaid CLI"""
    return """
    To enable Mermaid diagram rendering, you need to install the Mermaid CLI:

    1. Install Node.js (if not already installed):
       - macOS: brew install node
       - Windows: Download from https://nodejs.org
       - Linux: sudo apt install nodejs npm

    2. Install Mermaid CLI globally:
       npm install -g @mermaid-js/mermaid-cli

    3. Verify installation:
       mmdc --version
    """
