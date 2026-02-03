"""Inline element formatting for Word documents"""

from docx.shared import Pt, RGBColor
from docx.enum.text import WD_COLOR_INDEX
from .hyperlink import add_hyperlink


def process_inline_element(paragraph, elem):
    """Process inline elements recursively with formatting"""
    if elem.name == 'a':
        # Handle hyperlinks
        url = elem.get('href', '')
        if url:
            add_hyperlink(paragraph, url, elem.get_text())
    elif elem.name in ['strong', 'b']:
        # Bold text - process children recursively to preserve spaces
        _process_formatted_children(paragraph, elem, bold=True)
    elif elem.name in ['em', 'i']:
        # Italic text - process children recursively to preserve spaces
        _process_formatted_children(paragraph, elem, italic=True)
    elif elem.name == 'mark':
        # Highlighted text (from ==text== syntax)
        # Use yellow highlight color
        for child in elem.children:
            if isinstance(child, str):
                run = paragraph.add_run(child)
                run.font.highlight_color = WD_COLOR_INDEX.YELLOW
            else:
                # Recursively process nested elements
                process_inline_element(paragraph, child)
    elif elem.name == 'code':
        # Inline code - preserve exact text including spaces
        run = paragraph.add_run(elem.get_text())
        run.font.name = 'Courier New'
        run.font.size = Pt(10)
    else:
        # Regular text - preserve spaces
        paragraph.add_run(elem.get_text())


def _process_formatted_children(paragraph, elem, bold=False, italic=False):
    """Process children of formatted elements while preserving spaces"""
    for child in elem.children:
        if isinstance(child, str):
            # Direct text node - preserve all whitespace
            if child:
                run = paragraph.add_run(child)
                if bold:
                    run.bold = True
                if italic:
                    run.italic = True
        else:
            # Nested element
            if child.name in ['em', 'i']:
                # Bold + italic combination
                _process_formatted_children(paragraph, child, bold=bold, italic=True)
            elif child.name in ['strong', 'b']:
                # Italic + bold combination
                _process_formatted_children(paragraph, child, bold=True, italic=italic)
            else:
                # Other nested elements
                for text in child.children:
                    if isinstance(text, str) and text:
                        run = paragraph.add_run(text)
                        if bold:
                            run.bold = True
                        if italic:
                            run.italic = True
