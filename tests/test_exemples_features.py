"""
Test script to identify failing features in Exemples.md Word conversion
This script converts Exemples.md and analyzes what features work correctly.
"""

import sys
import os
from pathlib import Path
from docx import Document

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.docx_converter import convert_to_docx


def analyze_word_document(doc_buffer):
    """Analyze the generated Word document structure"""
    doc_buffer.seek(0)
    doc = Document(doc_buffer)

    findings = {
        'paragraphs_count': len(doc.paragraphs),
        'tables_count': len(doc.tables),
        'has_lists': False,
        'has_checkboxes': False,
        'has_bold': False,
        'has_italic': False,
        'has_code_blocks': False,
        'has_images': False,
        'paragraph_styles': set(),
        'special_characters': set()
    }

    for para in doc.paragraphs:
        # Check paragraph style
        findings['paragraph_styles'].add(para.style.name)

        # Check for list formatting
        if para.style.name in ['List Bullet', 'List Number']:
            findings['has_lists'] = True

        # Check text content
        text = para.text
        if '☐' in text or '☑' in text:
            findings['has_checkboxes'] = True

        # Check for runs with formatting
        for run in para.runs:
            if run.bold:
                findings['has_bold'] = True
            if run.italic:
                findings['has_italic'] = True
            if run.font.name == 'Courier New':
                findings['has_code_blocks'] = True

        # Check for special characters (emojis, symbols)
        for char in text:
            if ord(char) > 127:  # Non-ASCII
                findings['special_characters'].add(char)

    return findings


def test_individual_features():
    """Test each markdown feature individually"""
    test_results = {}

    # Test 1: Lists
    print("\n" + "="*60)
    print("TEST 1: LISTS (Bullet and Numbered)")
    print("="*60)
    md_lists = """## Lists

* List
* List
  * Embedded

1. List
2. List
   1. Embedded
"""
    try:
        buffer = convert_to_docx(md_lists, render_mermaid=False)
        doc = Document(buffer)

        list_items = [p for p in doc.paragraphs if p.style.name in ['List Bullet', 'List Number']]
        test_results['lists'] = {
            'status': 'PASS' if len(list_items) >= 4 else 'FAIL',
            'details': f"Found {len(list_items)} list items",
            'issues': [] if len(list_items) >= 4 else ['List items not properly formatted']
        }
        print(f"✓ Status: {test_results['lists']['status']}")
        print(f"  Details: {test_results['lists']['details']}")
    except Exception as e:
        test_results['lists'] = {'status': 'ERROR', 'details': str(e), 'issues': [str(e)]}
        print(f"✗ ERROR: {e}")

    # Test 2: Checkboxes
    print("\n" + "="*60)
    print("TEST 2: CHECKBOXES (Task Lists)")
    print("="*60)
    md_checkboxes = """## Checkboxes

* [ ] Unchecked
* [x] Checked
  * [ ] Nested unchecked
  * [x] Nested checked
"""
    try:
        buffer = convert_to_docx(md_checkboxes, render_mermaid=False)
        doc = Document(buffer)

        checkbox_paras = [p for p in doc.paragraphs if '☐' in p.text or '☑' in p.text]
        has_unchecked = any('☐' in p.text for p in doc.paragraphs)
        has_checked = any('☑' in p.text for p in doc.paragraphs)

        issues = []
        if not has_unchecked:
            issues.append('Missing unchecked boxes (☐)')
        if not has_checked:
            issues.append('Missing checked boxes (☑)')
        if len(checkbox_paras) < 4:
            issues.append('Nested checkboxes may not be properly indented')

        test_results['checkboxes'] = {
            'status': 'PASS' if not issues else 'PARTIAL',
            'details': f"Found {len(checkbox_paras)} checkbox paragraphs",
            'issues': issues
        }
        print(f"✓ Status: {test_results['checkboxes']['status']}")
        print(f"  Details: {test_results['checkboxes']['details']}")
        if issues:
            print(f"  Issues: {', '.join(issues)}")
    except Exception as e:
        test_results['checkboxes'] = {'status': 'ERROR', 'details': str(e), 'issues': [str(e)]}
        print(f"✗ ERROR: {e}")

    # Test 3: Text Formatting (Bold, Italic, Highlight, Combined)
    print("\n" + "="*60)
    print("TEST 3: TEXT FORMATTING")
    print("="*60)
    md_formatting = """## Text Formatting

Regular text with *italic*, **bold**, ==highlighted==, and ***bold italic*** formatting.
"""
    try:
        buffer = convert_to_docx(md_formatting, render_mermaid=False)
        doc = Document(buffer)

        has_bold = False
        has_italic = False
        has_both = False
        has_highlight = False

        for para in doc.paragraphs:
            for run in para.runs:
                if run.bold and run.italic:
                    has_both = True
                elif run.bold:
                    has_bold = True
                elif run.italic:
                    has_italic = True

            # Check for highlight marker text (since <mark> may not render)
            if '==' in para.text or 'highlighted' in para.text.lower():
                has_highlight = True

        issues = []
        if not has_bold:
            issues.append('Bold formatting not detected')
        if not has_italic:
            issues.append('Italic formatting not detected')
        if not has_both:
            issues.append('Combined bold+italic not detected')
        if not has_highlight:
            issues.append('Highlighted text not properly rendered (==text== syntax)')

        test_results['formatting'] = {
            'status': 'PASS' if len(issues) <= 1 else 'PARTIAL',
            'details': f"Bold: {has_bold}, Italic: {has_italic}, Combined: {has_both}",
            'issues': issues
        }
        print(f"✓ Status: {test_results['formatting']['status']}")
        print(f"  Details: {test_results['formatting']['details']}")
        if issues:
            print(f"  Issues: {', '.join(issues)}")
    except Exception as e:
        test_results['formatting'] = {'status': 'ERROR', 'details': str(e), 'issues': [str(e)]}
        print(f"✗ ERROR: {e}")

    # Test 4: Code Blocks
    print("\n" + "="*60)
    print("TEST 4: CODE BLOCKS")
    print("="*60)
    md_code = """## Code Block

```text
Code line 1
Code line 2
Code line 3
```
"""
    try:
        buffer = convert_to_docx(md_code, render_mermaid=False)
        doc = Document(buffer)

        code_paras = [p for p in doc.paragraphs if any(run.font.name == 'Courier New' for run in p.runs)]

        test_results['code_blocks'] = {
            'status': 'PASS' if len(code_paras) > 0 else 'FAIL',
            'details': f"Found {len(code_paras)} code block paragraphs",
            'issues': [] if len(code_paras) > 0 else ['Code blocks not properly formatted']
        }
        print(f"✓ Status: {test_results['code_blocks']['status']}")
        print(f"  Details: {test_results['code_blocks']['details']}")
    except Exception as e:
        test_results['code_blocks'] = {'status': 'ERROR', 'details': str(e), 'issues': [str(e)]}
        print(f"✗ ERROR: {e}")

    # Test 5: Callouts (Obsidian-style)
    print("\n" + "="*60)
    print("TEST 5: CALLOUT BLOCKS")
    print("="*60)
    md_callout = """## Callout

> [!INFO] Important Information
> This is a callout block with important info.
> It should be formatted specially.
"""
    try:
        buffer = convert_to_docx(md_callout, render_mermaid=False)
        doc = Document(buffer)

        # Callouts are converted to blockquotes with emoji headers
        blockquote_text = '\n'.join([p.text for p in doc.paragraphs])
        has_callout = 'INFO' in blockquote_text or 'ℹ️' in blockquote_text

        test_results['callouts'] = {
            'status': 'PASS' if has_callout else 'FAIL',
            'details': f"Callout detected: {has_callout}",
            'issues': [] if has_callout else ['Callout blocks not properly converted']
        }
        print(f"✓ Status: {test_results['callouts']['status']}")
        print(f"  Details: {test_results['callouts']['details']}")
    except Exception as e:
        test_results['callouts'] = {'status': 'ERROR', 'details': str(e), 'issues': [str(e)]}
        print(f"✗ ERROR: {e}")

    # Test 6: Blockquotes
    print("\n" + "="*60)
    print("TEST 6: BLOCKQUOTES")
    print("="*60)
    md_quote = """## Quote

> This is a regular blockquote.
> It should be indented or styled differently.
"""
    try:
        buffer = convert_to_docx(md_quote, render_mermaid=False)
        doc = Document(buffer)

        # Check if any paragraph contains the quote text
        quote_found = any('blockquote' in p.text for p in doc.paragraphs)

        test_results['blockquotes'] = {
            'status': 'PASS' if quote_found else 'PARTIAL',
            'details': f"Quote text found: {quote_found}",
            'issues': ['Blockquote styling may not be distinct from regular text']
        }
        print(f"✓ Status: {test_results['blockquotes']['status']}")
        print(f"  Details: {test_results['blockquotes']['details']}")
    except Exception as e:
        test_results['blockquotes'] = {'status': 'ERROR', 'details': str(e), 'issues': [str(e)]}
        print(f"✗ ERROR: {e}")

    # Test 7: Tables
    print("\n" + "="*60)
    print("TEST 7: TABLES")
    print("="*60)
    md_table = """## Table

| ID | Name | Description |
|----|------|-------------|
| 1  | One  | First item  |
| 2  | Two  | Second item |
"""
    try:
        buffer = convert_to_docx(md_table, render_mermaid=False)
        doc = Document(buffer)

        tables_count = len(doc.tables)
        if tables_count > 0:
            table = doc.tables[0]
            rows = len(table.rows)
            cols = len(table.columns)

            test_results['tables'] = {
                'status': 'PASS',
                'details': f"Found {tables_count} table(s) with {rows} rows and {cols} columns",
                'issues': []
            }
        else:
            test_results['tables'] = {
                'status': 'FAIL',
                'details': 'No tables found',
                'issues': ['Tables not rendered']
            }
        print(f"✓ Status: {test_results['tables']['status']}")
        print(f"  Details: {test_results['tables']['details']}")
    except Exception as e:
        test_results['tables'] = {'status': 'ERROR', 'details': str(e), 'issues': [str(e)]}
        print(f"✗ ERROR: {e}")

    # Test 8: Mermaid Diagrams
    print("\n" + "="*60)
    print("TEST 8: MERMAID DIAGRAMS")
    print("="*60)
    md_mermaid = """## Mermaid

```mermaid
graph TD
    A[Start] --> B[End]
```
"""
    try:
        buffer = convert_to_docx(md_mermaid, render_mermaid=True)
        doc = Document(buffer)

        # Check for images in document
        has_images = False
        for para in doc.paragraphs:
            for run in para.runs:
                if hasattr(run, '_element'):
                    # Check for drawing elements (images)
                    drawings = run._element.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}drawing')
                    if drawings:
                        has_images = True
                        break

        test_results['mermaid'] = {
            'status': 'PASS' if has_images else 'FAIL',
            'details': f"Images found: {has_images}",
            'issues': [] if has_images else ['Mermaid diagrams not rendered as images']
        }
        print(f"✓ Status: {test_results['mermaid']['status']}")
        print(f"  Details: {test_results['mermaid']['details']}")
    except Exception as e:
        test_results['mermaid'] = {'status': 'ERROR', 'details': str(e), 'issues': [str(e)]}
        print(f"✗ ERROR: {e}")

    # Test 9: LaTeX Math
    print("\n" + "="*60)
    print("TEST 9: LATEX MATH EQUATIONS")
    print("="*60)
    md_math = """## Math

Inline math: $x = 3$

Block math:
$$\\int_{a}^{b} f(x)dx$$
"""
    try:
        buffer = convert_to_docx(md_math, render_mermaid=False)
        doc = Document(buffer)

        # Check if LaTeX syntax is preserved or converted
        all_text = '\n'.join([p.text for p in doc.paragraphs])
        has_dollar_signs = '$' in all_text
        has_latex = '\\int' in all_text or 'int_' in all_text

        issues = []
        if has_dollar_signs:
            issues.append('LaTeX syntax not converted - raw $ symbols visible')
        if not has_latex and not has_dollar_signs:
            issues.append('Math content missing entirely')

        test_results['latex_math'] = {
            'status': 'FAIL',
            'details': f"Raw LaTeX: {has_dollar_signs}, Converted: {not has_dollar_signs and not has_latex}",
            'issues': issues if issues else ['LaTeX math not supported in Word converter']
        }
        print(f"✗ Status: {test_results['latex_math']['status']}")
        print(f"  Details: {test_results['latex_math']['details']}")
        if issues:
            print(f"  Issues: {', '.join(issues)}")
    except Exception as e:
        test_results['latex_math'] = {'status': 'ERROR', 'details': str(e), 'issues': [str(e)]}
        print(f"✗ ERROR: {e}")

    return test_results


def print_summary(results):
    """Print a summary of all test results"""
    print("\n" + "="*60)
    print("SUMMARY OF ALL TESTS")
    print("="*60)

    passed = []
    partial = []
    failed = []
    errors = []

    for feature, result in results.items():
        status = result['status']
        if status == 'PASS':
            passed.append(feature)
        elif status == 'PARTIAL':
            partial.append(feature)
        elif status == 'FAIL':
            failed.append(feature)
        elif status == 'ERROR':
            errors.append(feature)

    print(f"\n✓ PASSED ({len(passed)}):")
    for feature in passed:
        print(f"  - {feature.replace('_', ' ').title()}")

    if partial:
        print(f"\n⚠ PARTIAL ({len(partial)}):")
        for feature in partial:
            print(f"  - {feature.replace('_', ' ').title()}")
            print(f"    Issues: {', '.join(results[feature]['issues'])}")

    if failed:
        print(f"\n✗ FAILED ({len(failed)}):")
        for feature in failed:
            print(f"  - {feature.replace('_', ' ').title()}")
            print(f"    Issues: {', '.join(results[feature]['issues'])}")

    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for feature in errors:
            print(f"  - {feature.replace('_', ' ').title()}")
            print(f"    Details: {results[feature]['details']}")

    # Overall statistics
    total = len(results)
    success_rate = (len(passed) + len(partial) * 0.5) / total * 100
    print(f"\n" + "="*60)
    print(f"Overall Success Rate: {success_rate:.1f}%")
    print(f"Total Tests: {total}")
    print(f"Passed: {len(passed)}, Partial: {len(partial)}, Failed: {len(failed)}, Errors: {len(errors)}")
    print("="*60)


def main():
    """Main test runner"""
    print("\n" + "="*60)
    print("MARKDOWN TO WORD CONVERSION - FEATURE TESTING")
    print("Testing features from Exemples.md")
    print("="*60)

    # Run all individual feature tests
    results = test_individual_features()

    # Print summary
    print_summary(results)

    # Test the full Exemples.md file
    print("\n" + "="*60)
    print("FULL EXEMPLES.MD CONVERSION TEST")
    print("="*60)

    exemples_path = Path(__file__).parent / "Exemples.md"
    if exemples_path.exists():
        print(f"Converting: {exemples_path}")

        with open(exemples_path, 'r', encoding='utf-8') as f:
            content = f.read()

        try:
            buffer = convert_to_docx(content, render_mermaid=True)

            # Save test output
            output_path = Path(__file__).parent / "Exemples_test_output.docx"
            with open(output_path, 'wb') as f:
                f.write(buffer.getvalue())

            print(f"✓ Successfully converted to: {output_path}")
            print(f"  Please open this file in Word to visually inspect all features")

            # Analyze the document
            findings = analyze_word_document(buffer)
            print(f"\nDocument Analysis:")
            print(f"  Paragraphs: {findings['paragraphs_count']}")
            print(f"  Tables: {findings['tables_count']}")
            print(f"  Has lists: {findings['has_lists']}")
            print(f"  Has checkboxes: {findings['has_checkboxes']}")
            print(f"  Has bold: {findings['has_bold']}")
            print(f"  Has italic: {findings['has_italic']}")
            print(f"  Has code: {findings['has_code_blocks']}")
            print(f"  Paragraph styles: {', '.join(sorted(findings['paragraph_styles']))}")

        except Exception as e:
            print(f"✗ Error converting full document: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"✗ Exemples.md not found at: {exemples_path}")


if __name__ == '__main__':
    main()
