# Page Break Guide

This document explains how to insert page breaks in your Markdown documents for conversion to PDF and DOCX formats.

## Supported Page Break Syntaxes

The converter supports **three different ways** to insert page breaks, giving you flexibility based on your workflow:

### 1. HTML Comments (Recommended for Obsidian) ✅

```markdown
Content on page 1

<!-- pagebreak -->

Content on page 2
```

**Variants supported** (case-insensitive):

- `<!-- pagebreak -->`
- `<!-- page-break -->`
- `<!-- page_break -->`
- `<!-- newpage -->`
- `<!-- PAGEBREAK -->` (any capitalization)

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

### 3. Horizontal Rules ✅

```markdown
Content on page 1

---

Content on page 2
```

**Also supports:**

- `---` (three or more hyphens)
- `***` (three or more asterisks)
- `___` (three or more underscores)

**Pros:**

- Quick to type
- Standard Markdown syntax
- Visual separator in source

**⚠️ Smart Detection:**
The converter is **code-block aware** and will NOT convert horizontal rules inside:

- Fenced code blocks (```)
- YAML frontmatter
- This prevents conflicts with legitimate uses of `---`

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

---

# Conclusion

Final thoughts.
```

### Using in Code Blocks (Safe)

```markdown
Here's some Python code:

```python
def example():
    # This --- won't trigger a page break
    separator = "---"
    return separator
```

<!-- pagebreak -->

Next page content.

```text

### YAML Frontmatter (Safe)

```markdown
---
title: Document Title
date: 2025-12-05
---

The --- above won't trigger a page break!

<!-- pagebreak -->

New page starts here.
```

## Output Formats

| Format | Status | Notes |
|--------|--------|-------|
| **PDF** | ✅ Fully Supported | Uses LaTeX `\newpage` |
| **DOCX** | ✅ Fully Supported | Uses Word page breaks |

Both formats support all three syntax types identically.

## Best Practices

1. **Choose one style and be consistent** - Pick the syntax that works best for your workflow
2. **Use HTML comments in Obsidian** - They're invisible in preview mode
3. **Use `\newpage` for LaTeX documents** - Familiar to academic users
4. **Use `---` for quick drafts** - Fast to type, but be aware it converts ALL horizontal rules

## Migration from Previous Version

If you were using the previous version that converted ALL `---` to page breaks:

- **No changes needed** - It still works the same way
- **But now safer** - Code blocks and YAML frontmatter are protected
- **More options** - You can now use HTML comments or `\newpage` too

## Advanced: Code-Block Detection

The converter tracks:

- Fenced code blocks with ` ``` ` or `~~~`
- YAML frontmatter (only the first `---...---` block at document start)
- Nested structures

This ensures page break detection is **context-aware** and won't interfere with your code examples or metadata.

---

**Questions?** Check the main documentation or raise an issue on GitHub.
