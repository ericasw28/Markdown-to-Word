# Setup Instructions for Option 5 (Hybrid Approach)

## Step 1: Install LaTeX Packages

Run this command in your terminal:

```bash
sudo tlmgr install soul ulem xcolor tcolorbox environ fontawesome5 mdframed
```

**What these packages do:**
- `soul` - Text highlighting (`==highlighted text==`)
- `ulem` - Underlining (`<u>underlined</u>`)
- `xcolor` - Colored text and backgrounds
- `tcolorbox` - Styled boxes for Obsidian callouts
- `environ` - Environment handling (dependency)
- `fontawesome5` - Icons for callouts (optional but nice)
- `mdframed` - Alternative framed boxes

## Step 2: Verify Installation

After installation, verify with:

```bash
kpsewhich soul.sty
```

Should return a path like: `/usr/local/texlive/2025basic/texmf-dist/tex/latex/soul/soul.sty`

## Step 3: Python Environment

Your current `requirements.txt` is good for now:
- streamlit
- markdown
- python-docx
- beautifulsoup4
- pypandoc
- Pillow

Make sure your conda AI_Env has these installed:

```bash
conda activate AI_Env
pip install -r requirements.txt
```

## Next Steps

After LaTeX packages are installed, we'll:
1. Create an Obsidian syntax preprocessor (`helpers/obsidian_preprocessor.py`)
2. Enhance the LaTeX template for better callout styling
3. Test with the Obsidian Formatting.md file
4. Fix any remaining issues

## What We're Solving

- ✅ Missing LaTeX packages (soul.sty error)
- 🔄 Obsidian-specific syntax conversion
- 🔄 Enhanced callout rendering
- 🔄 Extended checkbox support
- ✅ Mermaid diagrams (already working)
- ✅ LaTeX math (already supported by Pandoc)
