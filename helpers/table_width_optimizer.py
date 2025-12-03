"""Smart table width optimization for markdown tables

This module analyzes markdown pipe tables and calculates optimal column widths
based on content length, then converts them to LaTeX tables with proportional widths.
"""

import re
from typing import List, Tuple, Dict


def calculate_column_widths(rows: List[List[str]], min_width: float = 0.1, max_width: float = 0.6) -> List[float]:
    """Calculate optimal column widths based on content length

    Args:
        rows: List of rows, where each row is a list of cell contents
        min_width: Minimum width ratio for any column (default 0.1 = 10%)
        max_width: Maximum width ratio for any column (default 0.6 = 60%)

    Returns:
        List of width ratios that sum to 1.0
    """
    if not rows:
        return []

    num_cols = len(rows[0])
    if num_cols == 0:
        return []

    # Calculate average content length per column
    col_lengths = [0] * num_cols
    for row in rows:
        for i, cell in enumerate(row):
            if i < num_cols:
                # Weight longer content more heavily (sqrt to avoid extreme dominance)
                col_lengths[i] += len(cell.strip()) ** 0.7

    # Average across rows
    total_rows = len(rows)
    col_lengths = [length / total_rows for length in col_lengths]

    # Convert to ratios
    total_length = sum(col_lengths)
    if total_length == 0:
        # Equal widths if no content
        return [1.0 / num_cols] * num_cols

    ratios = [length / total_length for length in col_lengths]

    # Apply min/max constraints
    ratios = [max(min_width, min(max_width, r)) for r in ratios]

    # Renormalize to sum to 1.0
    total_ratio = sum(ratios)
    ratios = [r / total_ratio for r in ratios]

    return ratios


def parse_pipe_table(table_text: str) -> Tuple[List[str], List[List[str]]]:
    """Parse a markdown pipe table into header and rows

    Args:
        table_text: The markdown table text

    Returns:
        Tuple of (header_row, data_rows)
    """
    lines = table_text.strip().split('\n')
    if len(lines) < 2:
        return [], []

    # Parse header (first line)
    header_line = lines[0]
    headers = [cell.strip() for cell in header_line.split('|')]
    headers = [h for h in headers if h]  # Remove empty strings from leading/trailing |

    # Skip separator line (second line with dashes)
    # Parse data rows (remaining lines)
    data_rows = []
    for line in lines[2:]:
        if line.strip():
            cells = [cell.strip() for cell in line.split('|')]
            cells = [c for c in cells if c or cells.index(c) > 0]  # Keep empty cells except leading
            if cells:
                # Pad or trim to match header length
                while len(cells) < len(headers):
                    cells.append('')
                data_rows.append(cells[:len(headers)])

    return headers, data_rows


def markdown_to_latex(text: str) -> str:
    """Convert markdown formatting to LaTeX equivalents

    Args:
        text: Text with markdown formatting

    Returns:
        Text with LaTeX formatting
    """
    import re

    # Handle bold + italic: ***text*** or ___text___
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\\textbf{\\textit{\1}}', text)
    text = re.sub(r'___(.+?)___', r'\\textbf{\\textit{\1}}', text)

    # Handle bold: **text** or __text__
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    text = re.sub(r'__(.+?)__', r'\\textbf{\1}', text)

    # Handle italic: *text* or _text_ (but not in middle of words)
    text = re.sub(r'(?<!\w)\*(.+?)\*(?!\w)', r'\\textit{\1}', text)
    text = re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'\\textit{\1}', text)

    # Handle inline code: `code`
    text = re.sub(r'`(.+?)`', r'\\texttt{\1}', text)

    return text


def escape_latex_chars(text: str) -> str:
    """Escape special LaTeX characters in text

    Args:
        text: Text that may contain special LaTeX characters

    Returns:
        Text with LaTeX special characters escaped
    """
    # Order matters: backslash must be first
    replacements = [
        ('\\', r'\textbackslash{}'),
        ('&', r'\&'),
        ('%', r'\%'),
        ('$', r'\$'),
        ('#', r'\#'),
        ('_', r'\_'),
        ('{', r'\{'),
        ('}', r'\}'),
        ('~', r'\textasciitilde{}'),
        ('^', r'\textasciicircum{}'),
    ]

    for old, new in replacements:
        text = text.replace(old, new)

    return text


def process_cell_content(text: str) -> str:
    """Process table cell content: escape special chars, then convert markdown to LaTeX

    Args:
        text: Raw cell content with potential markdown formatting

    Returns:
        LaTeX-ready cell content
    """
    import re

    # Strategy: Process markdown patterns one by one, escaping content before wrapping

    # Define special char escaping (excluding markdown markers)
    def escape_special_chars(s: str) -> str:
        """Escape LaTeX special characters except markdown markers"""
        replacements = [
            ('&', r'\&'),
            ('%', r'\%'),
            ('$', r'\$'),
            ('#', r'\#'),
            ('{', r'\{'),
            ('}', r'\}'),
            ('~', r'\textasciitilde{}'),
            ('^', r'\textasciicircum{}'),
        ]
        for old, new in replacements:
            s = s.replace(old, new)
        return s

    # Process bold + italic: ***text*** or ___text___
    def process_bold_italic(match):
        content = escape_special_chars(match.group(1))
        # Escape underscores for this specific case
        content = content.replace('_', r'\_')
        return f'\\textbf{{\\textit{{{content}}}}}'

    text = re.sub(r'\*\*\*(.+?)\*\*\*', process_bold_italic, text)
    text = re.sub(r'___(.+?)___', process_bold_italic, text)

    # Process bold: **text** or __text__
    def process_bold(match):
        content = escape_special_chars(match.group(1))
        # Escape underscores for this specific case
        content = content.replace('_', r'\_')
        return f'\\textbf{{{content}}}'

    text = re.sub(r'\*\*(.+?)\*\*', process_bold, text)
    text = re.sub(r'__(.+?)__', process_bold, text)

    # Process italic: *text* or _text_
    def process_italic(match):
        content = escape_special_chars(match.group(1))
        # Escape underscores for this specific case
        content = content.replace('_', r'\_')
        return f'\\textit{{{content}}}'

    text = re.sub(r'(?<!\w)\*(.+?)\*(?!\w)', process_italic, text)
    text = re.sub(r'(?<!\w)_(.+?)_(?!\w)', process_italic, text)

    # Process inline code: `code`
    def process_code(match):
        content = escape_special_chars(match.group(1))
        # Escape underscores for code
        content = content.replace('_', r'\_')
        return f'\\texttt{{{content}}}'

    text = re.sub(r'`(.+?)`', process_code, text)

    # Now we need to escape remaining special chars, but NOT the ones in our LaTeX commands
    # Protect all LaTeX commands we just created
    import re as re_module
    latex_commands = []

    def protect_latex(match):
        latex_commands.append(match.group(0))
        return f'<<<LATEX{len(latex_commands)-1}>>>'

    # Protect all \textbf{...}, \textit{...}, \texttt{...} patterns (including nested ones)
    # Use a more robust pattern that handles nested braces
    text = re_module.sub(r'\\text(?:bf|it|tt)\{(?:[^{}]|\\text(?:bf|it|tt)\{[^{}]*\})*\}', protect_latex, text)

    # Now escape any remaining special characters
    text = escape_special_chars(text)
    text = text.replace('_', r'\_')

    # Restore LaTeX commands
    for i, cmd in enumerate(latex_commands):
        text = text.replace(f'<<<LATEX{i}>>>', cmd)

    return text


def convert_table_to_latex(headers: List[str], rows: List[List[str]], widths: List[float]) -> str:
    """Convert table data to LaTeX longtable with specified widths

    Args:
        headers: List of header cell contents
        rows: List of data rows
        widths: List of column width ratios (should sum to ~1.0)

    Returns:
        LaTeX table code as string
    """
    if not headers or not widths:
        return ""

    # Use 95% of textwidth to leave margins and prevent overflow
    total_width_ratio = 0.95

    # Calculate actual widths in terms of textwidth
    col_specs = []
    for width in widths:
        # Use p{width} for paragraph columns with specified width
        adjusted_width = width * total_width_ratio
        col_specs.append(f'p{{{adjusted_width:.3f}\\textwidth}}')

    col_spec_str = '|'.join(col_specs)

    # Build LaTeX table
    latex_lines = [
        '',
        '```{=latex}',
        '\\begin{longtable}[]{@{}' + col_spec_str + '@{}}',
        '\\toprule',
    ]

    # Add header row (process markdown and escape LaTeX special characters)
    processed_headers = [process_cell_content(h) for h in headers]
    header_str = ' & '.join(processed_headers) + ' \\\\'
    latex_lines.append(header_str)
    latex_lines.append('\\midrule')
    latex_lines.append('\\endhead')

    # Add data rows (process markdown and escape LaTeX special characters)
    for row in rows:
        processed_row = [process_cell_content(cell) for cell in row]
        row_str = ' & '.join(processed_row) + ' \\\\'
        latex_lines.append(row_str)

    # Close table
    latex_lines.append('\\bottomrule')
    latex_lines.append('\\end{longtable}')
    latex_lines.append('```')
    latex_lines.append('')

    return '\n'.join(latex_lines)


def optimize_table_widths(markdown_content: str) -> str:
    """Find all pipe tables in markdown and replace with optimized LaTeX tables

    Args:
        markdown_content: Full markdown document content

    Returns:
        Markdown content with tables replaced by LaTeX tables with optimal widths
    """
    # Regex to match pipe tables (must have header, separator, and at least one row)
    # Look for lines starting with | and containing |
    lines = markdown_content.split('\n')
    result_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if this line starts a pipe table
        if line.strip().startswith('|') and '|' in line:
            # Look ahead for separator line
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                # Check if next line is a separator (contains dashes and pipes)
                if '|' in next_line and any(c in next_line for c in ['-', ':']):
                    # Found a table! Collect all table lines
                    table_lines = [line]
                    j = i + 1

                    # Collect separator and all subsequent table rows
                    while j < len(lines) and lines[j].strip().startswith('|'):
                        table_lines.append(lines[j])
                        j += 1

                    # Parse and optimize the table
                    table_text = '\n'.join(table_lines)
                    headers, data_rows = parse_pipe_table(table_text)

                    if headers and data_rows:
                        # Calculate optimal widths
                        all_rows = [headers] + data_rows
                        widths = calculate_column_widths(all_rows)

                        # Convert to LaTeX
                        latex_table = convert_table_to_latex(headers, data_rows, widths)
                        result_lines.append(latex_table)
                    else:
                        # Failed to parse, keep original
                        result_lines.extend(table_lines)

                    # Skip past the table
                    i = j
                    continue

        # Not a table line, keep as-is
        result_lines.append(line)
        i += 1

    return '\n'.join(result_lines)
