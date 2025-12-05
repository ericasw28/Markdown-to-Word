"""Obsidian syntax preprocessing for HTML/DOCX output

This module converts Obsidian-specific syntax to HTML-friendly Markdown,
unlike obsidian_preprocessor.py which outputs LaTeX.
"""

import re
from typing import List
from .table_width_optimizer import optimize_table_widths


def convert_obsidian_images_html(content: str) -> str:
    """Convert ![[image.png]] to standard markdown ![](image.png)"""
    content = re.sub(
        r'!\[\[([^\]|]+?)(?:\|([^\]]+))?\]\]',
        lambda m: f'![]({m.group(1)})',
        content
    )
    return content


def convert_wikilinks_html(content: str) -> str:
    """Convert [[wikilink]] to plain text or standard links"""
    # Remove section links like [[Note#Section]]
    content = re.sub(r'!\[\[([^\]]+?)#([^\]]+?)\]\]', r'', content)

    # Convert regular wikilinks to plain text
    content = re.sub(r'\[\[([^\]|]+?)(?:\|([^\]]+))?\]\]', r'\2' if r'\2' else r'\1', content)
    return content


def convert_extended_checkboxes_html(content: str) -> str:
    """Convert Obsidian extended checkboxes to standard checkboxes with emoji

    Uses the same emoji mapping as the LaTeX version but outputs
    markdown-compatible format.
    """
    # Simple checkbox emoji mapping
    CHECKBOX_EMOJI = {
        '!': '⚠️',  # Important
        '/': '🔄',  # In Progress
        'd': '💪',  # Doing
        '-': '❌',  # Dropped
        '>': '➡️',  # Forwarded
        '?': '❓',  # Question
        'R': '🔍',  # Research
        '+': '➕',  # To Add
        'i': '💡',  # Idea
        'P': '✅',  # Pro
        'C': '❌',  # Con
        'N': '📝',  # Note
        'D': '📅',  # Date
    }

    lines = content.split('\n')
    result = []

    for line in lines:
        # Match extended checkbox patterns: - [X] text
        match = re.match(r'^(\s*)- \[(.)\] (.+)$', line)
        if match:
            indent, checkbox_type, text = match.groups()

            # Keep standard checkboxes as-is
            if checkbox_type in [' ', 'x', 'X']:
                result.append(line)
            # Convert extended checkboxes to standard checkbox + emoji
            elif checkbox_type in CHECKBOX_EMOJI:
                emoji = CHECKBOX_EMOJI[checkbox_type]
                result.append(f'{indent}- [x] {emoji} {text}')
            else:
                # Unknown type, keep as-is
                result.append(line)
        else:
            result.append(line)

    return '\n'.join(result)


def convert_callouts_html(content: str) -> str:
    """Convert Obsidian callouts to blockquotes with title

    Since we can't use LaTeX tcolorbox in HTML, we convert callouts
    to styled blockquotes that will render nicely in Word.

    Example:
        > [!note] My Note
        > Content

    Becomes:
        > **NOTE: My Note**
        >
        > Content
    """
    lines = content.split('\n')
    converted_lines = []
    in_callout = False
    callout_type = None
    callout_title = None
    callout_content = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check for callout start: > [!type] title
        callout_match = re.match(r'^>\s*\[!(\w+)\](?:\s+(.+))?', line)

        if callout_match:
            # If we were already in a callout, close it
            if in_callout:
                converted_lines.extend(_format_callout_html(callout_type, callout_title, callout_content))
                callout_content = []

            # Start new callout
            in_callout = True
            callout_type = callout_match.group(1).lower()
            callout_title = callout_match.group(2) or callout_type.capitalize()

        elif in_callout:
            # Check if line is part of callout (starts with >)
            if line.startswith('>'):
                # Remove the > prefix and add to content
                callout_content.append(line[1:].lstrip())
            else:
                # Callout ended
                converted_lines.extend(_format_callout_html(callout_type, callout_title, callout_content))
                in_callout = False
                callout_type = None
                callout_title = None
                callout_content = []
                converted_lines.append(line)
        else:
            converted_lines.append(line)

        i += 1

    # Close any remaining callout
    if in_callout:
        converted_lines.extend(_format_callout_html(callout_type, callout_title, callout_content))

    return '\n'.join(converted_lines)


def _format_callout_html(callout_type: str, title: str, content: List[str]) -> List[str]:
    """Format a callout as a blockquote with bold title

    This creates a visually distinct blockquote that will render in Word
    with proper styling.
    """
    # Get emoji for callout type
    callout_icons = {
        'note': '📝',
        'info': 'ℹ️',
        'tip': '💡',
        'warning': '⚠️',
        'danger': '⚡',
        'error': '❌',
        'bug': '🐛',
        'example': '📋',
        'success': '✅',
        'question': '❓',
    }

    icon = callout_icons.get(callout_type.lower(), '📌')
    type_label = callout_type.upper()

    # Create blockquote with bold header
    result = [
        '',
        f'> **{icon} {type_label}: {title}**',
        '>',
    ]

    # Add content lines
    for line in content:
        if line.strip():
            result.append(f'> {line}')
        else:
            result.append('>')

    result.append('')

    return result


def convert_highlighting_html(content: str) -> str:
    """Convert ==highlighted text== to HTML mark tags

    The markdown library will convert <mark> tags to proper HTML.
    """
    # Replace ==text== with <mark>text</mark>
    content = re.sub(r'==([^=]+)==', r'<mark>\1</mark>', content)
    return content


def convert_underline_html(content: str) -> str:
    """Convert <u>text</u> to underlined text

    HTML <u> tags are already supported, so just keep them as-is.
    This function is here for consistency with the LaTeX version.
    """
    # <u> tags are already valid HTML, no conversion needed
    return content


def fix_list_blank_lines(content: str) -> str:
    """Ensure blank lines before bullet/numbered lists

    Same as the LaTeX version - needed for proper HTML rendering too.
    """
    lines = content.split('\n')
    result = []

    for i, line in enumerate(lines):
        # Check if current line starts a list (bullet or numbered)
        is_list_item = re.match(r'^(\s*)[-*+]\s+', line) or re.match(r'^(\s*)\d+\.\s+', line)

        if is_list_item and i > 0:
            prev_line = lines[i - 1]
            # Check if previous line is not blank and not a list item
            prev_is_blank = prev_line.strip() == ''
            prev_is_list = re.match(r'^(\s*)[-*+]\s+', prev_line) or re.match(r'^(\s*)\d+\.\s+', prev_line)

            # If previous line has content and is not a list item, add blank line
            if not prev_is_blank and not prev_is_list:
                result.append('')  # Add blank line

        result.append(line)

    return '\n'.join(result)


def preprocess_obsidian_for_html(content: str) -> str:
    """Main preprocessing function for HTML/DOCX output

    Converts Obsidian syntax to HTML-friendly Markdown (not LaTeX).

    Args:
        content: Raw markdown content with Obsidian syntax

    Returns:
        Preprocessed markdown content compatible with HTML converters
    """
    # Order matters! Process in this sequence:

    # 0. Optimize table column widths
    content = optimize_table_widths(content)

    # 1. Fix missing blank lines before lists
    content = fix_list_blank_lines(content)

    # 2. Convert callouts to blockquotes
    content = convert_callouts_html(content)

    # 3. Convert Obsidian-specific links and embeds
    content = convert_obsidian_images_html(content)
    content = convert_wikilinks_html(content)

    # 4. Convert extended checkboxes
    content = convert_extended_checkboxes_html(content)

    # 5. Convert text formatting (HTML-safe)
    content = convert_highlighting_html(content)
    content = convert_underline_html(content)

    return content
