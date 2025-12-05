"""Obsidian-specific Markdown syntax preprocessor

This module converts Obsidian-specific syntax to standard Markdown/LaTeX
that can be properly rendered by Pandoc.
"""

import re
from typing import Tuple, List
from .table_width_optimizer import optimize_table_widths
from .page_break_handler import convert_page_breaks_to_latex


# Callout type mapping to colors and icons
CALLOUT_STYLES = {
    'note': {'color': 'blue', 'icon': '📝'},
    'abstract': {'color': 'cyan', 'icon': '📋'},
    'summary': {'color': 'cyan', 'icon': '📋'},
    'tldr': {'color': 'cyan', 'icon': '📋'},
    'info': {'color': 'blue', 'icon': 'ℹ️'},
    'todo': {'color': 'blue', 'icon': '☑️'},
    'tip': {'color': 'green', 'icon': '💡'},
    'hint': {'color': 'green', 'icon': '💡'},
    'important': {'color': 'cyan', 'icon': '❗'},
    'success': {'color': 'green', 'icon': '✅'},
    'check': {'color': 'green', 'icon': '✅'},
    'done': {'color': 'green', 'icon': '✅'},
    'question': {'color': 'yellow', 'icon': '❓'},
    'help': {'color': 'yellow', 'icon': '❓'},
    'faq': {'color': 'yellow', 'icon': '❓'},
    'warning': {'color': 'orange', 'icon': '⚠️'},
    'caution': {'color': 'orange', 'icon': '⚠️'},
    'attention': {'color': 'orange', 'icon': '⚠️'},
    'failure': {'color': 'red', 'icon': '❌'},
    'fail': {'color': 'red', 'icon': '❌'},
    'missing': {'color': 'red', 'icon': '❌'},
    'danger': {'color': 'red', 'icon': '⚡'},
    'error': {'color': 'red', 'icon': '⚡'},
    'bug': {'color': 'red', 'icon': '🐛'},
    'example': {'color': 'purple', 'icon': '📝'},
    'quote': {'color': 'gray', 'icon': '💬'},
    'cite': {'color': 'gray', 'icon': '💬'},
}

# Extended checkbox type mapping - using emoji icons only (no text to avoid duplication)
CHECKBOX_TYPES = {
    ' ': ('[ ]', ''),  # Unchecked - no icon
    'x': ('[x]', ''),  # Regular checked - no icon
    'X': ('[x]', ''),  # Checked - no icon

    # Action/Status
    '!': ('[x]', '⚠️'),  # Important
    '/': ('[x]', '🔄'),  # In Progress / Half Done
    'd': ('[x]', '💪'),  # Doing
    '-': ('[x]', '❌'),  # Dropped
    '>': ('[x]', '➡️'),  # Forwarded

    # Planning/Research
    '?': ('[ ]', '❓'),  # Question
    'R': ('[ ]', '🔍'),  # Research
    '+': ('[ ]', '➕'),  # To Add
    'i': ('[ ]', '💡'),  # Idea
    'B': ('[ ]', '🧠'),  # Brainstorm

    # Evaluation
    'P': ('[x]', '✅'),  # Pro
    'C': ('[x]', '❌'),  # Con
    'A': ('[x]', '💬'),  # Answer

    # Documentation
    'N': ('[ ]', '📝'),  # Note
    'Q': ('[ ]', '💬'),  # Quote
    'b': ('[ ]', '🔖'),  # Bookmark
    'I': ('[ ]', 'ℹ️'),  # Information
    'E': ('[ ]', '📋'),  # Example
    'p': ('[ ]', '📖'),  # Paraphrase

    # Temporal
    'D': ('[x]', '📅'),  # Date
    'T': ('[ ]', '⏰'),  # Time

    # Creative Writing
    '@': ('[ ]', '👤'),  # Person / Character
    't': ('[ ]', '💬'),  # Talk / Dialogue
    'O': ('[ ]', '📑'),  # Outline / Plot
    '~': ('[ ]', '⚔️'),  # Conflict
    'W': ('[ ]', '🌍'),  # World / Worldbuilding
    'f': ('[ ]', '🔎'),  # Clue / Find
    'F': ('[ ]', '🔮'),  # Foreshadow
    '&': ('[ ]', '🎭'),  # Symbol / Symbolism
    's': ('[ ]', '🤫'),  # Secret

    # Other
    'L': ('[ ]', '📍'),  # Location
    'r': ('[x]', '🏆'),  # Reward
    'c': ('[ ]', '🔀'),  # Choice
    'H': ('[x]', '❤️'),  # Favorite / Health
}


def convert_highlighting(content: str) -> str:
    """Convert ==highlighted text== to LaTeX highlighting"""
    # Replace ==text== with \hl{text} for LaTeX soul package
    content = re.sub(r'==([^=]+)==', r'\\hl{\1}', content)
    return content


def convert_underline(content: str) -> str:
    """Convert <u>text</u> to LaTeX underline"""
    content = re.sub(r'<u>([^<]+)</u>', r'\\underline{\1}', content)
    return content


def convert_obsidian_images(content: str) -> str:
    """Convert ![[image.png]] to standard markdown ![](image.png)"""
    # Handle images with optional sizing and alignment
    content = re.sub(
        r'!\[\[([^\]|]+?)(?:\|([^\]]+))?\]\]',
        lambda m: f'![]({m.group(1)})',
        content
    )
    return content


def convert_wikilinks(content: str) -> str:
    """Convert [[wikilink]] to plain text or standard links"""
    # Remove section links like [[Note#Section]]
    content = re.sub(r'!\[\[([^\]]+?)#([^\]]+?)\]\]', r'', content)

    # Convert regular wikilinks to plain text
    # (could be enhanced to actual links if we had a mapping)
    content = re.sub(r'\[\[([^\]|]+?)(?:\|([^\]]+))?\]\]', r'\2' if r'\2' else r'\1', content)
    return content


def convert_extended_checkboxes(content: str) -> str:
    """Convert Obsidian extended checkboxes to standard checkboxes with text labels"""
    lines = content.split('\n')
    converted_lines = []

    for line in lines:
        # Match extended checkbox patterns: - [X] text
        match = re.match(r'^(\s*)- \[(.)\] (.+)$', line)
        if match:
            indent, checkbox_type, text = match.groups()
            checkbox_info = CHECKBOX_TYPES.get(checkbox_type, ('[ ]', ''))

            if isinstance(checkbox_info, tuple):
                checkbox_symbol, label = checkbox_info
            else:
                # Fallback for old format
                checkbox_symbol = '[ ]'
                label = ''

            # For standard checkboxes, keep them as-is
            if checkbox_type in [' ', 'x', 'X']:
                converted_lines.append(line)
            else:
                # Convert to standard checkbox with text label
                if label:
                    converted_lines.append(f'{indent}- {checkbox_symbol} {label} {text}')
                else:
                    converted_lines.append(f'{indent}- {checkbox_symbol} {text}')
        else:
            converted_lines.append(line)

    return '\n'.join(converted_lines)


def convert_callouts(content: str) -> str:
    """Convert Obsidian callouts to formatted blockquotes

    Converts:
        > [!note] Title
        > Content

    To a LaTeX-friendly format with styling
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
                converted_lines.extend(_format_callout(callout_type, callout_title, callout_content))
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
                converted_lines.extend(_format_callout(callout_type, callout_title, callout_content))
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
        converted_lines.extend(_format_callout(callout_type, callout_title, callout_content))

    return '\n'.join(converted_lines)


def _format_callout(callout_type: str, title: str, content: List[str]) -> List[str]:
    """Format a callout as a colored tcolorbox using raw LaTeX

    This outputs raw LaTeX that Pandoc will pass through directly to the PDF.
    """
    # Map callout type to LaTeX environment name
    type_to_env = {
        'note': 'calloutNote',
        'info': 'calloutInfo',
        'todo': 'calloutTodo',
        'tip': 'calloutTip',
        'hint': 'calloutTip',  # Use Tip style
        'success': 'calloutSuccess',
        'check': 'calloutSuccess',  # Use Success style
        'done': 'calloutSuccess',  # Use Success style
        'question': 'calloutQuestion',
        'help': 'calloutQuestion',  # Use Question style
        'faq': 'calloutQuestion',  # Use Question style
        'warning': 'calloutWarning',
        'caution': 'calloutWarning',  # Use Warning style
        'attention': 'calloutWarning',  # Use Warning style
        'danger': 'calloutDanger',
        'error': 'calloutError',
        'failure': 'calloutError',  # Use Error style
        'fail': 'calloutError',  # Use Error style
        'missing': 'calloutError',  # Use Error style
        'bug': 'calloutBug',
        'example': 'calloutExample',
        'quote': 'calloutNote',  # Use Note style for quotes
        'cite': 'calloutNote',  # Use Note style for citations
        'abstract': 'calloutInfo',  # Use Info style
        'summary': 'calloutInfo',  # Use Info style
        'tldr': 'calloutInfo',  # Use Info style
        'important': 'calloutWarning',  # Use Warning style
    }

    env_name = type_to_env.get(callout_type.lower(), 'calloutNote')

    # Clean up the title - remove the callout type if it's redundant
    clean_title = title.strip()
    if clean_title.lower() == callout_type.lower():
        clean_title = ''

    # Join content lines, preserving paragraph breaks
    content_text = '\n'.join(content).strip()

    # Create raw LaTeX block that Pandoc will pass through
    # Using ````{=latex} syntax for raw LaTeX blocks in Pandoc
    result = [
        '',
        '```{=latex}',
        f'\\begin{{{env_name}}}{{{clean_title}}}',
        content_text,
        f'\\end{{{env_name}}}',
        '```',
        ''
    ]

    return result


def fix_consecutive_bold_lines(content: str) -> str:
    """Add line breaks between consecutive bold label lines

    Fixes issue where lines like:
    **Label:** text
    **Label:** text

    Run together in PDF output. Adds explicit line breaks.
    """
    lines = content.split('\n')
    result = []
    prev_was_bold_label = False

    for line in lines:
        # Check if line starts with **text:** pattern (bold label)
        is_bold_label = re.match(r'^\*\*.+:\*\*\s+', line)

        if is_bold_label and prev_was_bold_label:
            # Add explicit line break before this line
            result.append('\\')

        result.append(line)
        prev_was_bold_label = bool(is_bold_label)

    return '\n'.join(result)


def fix_list_blank_lines(content: str) -> str:
    """Ensure blank lines before bullet/numbered lists for proper Pandoc parsing

    Pandoc requires blank lines before lists to recognize them as list environments.
    This function automatically adds missing blank lines.

    Args:
        content: Markdown content

    Returns:
        Content with blank lines added before lists where needed
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


# Page break conversion is now handled by shared page_break_handler module
# This function is kept for backward compatibility
def convert_page_break_markers(content: str) -> str:
    """Convert page break markers to LaTeX page breaks

    NOTE: This function now delegates to the shared page_break_handler module
    for consistent behavior across PDF and DOCX converters.

    Supports multiple page break syntaxes:
    1. HTML comments: <!-- pagebreak -->, <!-- page-break -->, <!-- newpage -->
    2. Raw LaTeX: \newpage (already supported by Pandoc, but normalized here)
    3. Horizontal rules: --- (only when NOT in code blocks or YAML frontmatter)

    This function is code-block aware and won't convert markers inside:
    - Fenced code blocks (```)
    - YAML frontmatter

    Args:
        content: Markdown content

    Returns:
        Content with page break markers converted to \newpage
    """
    return convert_page_breaks_to_latex(content)


def wrap_code_block_lines(content: str, max_width: int = 100) -> str:
    """Wrap long lines in code blocks to prevent PDF overflow.

    This preprocesses markdown content to wrap lines in code blocks that exceed
    max_width characters. Lines are wrapped at spaces to avoid breaking mid-word.

    Args:
        content: Markdown content with code blocks
        max_width: Maximum line width in characters (default 100)

    Returns:
        Markdown content with wrapped code block lines
    """
    import textwrap

    lines = content.split('\n')
    result = []
    in_code_block = False
    code_fence = ''

    for line in lines:
        # Check for code block fences (``` or ~~~)
        if line.strip().startswith('```') or line.strip().startswith('~~~'):
            if not in_code_block:
                # Starting a code block
                in_code_block = True
                code_fence = line.strip()[:3]
            else:
                # Ending a code block
                in_code_block = False
                code_fence = ''
            result.append(line)
            continue

        # If we're in a code block and the line is too long, wrap it
        if in_code_block and len(line) > max_width:
            # Preserve leading whitespace
            leading_space = len(line) - len(line.lstrip())
            indent = line[:leading_space]
            content_part = line[leading_space:]

            # Wrap the content part
            # Use break_long_words=False to avoid breaking in the middle of words
            # Use break_on_hyphens=False to keep hyphenated words together
            wrapped = textwrap.wrap(
                content_part,
                width=max_width - leading_space,
                break_long_words=False,
                break_on_hyphens=False,
                replace_whitespace=False,
                drop_whitespace=False
            )

            # If wrapping produced multiple lines, add them with original indentation
            if wrapped:
                for wrapped_line in wrapped:
                    result.append(indent + wrapped_line)
            else:
                # If wrapping failed (e.g., single word longer than max_width), keep original
                result.append(line)
        else:
            # Not in code block or line is short enough
            result.append(line)

    return '\n'.join(result)


def preprocess_obsidian_syntax(content: str) -> str:
    """Main preprocessing function that converts all Obsidian syntax

    Args:
        content: Raw markdown content with Obsidian syntax

    Returns:
        Preprocessed markdown content compatible with Pandoc
    """
    # Order matters! Process in this sequence:

    # 0. Optimize table column widths (do this first, before other processing)
    content = optimize_table_widths(content)

    # 1. Wrap long lines in code blocks to prevent PDF overflow
    content = wrap_code_block_lines(content)

    # 2. Convert page break markers (HTML comments, \newpage, ---) to \newpage
    # Do this early but after code block wrapping to preserve code block tracking
    content = convert_page_break_markers(content)

    # 3. Fix consecutive bold label lines first
    content = fix_consecutive_bold_lines(content)

    # 4. Fix missing blank lines before lists (for proper Pandoc parsing)
    content = fix_list_blank_lines(content)

    # 5. Convert callouts (they contain other syntax)
    content = convert_callouts(content)

    # 6. Convert Obsidian-specific links and embeds
    content = convert_obsidian_images(content)
    content = convert_wikilinks(content)

    # 7. Convert extended checkboxes
    content = convert_extended_checkboxes(content)

    # 8. Convert text formatting
    content = convert_highlighting(content)
    content = convert_underline(content)

    return content


def get_enhanced_latex_header(use_lualatex=False) -> str:
    """Generate enhanced LaTeX header for better Obsidian feature support

    Args:
        use_lualatex: If True, generate LuaLaTeX-compatible header (avoids soul package)

    Returns:
        LaTeX header content as string
    """
    # Engine-specific packages
    if use_lualatex:
        engine_specific = r'''
% Obsidian formatting support for LuaLaTeX
\usepackage{etoolbox}      % For code hooks
\usepackage{xcolor}        % For colors
\usepackage{tcolorbox}     % For callout boxes
\usepackage{fontawesome5}  % For icons (if available)
\usepackage{enumitem}      % For better list control
\usepackage{fontspec}      % For font configuration
\usepackage{ulem}          % For underline support

% Configure fallback font for emoji support
\directlua{
  luaotfload.add_fallback("emojifallback", {
    "Apple Color Emoji:mode=harf"
  })
}

% Set main font with emoji fallback
\setmainfont{Helvetica Neue}[RawFeature={fallback=emojifallback}]

% Use default monospace font for better line breaking in code blocks
% Custom fonts can interfere with fvextra's character width calculations
\setmonofont{Latin Modern Mono}[Scale=0.9]

% Define custom highlight command using colorbox (replacement for soul's \hl)
\definecolor{highlightyellow}{RGB}{255, 255, 0}
\providecommand{\hl}{}
\renewcommand{\hl}[1]{\colorbox{highlightyellow}{#1}}
'''
    else:
        engine_specific = r'''
% Obsidian formatting support
\usepackage{etoolbox}      % For code hooks
\usepackage{soul}          % For highlighting
\usepackage{xcolor}        % For colors
\usepackage{tcolorbox}     % For callout boxes
\usepackage{fontawesome5}  % For icons (if available)
\usepackage{enumitem}      % For better list control
\usepackage{ulem}          % For underline support

% Define highlight color
\sethlcolor{yellow}
'''

    # Common LaTeX code for both engines
    common_header = r'''
% Enable professional typography and reasonable text wrapping
\usepackage{microtype}
\usepackage{parskip}

% Moderate line breaking settings (code blocks are pre-wrapped during preprocessing)
\setlength{\emergencystretch}{3em}
\tolerance=2000
\hbadness=2000

% Note: Code blocks are automatically wrapped during preprocessing at ~100 characters
% so aggressive LaTeX line breaking is not needed and would break table formatting

% Code block styling with light gray background (using framed package like quotes)
\definecolor{codebg}{gray}{0.95}

% Redefine verbatim to add gray background
\let\oldverbatim\verbatim
\let\endoldverbatim\endverbatim
\renewenvironment{verbatim}{%
  \def\FrameCommand{%
    \fboxsep=8pt\colorbox{codebg}%
  }%
  \MakeFramed{\advance\hsize-\width\FrameRestore}%
  \oldverbatim
}{%
  \endoldverbatim
  \endMakeFramed
}

% Redefine Highlighting (syntax-highlighted code) to add gray background if it exists
\AtBeginDocument{%
  \ifcsname Highlighting\endcsname
    \let\oldHighlighting\Highlighting
    \let\endoldHighlighting\endHighlighting
    \renewenvironment{Highlighting}{%
      \def\FrameCommand{%
        \fboxsep=8pt\colorbox{codebg}%
      }%
      \MakeFramed{\advance\hsize-\width\FrameRestore}%
      \oldHighlighting
    }{%
      \endoldHighlighting
      \endMakeFramed
    }%
  \fi
}

% Enhanced table support with smart column widths
\usepackage{booktabs}       % Professional table styling
\usepackage{tabularx}       % Smart column width distribution
\usepackage{array}          % Enhanced column formatting
\usepackage{longtable}      % Multi-page tables

% Configure longtable to use content-based column widths
% LTleft and LTright control horizontal positioning
\setlength{\LTleft}{0pt}
\setlength{\LTright}{0pt}

% Allow tables to use full text width
\setlength{\tabcolsep}{6pt}

% Configure blockquote styling
\usepackage{xcolor}
\usepackage{framed}
\definecolor{quotebg}{gray}{0.95}
\definecolor{quotebar}{gray}{0.4}

\renewenvironment{quote}{%
  \def\FrameCommand{%
    {\color{quotebar}\vrule width 3pt}%
    \hspace{10pt}%
    \fboxsep=10pt\colorbox{quotebg}%
  }%
  \MakeFramed{\advance\hsize-\width\FrameRestore}%
  \itshape
}{%
  \endMakeFramed
}

% Fix "too deeply nested" error by increasing list nesting depth
\setlistdepth{9}
\renewlist{itemize}{itemize}{9}
\renewlist{enumerate}{enumerate}{9}

% Configure list appearance for all levels
\setlist[itemize,1]{label=$\bullet$}
\setlist[itemize,2]{label=$\circ$}
\setlist[itemize,3]{label=$\ast$}
\setlist[itemize,4]{label=$\cdot$}
\setlist[itemize,5]{label=$\diamond$}
\setlist[itemize,6]{label=$\triangleright$}
\setlist[itemize,7]{label=$\star$}
\setlist[itemize,8]{label=$\dagger$}
\setlist[itemize,9]{label=$\bullet$}

% Configure figure placement
\usepackage{float}
\let\origfigure\figure
\let\endorigfigure\endfigure
\renewenvironment{figure}[1][]{\origfigure[H]}{\endorigfigure}

% Define Obsidian-style callout colors
\definecolor{calloutblue}{RGB}{8, 109, 221}
\definecolor{calloutcyan}{RGB}{0, 191, 188}
\definecolor{calloutgreen}{RGB}{8, 185, 78}
\definecolor{calloutyellow}{RGB}{224, 175, 104}
\definecolor{calloutorange}{RGB}{233, 151, 63}
\definecolor{calloutred}{RGB}{233, 68, 83}
\definecolor{calloutpurple}{RGB}{168, 101, 221}
\definecolor{calloutgray}{RGB}{120, 120, 120}

% Define individual callout environments with proper styling
\newtcolorbox{calloutNote}[1]{
    colback=calloutblue!5!white,
    colframe=calloutblue!75!black,
    fonttitle=\bfseries,
    title={NOTE: #1},
    arc=2mm,
    boxrule=1pt,
    left=3mm,
    right=3mm,
    top=2mm,
    bottom=2mm
}

\newtcolorbox{calloutInfo}[1]{
    colback=calloutblue!5!white,
    colframe=calloutblue!75!black,
    fonttitle=\bfseries,
    title={INFO: #1},
    arc=2mm,
    boxrule=1pt,
    left=3mm,
    right=3mm,
    top=2mm,
    bottom=2mm
}

\newtcolorbox{calloutTodo}[1]{
    colback=calloutblue!5!white,
    colframe=calloutblue!75!black,
    fonttitle=\bfseries,
    title={TODO: #1},
    arc=2mm,
    boxrule=1pt,
    left=3mm,
    right=3mm,
    top=2mm,
    bottom=2mm
}

\newtcolorbox{calloutTip}[1]{
    colback=calloutgreen!5!white,
    colframe=calloutgreen!75!black,
    fonttitle=\bfseries,
    title={TIP: #1},
    arc=2mm,
    boxrule=1pt,
    left=3mm,
    right=3mm,
    top=2mm,
    bottom=2mm
}

\newtcolorbox{calloutSuccess}[1]{
    colback=calloutgreen!5!white,
    colframe=calloutgreen!75!black,
    fonttitle=\bfseries,
    title={SUCCESS: #1},
    arc=2mm,
    boxrule=1pt,
    left=3mm,
    right=3mm,
    top=2mm,
    bottom=2mm
}

\newtcolorbox{calloutQuestion}[1]{
    colback=calloutyellow!5!white,
    colframe=calloutyellow!75!black,
    fonttitle=\bfseries,
    title={QUESTION: #1},
    arc=2mm,
    boxrule=1pt,
    left=3mm,
    right=3mm,
    top=2mm,
    bottom=2mm
}

\newtcolorbox{calloutWarning}[1]{
    colback=calloutorange!5!white,
    colframe=calloutorange!75!black,
    fonttitle=\bfseries,
    title={WARNING: #1},
    arc=2mm,
    boxrule=1pt,
    left=3mm,
    right=3mm,
    top=2mm,
    bottom=2mm
}

\newtcolorbox{calloutDanger}[1]{
    colback=calloutred!5!white,
    colframe=calloutred!75!black,
    fonttitle=\bfseries,
    title={DANGER: #1},
    arc=2mm,
    boxrule=1pt,
    left=3mm,
    right=3mm,
    top=2mm,
    bottom=2mm
}

\newtcolorbox{calloutError}[1]{
    colback=calloutred!5!white,
    colframe=calloutred!75!black,
    fonttitle=\bfseries,
    title={ERROR: #1},
    arc=2mm,
    boxrule=1pt,
    left=3mm,
    right=3mm,
    top=2mm,
    bottom=2mm
}

\newtcolorbox{calloutBug}[1]{
    colback=calloutred!5!white,
    colframe=calloutred!75!black,
    fonttitle=\bfseries,
    title={BUG: #1},
    arc=2mm,
    boxrule=1pt,
    left=3mm,
    right=3mm,
    top=2mm,
    bottom=2mm
}

\newtcolorbox{calloutExample}[1]{
    colback=calloutpurple!5!white,
    colframe=calloutpurple!75!black,
    fonttitle=\bfseries,
    title={EXAMPLE: #1},
    arc=2mm,
    boxrule=1pt,
    left=3mm,
    right=3mm,
    top=2mm,
    bottom=2mm
}
'''

    return engine_specific + common_header
