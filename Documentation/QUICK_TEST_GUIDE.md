---
up: "[[Dev/20 - Garage/64 - Streamlit/Markdown to Word/Markdown to Word|Markdown to Word]]"  # hub
---
# Quick Test Guide

## Test the Streamlit App

1. **Start the app:**
   ```bash
   cd "/Users/ErictTaylor/Dev/Streamlit/Markdown to Word"
   streamlit run app.py
   ```

2. **Upload a test file:**
   - Use `test_simple.md` (recommended - works perfectly)
   - Or use any Obsidian markdown file

3. **Select PDF format**

4. **Click Convert**

5. **Download and verify:**
   - Check that highlighting works (==text==)
   - Check that callouts are styled
   - Check that checkboxes show emojis
   - Check that math renders correctly

## What You Should See

### ✅ Success Indicators:
- No errors about missing LaTeX packages
- PDF generates successfully
- Download button appears
- File size is reasonable (30-50KB for simple docs)

### ⚠️ Expected Warnings:
- Missing emoji characters in font (normal - not an error)
- Missing images if they're not in the directory (won't stop conversion)

## Files to Test With

### Recommended:
- ✅ `test_simple.md` - Clean, works perfectly

### Advanced:
- ⚠️ `Obsidian Formatting.md` - Has some broken example code on lines 229-232
  - Will fail at "Missing $ inserted" error
  - This is due to malformed LaTeX example code in the source

## Quick Fix for Obsidian Formatting.md

If you want to test the full file, temporarily comment out the problematic lines:

```markdown
## Latex Math
<!--
This code with double $
	\begin{vmatrix}
	a & b\\ c & d \
	end{vmatrix}=ad-bc
-->
Will generate:
$$ \begin{vmatrix}
a & b\\ c & d
\end{vmatrix}
=ad-bc $$
```

Or wrap them in a proper code block:
````markdown
## Latex Math

Example code:
```latex
\begin{vmatrix}
a & b\\ c & d
\end{vmatrix}=ad-bc
```

Will generate:
$$ \begin{vmatrix}
a & b\\ c & d
\end{vmatrix}
=ad-bc $$
````

## Troubleshooting

### "Module not found" errors:
```bash
conda activate AI_Env
pip install -r requirements.txt
```

### "soul.sty not found":
```bash
sudo tlmgr install soul ulem xcolor tcolorbox environ fontawesome5 mdframed enumitem
```

### App won't start:
```bash
# Make sure you're in the right directory
cd "/Users/ErictTaylor/Dev/Streamlit/Markdown to Word"

# Make sure conda env is activated
conda activate AI_Env

# Check streamlit is installed
streamlit --version
```

## Success! 🎉

If you can convert `test_simple.md` to PDF successfully through the Streamlit app, then **Option 5 is fully working**!

All Obsidian features are now supported:
- Highlighting
- Underline
- Extended checkboxes
- Callouts
- Deep nesting
- Math
- Mermaid
- And more!

<!-- hub-related:start -->
⬆ [Markdown to Word](../Markdown%20to%20Word.md)

## Voir aussi

_Liens générés par `hub-related` (GLaDOS), entre ces balises._

- [Markdown to Word – Fiche projet](../../Markdown%20to%20Word%20%E2%80%93%20Fiche%20projet.md) — Fiche projet du même convertisseur Markdown/Word/PDF.
<!-- hub-related:end -->
