"""Pandoc content sanitization"""

from .yaml_stripper import strip_yaml_frontmatter
from .emoji_remover import remove_emojis


def sanitize_for_pandoc(markdown_content):
    """Sanitize markdown content to avoid Pandoc YAML parsing issues"""
    # First strip YAML frontmatter
    content = strip_yaml_frontmatter(markdown_content)

    # Remove emojis that LaTeX can't handle
    content = remove_emojis(content)

    # Replace any standalone --- with a safe alternative
    # This prevents Pandoc from trying to parse them as YAML delimiters
    lines = content.split('\n')
    sanitized_lines = []

    for line in lines:
        # If line is exactly ---, replace with ___
        if line.strip() == '---':
            sanitized_lines.append('___')
        else:
            sanitized_lines.append(line)

    return '\n'.join(sanitized_lines)
