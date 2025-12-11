# Page Break Guide

This document explains how to insert page breaks in your Markdown documents for conversion to PDF and DOCX formats.

## Supported Page Break Syntaxes

The converter supports **two different ways** to insert page breaks:

### 1. HTML Comments (Recommended for Obsidian) ✅

```markdown
Content on page 1

<!-- pagebreak -->

Content on page 2
```

**Variants supported** (case-insensitive):

- `<!-- pagebreak -->` (no separator)
- `<!-- page-break -->` (hyphen)
- `<!-- page_break -->` (underscore)
- `<!-- page break -->` (space)
- `<!-- newpage -->`
- `<!-- PAGEBREAK -->` (any capitalization works)

**Pros:**

- Clean and semantic
- Works in Obsidian and most Markdown editors
- Won't appear in preview (invisible in rendered markdown)

### 2. Raw LaTeX ✅

```markdown
Content on page 1

\newpage

Content on page 2
```

**Pros:**

- Standard LaTeX convention
- Familiar to academic users
- Direct and explicit

## Important: Horizontal Rules Are NOT Page Breaks

**⚠️ Note:** Markdown horizontal rules (`---`, `***`, `___`) are rendered as horizontal lines and do NOT create page breaks.

```markdown
Content on page 1

---

This will be on the same page with a horizontal line above it
```

If you need both a visual separator AND a page break, use them together:

```markdown
Content on page 1

---
\newpage

Content on page 2 with horizontal line at the top of the previous page
```

## Examples

### Basic Document with Multiple Page Breaks

```markdown
---
title: My Report
author: John Doe
---

# Introduction

This is the introduction content.

<!-- pagebreak -->

# Chapter 1

First chapter content here.

\newpage

# Chapter 2

Second chapter content.

\newpage

# Conclusion

Final thoughts.
```

### Using Page Breaks with Code Blocks

```markdown
Here's some Python code:

```python
def example():
    # Code blocks are never converted to page breaks
    separator = "---"
    return separator
```

<!-- pagebreak -->

Next page content.
```

### YAML Frontmatter (Safe)

```markdown
---
title: Document Title
date: 2025-12-05
---

The YAML frontmatter above is protected and never converted to page breaks.

\newpage

New page starts here.
```

## Output Formats

| Format | Status | Notes |
|--------|--------|-------|
| **PDF** | ✅ Fully Supported | Uses LaTeX `\newpage` |
| **DOCX** | ✅ Fully Supported | Uses Word page breaks |

Both formats support both syntax types identically.

## Best Practices

1. **Choose one style and be consistent** - Pick the syntax that works best for your workflow
2. **Use HTML comments in Obsidian** - They're invisible in preview mode
3. **Use `\newpage` for LaTeX documents** - Familiar to academic users and explicit
4. **Horizontal rules are for visual separation** - Use `---` for styling, not page breaks

## Important Changes

**Horizontal rules (`---`, `***`, `___`) are NOT converted to page breaks.**

If you have documents that relied on `---` for page breaks, update them to use:
- `\newpage` - LaTeX-style page break
- `<!-- pagebreak -->` - HTML comment-style page break

## Advanced: Code-Block Protection

The converter protects special content from page break conversion:

- Fenced code blocks with ` ``` ` or `~~~`
- YAML frontmatter (the first `---...---` block at document start)

This ensures `\newpage` and `<!-- pagebreak -->` markers inside code blocks are treated as literal text, not page break commands.

---

**Questions?** Check the main documentation or raise an issue on GitHub.
