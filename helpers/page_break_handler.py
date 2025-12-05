"""Shared page break detection and conversion logic

This module provides unified page break handling for both PDF and DOCX converters,
ensuring consistent behavior across output formats.
"""

import re
from typing import Tuple, List


def is_in_code_block_or_yaml(line_index: int, line: str, state: dict) -> Tuple[bool, dict]:
    """Track whether we're inside a code block or YAML frontmatter

    Args:
        line_index: Current line number (0-indexed)
        line: Current line content
        state: Dictionary tracking parser state

    Returns:
        Tuple of (is_inside_special_block, updated_state)
    """
    if state is None:
        state = {
            'in_code_block': False,
            'in_yaml_frontmatter': False,
            'yaml_fence_count': 0,
            'code_fence': ''
        }

    stripped = line.strip()

    # Track YAML frontmatter (only at start of document)
    if line_index == 0 and stripped == '---':
        state['in_yaml_frontmatter'] = True
        state['yaml_fence_count'] = 1
        return True, state
    elif state['in_yaml_frontmatter'] and stripped == '---':
        state['yaml_fence_count'] += 1
        if state['yaml_fence_count'] == 2:
            state['in_yaml_frontmatter'] = False
        return True, state
    elif state['in_yaml_frontmatter']:
        return True, state

    # Track code blocks
    if stripped.startswith('```') or stripped.startswith('~~~'):
        if not state['in_code_block']:
            state['in_code_block'] = True
            state['code_fence'] = stripped[:3]
            return True, state
        elif stripped.startswith(state['code_fence']):
            state['in_code_block'] = False
            state['code_fence'] = ''
            return True, state

    # Return current code block state
    return state['in_code_block'], state


def is_page_break_marker(line: str) -> bool:
    """Check if a line is a page break marker

    Supports:
    1. HTML comments: <!-- pagebreak -->, <!-- page-break -->, <!-- newpage -->
    2. Raw LaTeX: \\newpage
    3. Horizontal rules: ---, ***, ___

    Args:
        line: Line to check

    Returns:
        True if line is a page break marker
    """
    stripped = line.strip()

    # Check for HTML comment page breaks
    if re.match(r'^\s*<!--\s*(page[-_\s]?break|newpage)\s*-->\s*$', stripped, re.IGNORECASE):
        return True

    # Check for raw LaTeX \newpage
    if re.match(r'^\\newpage\s*$', stripped):
        return True

    # Check for horizontal rules (only if truly standalone)
    if re.match(r'^[-*_]{3,}$', stripped) and stripped == line.strip():
        return True

    return False


def convert_page_breaks_to_latex(content: str) -> str:
    """Convert all page break markers to LaTeX \\newpage commands

    Code-block aware - won't convert markers inside:
    - Fenced code blocks (```)
    - YAML frontmatter

    Args:
        content: Markdown content

    Returns:
        Content with page breaks converted to \\newpage
    """
    lines = content.split('\n')
    result = []
    state = None

    for i, line in enumerate(lines):
        inside_special, state = is_in_code_block_or_yaml(i, line, state)

        if inside_special:
            result.append(line)
            continue

        if is_page_break_marker(line):
            result.append('')
            result.append('\\newpage')
            result.append('')
        else:
            result.append(line)

    return '\n'.join(result)


def convert_page_breaks_to_placeholder(content: str, placeholder: str = '|||PAGEBREAK|||') -> str:
    """Convert all page break markers to a custom placeholder

    Useful for DOCX processing where we need a unique marker that survives
    HTML conversion.

    Code-block aware - won't convert markers inside:
    - Fenced code blocks (```)
    - YAML frontmatter

    Args:
        content: Markdown content
        placeholder: Placeholder text to use

    Returns:
        Content with page breaks converted to placeholder
    """
    lines = content.split('\n')
    result = []
    state = None

    for i, line in enumerate(lines):
        inside_special, state = is_in_code_block_or_yaml(i, line, state)

        if inside_special:
            result.append(line)
            continue

        if is_page_break_marker(line):
            result.append(placeholder)
        else:
            result.append(line)

    return '\n'.join(result)
