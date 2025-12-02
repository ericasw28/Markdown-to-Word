"""YAML frontmatter removal"""


def strip_yaml_frontmatter(markdown_content):
    """Remove YAML frontmatter from markdown content"""
    lines = markdown_content.split('\n')

    # Check if content starts with YAML frontmatter (---)
    if lines and lines[0].strip() == '---':
        # Find the closing ---
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                # Return content after the closing ---
                return '\n'.join(lines[i+1:])

    # No frontmatter found, return original content
    return markdown_content
