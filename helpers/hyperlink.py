"""Hyperlink creation for Word documents"""

from docx.oxml.shared import OxmlElement
from docx.oxml.ns import qn


def add_hyperlink(paragraph, url, text):
    """Add a hyperlink to a paragraph"""
    # This creates the hyperlink using low-level XML manipulation
    part = paragraph.part
    r_id = part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)

    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)

    new_run = OxmlElement('w:r')
    r_pr = OxmlElement('w:rPr')

    # Add hyperlink styling (blue and underlined)
    r_style = OxmlElement('w:rStyle')
    r_style.set(qn('w:val'), 'Hyperlink')
    r_pr.append(r_style)
    new_run.append(r_pr)

    new_run.text = text
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)

    return hyperlink
