#!/usr/bin/env python3
"""
Repair mojibake (double-encoded UTF-8) in careride-product-page.html.

The file was damaged by a PowerShell Get-Content/Set-Content round-trip that
read UTF-8 bytes as Windows-1252 and re-saved them as UTF-8. This corrupted
emojis AND text punctuation (em dashes, curly quotes, ellipses, etc.).

Strategy:
  1. If ftfy is installed, use it -- it reverses ALL such damage in one pass.
  2. Otherwise fall back to a built-in replacement table (emojis + common
     punctuation). Exact-match only, so nothing else is touched.

Usage:
    pip install ftfy        # recommended -- catches everything
    python fix_mojibake.py
"""

import shutil
import sys

PATH = r"/NetlifySite/careride-product-page.html"

# Deterministic fallback: mojibake -> correct character.
# Punctuation first, then emojis. Keys are the exact corrupted sequences.
FALLBACK = {
    # --- punctuation ---
    "\u00e2\u20ac\u201c":       "\u2013",          # – en dash
    "\u00e2\u20ac\u201d":       "\u2014",          # — em dash
    "\u00e2\u20ac\u02dc":       "\u2018",          # ‘ left single quote
    "\u00e2\u20ac\u2122":       "\u2019",          # ’ right single quote
    "\u00e2\u20ac\u0153":       "\u201c",          # “ left double quote
    "\u00e2\u20ac\x9d":         "\u201d",          # ” right double quote
    "\u00e2\u20ac\u00a6":       "\u2026",          # … ellipsis
    "\u00e2\u20ac\u00a2":       "\u2022",          # • bullet
    "\u00c2\u00a0":             "\u00a0",          # non-breaking space
    # --- emojis ---
    "\u00f0\u0178\u0152\u2122":               "\U0001F319",        # 🌙
    "\u00f0\u0178\u0152\u2018":               "\U0001F311",        # 🌑
    "\u00f0\u0178\u201c\u00b5":               "\U0001F4F5",        # 📵
    "\u00f0\u0178\u201c\u017e":               "\U0001F4DE",        # 📞
    "\u00f0\u0178\u201c\u2039":               "\U0001F4CB",        # 📋
    "\u00f0\u0178\u02dc\u0178":               "\U0001F61F",        # 😟
    "\u00f0\u0178\u2013\u00a5\u00ef\u00b8\x8f": "\U0001F5A5\uFE0F", # 🖥️
    "\u00f0\u0178\u201c\u00b1":               "\U0001F4F1",        # 📱
    "\u00f0\u0178\u201c\u0160":               "\U0001F4CA",        # 📊
    "\u00f0\u0178\u0161\x90":                 "\U0001F690",        # 🚐
    "\u00f0\u0178\x8f\u00a5":                 "\U0001F3E5",        # 🏥
    "\u00f0\u0178\x8f\u00a1":                 "\U0001F3E1",        # 🏡
    "\u00f0\u0178\u2019\u2030":               "\U0001F489",        # 💉
    "\u00f0\u0178\u201c\u00a6":               "\U0001F4E6",        # 📦
}


def main():
    try:
        with open(PATH, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"File not found: {PATH}")
        sys.exit(1)

    shutil.copy2(PATH, PATH + ".bak")
    print(f"Backup written: {PATH}.bak")

    try:
        import ftfy
        fixed = ftfy.fix_encoding(text)
        method = "ftfy (full repair)"
    except ImportError:
        print("ftfy not installed -- using built-in table.")
        print("For the most complete fix run:  pip install ftfy")
        fixed = text
        for bad, good in FALLBACK.items():
            fixed = fixed.replace(bad, good)
        method = "built-in table"

    if fixed == text:
        print("No corrupted sequences found. Nothing changed.")
        return

    with open(PATH, "w", encoding="utf-8") as f:
        f.write(fixed)
    print(f"Done. File repaired via {method} and saved as UTF-8.")


if __name__ == "__main__":
    main()
