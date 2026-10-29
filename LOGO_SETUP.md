---
up: "[[Dev/20 - Garage/64 - Streamlit/Markdown to Word/Markdown to Word|Markdown to Word]]"  # hub
---
# Logo Setup Instructions

## Issue: SVG Logos Not Supported in LaTeX

LaTeX (which Pandoc uses for PDF generation) doesn't support SVG images natively. Your logo needs to be in PNG, JPG, or PDF format.

## Quick Fix

Convert your `config/logo.svg` to PNG format:

### Option 1: Online Conversion
1. Go to https://cloudconvert.com/svg-to-png
2. Upload `config/logo.svg`
3. Download as `logo.png`
4. Save to `config/logo.png`

### Option 2: Using Inkscape (if installed)
```bash
inkscape config/logo.svg --export-type=png --export-filename=config/logo.png --export-width=400
```

### Option 3: Using ImageMagick (if installed)
```bash
convert -density 300 config/logo.svg -resize 400x config/logo.png
```

### Option 4: Using macOS Preview
1. Open `config/logo.svg` in Preview
2. File → Export
3. Format: PNG
4. Save as `config/logo.png`

## Automatic Detection

The system now automatically:
- Checks if logo is SVG
- Looks for a PNG version with same name (`logo.png`)
- Uses PNG version if found
- Shows warning if only SVG exists

## Update Config

Optionally update [config/header_footer_template.json](config/header_footer_template.json) to reference PNG directly:

```json
"logo": {
  "enabled": true,
  "path": "config/logo.png",
  "position": "header_left",
  "height": "0.8cm",
  "width": ""
}
```

Once you have `config/logo.png`, the logo will appear in your PDFs automatically!

<!-- hub-related:start -->
⬆ [Markdown to Word](Markdown%20to%20Word.md)

## Voir aussi

_Liens générés par `hub-related` (GLaDOS), entre ces balises._

- [EMOJI_NOTES](Documentation/EMOJI_NOTES.md) — Même projet : limitations LaTeX/PDF liées à la génération.
- [SETUP_INSTRUCTIONS](Documentation/SETUP_INSTRUCTIONS.md) — Même projet : installation LaTeX nécessaire pour PDF.
- [IMPLEMENTATION_SUMMARY](Documentation/IMPLEMENTATION_SUMMARY.md) — Même projet : résumé de conversion Markdown vers PDF.
<!-- hub-related:end -->
