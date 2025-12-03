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

    # Calculate actual widths in terms of textwidth
    col_specs = []
    for width in widths:
        # Use p{width} for paragraph columns with specified width
        col_specs.append(f'p{{{width:.3f}\\textwidth}}')

    col_spec_str = '|'.join(col_specs)

    # Build LaTeX table
    latex_lines = [
        '',
        '```{=latex}',
        '\\begin{longtable}[]{@{}' + col_spec_str + '@{}}',
        '\\toprule',
    ]

    # Add header row
    header_str = ' & '.join(headers) + ' \\\\'
    latex_lines.append(header_str)
    latex_lines.append('\\midrule')
    latex_lines.append('\\endhead')

    # Add data rows
    for row in rows:
        row_str = ' & '.join(row) + ' \\\\'
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
