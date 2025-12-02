"""Mermaid diagram detection in Markdown"""

import re


def detect_mermaid_blocks(markdown_content):
    """
    Detect Mermaid code blocks in Markdown content
    Returns list of tuples: (start_pos, end_pos, mermaid_code)
    """
    mermaid_blocks = []

    # Pattern to match ```mermaid ... ```
    pattern = r'```mermaid\s*\n(.*?)```'

    for match in re.finditer(pattern, markdown_content, re.DOTALL):
        start_pos = match.start()
        end_pos = match.end()
        mermaid_code = match.group(1).strip()
        mermaid_blocks.append((start_pos, end_pos, mermaid_code))

    return mermaid_blocks


def replace_mermaid_with_placeholder(markdown_content, placeholder_format="![Mermaid Diagram {}](mermaid_{}.png)"):
    """
    Replace Mermaid blocks with image placeholders
    Returns: (modified_content, list of mermaid codes)
    """
    mermaid_blocks = detect_mermaid_blocks(markdown_content)

    if not mermaid_blocks:
        return markdown_content, []

    # Work backwards to maintain correct positions
    mermaid_codes = []
    modified_content = markdown_content

    for idx, (start, end, code) in enumerate(reversed(mermaid_blocks)):
        diagram_idx = len(mermaid_blocks) - idx - 1
        placeholder = placeholder_format.format(diagram_idx, diagram_idx)
        modified_content = modified_content[:start] + placeholder + modified_content[end:]
        mermaid_codes.insert(0, code)

    return modified_content, mermaid_codes
