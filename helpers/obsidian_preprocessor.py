"""Obsidian-specific Markdown syntax preprocessor

This module converts Obsidian-specific syntax to standard Markdown/LaTeX
that can be properly rendered by Pandoc.
"""

import re
from typing import Tuple, List


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


def preprocess_obsidian_syntax(content: str) -> str:
    """Main preprocessing function that converts all Obsidian syntax

    Args:
        content: Raw markdown content with Obsidian syntax

    Returns:
        Preprocessed markdown content compatible with Pandoc
    """
    # Order matters! Process in this sequence:

    # 0. Fix consecutive bold label lines first
    content = fix_consecutive_bold_lines(content)

    # 1. Convert callouts first (they contain other syntax)
    content = convert_callouts(content)

    # 2. Convert Obsidian-specific links and embeds
    content = convert_obsidian_images(content)
    content = convert_wikilinks(content)

    # 3. Convert extended checkboxes
    content = convert_extended_checkboxes(content)

    # 4. Convert text formatting
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
\usepackage{xcolor}        % For colors
\usepackage{tcolorbox}     % For callout boxes
\usepackage{fontawesome5}  % For icons (if available)
\usepackage{enumitem}      % For better list control
\usepackage{fontspec}      % For font configuration

% Configure fonts with emoji support
\setmainfont{Helvetica Neue}
\newfontfamily\emojifont{Apple Color Emoji}[Renderer=Harfbuzz]
\usepackage{newunicodechar}

% Map emoji unicode ranges to use emoji font
\directlua{
  luaotfload.add_fallback("emojifallback", {
    "Apple Color Emoji:mode=harf"
  })
}
\setmainfont{Helvetica Neue}[RawFeature={fallback=emojifallback}]

% Define custom highlight command using colorbox (replacement for soul's \hl)
\definecolor{highlightyellow}{RGB}{255, 255, 0}
\providecommand{\hl}{}
\renewcommand{\hl}[1]{\colorbox{highlightyellow}{#1}}
'''
    else:
        engine_specific = r'''
% Obsidian formatting support
\usepackage{soul}          % For highlighting
\usepackage{xcolor}        % For colors
\usepackage{tcolorbox}     % For callout boxes
\usepackage{fontawesome5}  % For icons (if available)
\usepackage{enumitem}      % For better list control

% Define highlight color
\sethlcolor{yellow}
'''

    # Common LaTeX code for both engines
    common_header = r'''
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
