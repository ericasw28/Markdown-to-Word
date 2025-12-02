"""Emoji removal for LaTeX compatibility"""

import re


def remove_emojis(text):
    """Remove emoji characters that LaTeX can't handle"""
    # Note: With XeLaTeX, emojis are supported, so we just return the text as-is
    # This function is kept for backwards compatibility
    return text
