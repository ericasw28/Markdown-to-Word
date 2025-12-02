"""
Header/Footer Processor
Handles variable substitution and LaTeX generation for headers/footers
"""

import re
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from pathlib import Path


class HeaderFooterProcessor:
    """Processes header/footer templates and generates LaTeX code"""

    def __init__(self, preset_config: Dict[str, Any], default_variables: Dict[str, str]):
        """
        Initialize processor

        Args:
            preset_config: Preset configuration with header/footer/style settings
            default_variables: Default variable values
        """
        self.preset_config = preset_config
        self.default_variables = default_variables
        self.frontmatter_variables = {}

    def extract_frontmatter(self, markdown_content: str) -> Tuple[Dict[str, str], str]:
        """
        Extract YAML frontmatter from markdown content

        Args:
            markdown_content: Markdown file content

        Returns:
            Tuple of (frontmatter_dict, content_without_frontmatter)
        """
        frontmatter = {}
        content = markdown_content

        # Check for YAML frontmatter (--- at start)
        frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(frontmatter_pattern, markdown_content, re.DOTALL)

        if match:
            # Extract frontmatter
            frontmatter_text = match.group(1)
            content = markdown_content[match.end():]

            # Parse simple YAML (key: value pairs)
            for line in frontmatter_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    frontmatter[key] = value

        self.frontmatter_variables = frontmatter
        return frontmatter, content

    def _substitute_variables(self, text: str, variables: Dict[str, str]) -> str:
        """
        Substitute variables in text

        Args:
            text: Text with {variable} placeholders
            variables: Dictionary of variable values

        Returns:
            Text with variables substituted
        """
        if not text:
            return ""

        # Handle automatic variables
        auto_vars = {
            'current_date': datetime.now().strftime('%Y-%m-%d'),
            'current_time': datetime.now().strftime('%H:%M'),
            'page': r'\thepage',  # LaTeX command for current page
            'total': r'\pageref{LastPage}'  # LaTeX command for total pages
        }

        # Merge all variable sources (priority: frontmatter > default > auto)
        all_vars = {**auto_vars, **self.default_variables, **variables, **self.frontmatter_variables}

        # Replace {variable} patterns
        result = text
        for key, value in all_vars.items():
            pattern = '{' + key + '}'
            result = result.replace(pattern, str(value))

        return result

    def _escape_latex(self, text: str) -> str:
        """
        Escape special LaTeX characters, but preserve LaTeX commands

        Args:
            text: Text to escape

        Returns:
            LaTeX-safe text
        """
        if not text:
            return ""

        # Don't escape if the text contains LaTeX commands (backslash present)
        # This preserves commands like \thepage, \pageref{LastPage}, etc.
        if '\\' in text:
            return text

        # Escape special LaTeX characters only in plain text
        replacements = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '~': r'\textasciitilde{}',
            '^': r'\^{}',
        }

        result = text
        for char, replacement in replacements.items():
            result = result.replace(char, replacement)

        return result

    def generate_latex_header(self, custom_variables: Optional[Dict[str, str]] = None) -> str:
        """
        Generate LaTeX header code for fancyhdr

        Args:
            custom_variables: Optional custom variables to override defaults

        Returns:
            LaTeX code for headers/footers
        """
        if not self.preset_config.get('enabled', False):
            return ""

        variables = custom_variables or {}

        # Get configuration
        header = self.preset_config.get('header', {})
        footer = self.preset_config.get('footer', {})
        style = self.preset_config.get('style', {})

        # Substitute variables in header/footer content
        header_left = self._substitute_variables(header.get('left', ''), variables)
        header_center = self._substitute_variables(header.get('center', ''), variables)
        header_right = self._substitute_variables(header.get('right', ''), variables)

        footer_left = self._substitute_variables(footer.get('left', ''), variables)
        footer_center = self._substitute_variables(footer.get('center', ''), variables)
        footer_right = self._substitute_variables(footer.get('right', ''), variables)

        # Escape LaTeX special characters (but preserve LaTeX commands)
        header_left = self._escape_latex(header_left)
        header_center = self._escape_latex(header_center)
        header_right = self._escape_latex(header_right)

        footer_left = self._escape_latex(footer_left)
        footer_center = self._escape_latex(footer_center)
        footer_right = self._escape_latex(footer_right)

        # Get style settings
        separator_line = style.get('separator_line', True)
        font_size = style.get('font_size', '10pt')

        # Generate LaTeX code
        latex_code = r'''
% Header and Footer Configuration
\usepackage{fancyhdr}
\usepackage{lastpage}  % For total page count

\pagestyle{fancy}
\fancyhf{}  % Clear all header/footer fields

'''

        # Add header configuration
        latex_code += f"% Header\n"
        if header_left:
            latex_code += f"\\fancyhead[L]{{{header_left}}}\n"
        if header_center:
            latex_code += f"\\fancyhead[C]{{{header_center}}}\n"
        if header_right:
            latex_code += f"\\fancyhead[R]{{{header_right}}}\n"

        latex_code += "\n"

        # Add footer configuration
        latex_code += f"% Footer\n"
        if footer_left:
            latex_code += f"\\fancyfoot[L]{{{footer_left}}}\n"
        if footer_center:
            latex_code += f"\\fancyfoot[C]{{{footer_center}}}\n"
        if footer_right:
            latex_code += f"\\fancyfoot[R]{{{footer_right}}}\n"

        latex_code += "\n"

        # Add separator line configuration
        if separator_line:
            latex_code += r"\renewcommand{\headrulewidth}{0.4pt}" + "\n"
            latex_code += r"\renewcommand{\footrulewidth}{0.4pt}" + "\n"
        else:
            latex_code += r"\renewcommand{\headrulewidth}{0pt}" + "\n"
            latex_code += r"\renewcommand{\footrulewidth}{0pt}" + "\n"

        latex_code += "\n"

        # Add font size configuration
        latex_code += f"% Header/Footer font size\n"
        latex_code += r"\fancyhfoffset{0pt}" + "\n"

        return latex_code

    def process_markdown_file(self, markdown_path: str, custom_variables: Optional[Dict[str, str]] = None) -> Tuple[str, str]:
        """
        Process markdown file and extract variables from frontmatter

        Args:
            markdown_path: Path to markdown file
            custom_variables: Optional custom variables to override defaults

        Returns:
            Tuple of (latex_header, processed_markdown_content)
        """
        # Read markdown file
        with open(markdown_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract frontmatter
        frontmatter, processed_content = self.extract_frontmatter(content)

        # Generate LaTeX header with merged variables
        latex_header = self.generate_latex_header(custom_variables)

        return latex_header, processed_content

    def preview_header_footer(self, custom_variables: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Generate a preview of what the header/footer will look like

        Args:
            custom_variables: Optional custom variables

        Returns:
            Dictionary with substituted header/footer values
        """
        variables = custom_variables or {}

        header = self.preset_config.get('header', {})
        footer = self.preset_config.get('footer', {})

        return {
            'header_left': self._substitute_variables(header.get('left', ''), variables),
            'header_center': self._substitute_variables(header.get('center', ''), variables),
            'header_right': self._substitute_variables(header.get('right', ''), variables),
            'footer_left': self._substitute_variables(footer.get('left', ''), variables),
            'footer_center': self._substitute_variables(footer.get('center', ''), variables),
            'footer_right': self._substitute_variables(footer.get('right', ''), variables),
        }


def create_processor_from_preset(preset_name: str, template_manager) -> HeaderFooterProcessor:
    """
    Create a HeaderFooterProcessor from a preset name

    Args:
        preset_name: Name of the preset to use
        template_manager: TemplateManager instance

    Returns:
        HeaderFooterProcessor instance
    """
    preset = template_manager.get_preset(preset_name)
    default_vars = template_manager.get_default_variables()

    return HeaderFooterProcessor(preset, default_vars)
