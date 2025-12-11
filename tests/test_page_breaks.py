"""Test page break detection logic"""

from helpers.page_break_handler import is_page_break_marker

# Test cases
test_cases = [
    # Should be page breaks
    ("\\newpage", True, "LaTeX newpage"),
    ("  \\newpage  ", True, "LaTeX newpage with whitespace"),
    ("<!-- pagebreak -->", True, "HTML comment pagebreak"),
    ("<!-- page-break -->", True, "HTML comment page-break"),
    ("<!-- page_break -->", True, "HTML comment page_break"),
    ("<!-- newpage -->", True, "HTML comment newpage"),
    ("<!-- PAGEBREAK -->", True, "HTML comment uppercase"),

    # Should NOT be page breaks
    ("---", False, "Horizontal rule (3 hyphens)"),
    ("-----", False, "Horizontal rule (5 hyphens)"),
    ("***", False, "Horizontal rule (asterisks)"),
    ("___", False, "Horizontal rule (underscores)"),
    ("text --- text", False, "Hyphens in text"),
    ("/newpage", False, "Forward slash newpage"),
    ("\\newpages", False, "Wrong LaTeX command"),
    ("<!-- page break -->", False, "HTML comment with space"),
]

print("Testing page break detection:\n")
all_passed = True

for line, expected, description in test_cases:
    result = is_page_break_marker(line)
    status = "✅ PASS" if result == expected else "❌ FAIL"
    if result != expected:
        all_passed = False
    print(f"{status} | {description:30} | '{line:20}' | Expected: {expected}, Got: {result}")

print("\n" + "="*80)
if all_passed:
    print("✅ ALL TESTS PASSED!")
else:
    print("❌ SOME TESTS FAILED!")
