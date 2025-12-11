"""Pandoc content sanitization"""

from .yaml_stripper import strip_yaml_frontmatter
from .emoji_remover import remove_emojis


def sanitize_for_pandoc(markdown_content):
    """Sanitize markdown content to avoid Pandoc YAML parsing issues"""
    # First strip YAML frontmatter
    content = strip_yaml_frontmatter(markdown_content)

    # Remove emojis that LaTeX can't handle
    content = remove_emojis(content)

    # Replace any standalone --- with explicit LaTeX horizontal rule
    # This prevents Pandoc from trying to parse them as YAML delimiters
    # and ensures they render properly in PDF
    lines = content.split('\n')
    sanitized_lines = []

    for line in lines:
        # If line is exactly ---, replace with LaTeX hrule
        if line.strip() == '---':
            # Use raw LaTeX block for explicit horizontal rule
            sanitized_lines.append('')
            sanitized_lines.append('```{=latex}')
            sanitized_lines.append('\\vspace{0.5em}')
            sanitized_lines.append('\\noindent\\rule{\\textwidth}{0.4pt}')
            sanitized_lines.append('\\vspace{0.5em}')
            sanitized_lines.append('```')
            sanitized_lines.append('')
        else:
            sanitized_lines.append(line)

    return '\n'.join(sanitized_lines)
