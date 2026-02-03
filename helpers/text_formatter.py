"""Text formatting with inline styles"""

from .inline_formatter import process_inline_element


def add_formatted_text(paragraph, element):
    """Add text with formatting (bold, italic, code, links) to a paragraph"""
    for child in element.children:
        if isinstance(child, str):
            # Plain text node - preserve spaces
            text = child
            if text:
                paragraph.add_run(text)
        elif child.name in ['strong', 'b', 'em', 'i', 'code', 'a', 'mark']:
            # Inline formatting (added 'mark' for highlighting)
            process_inline_element(paragraph, child)
        else:
            # Nested elements, recurse
            for nested in child.descendants:
                if isinstance(nested, str):
                    text = nested
                    if text:
                        paragraph.add_run(text)
