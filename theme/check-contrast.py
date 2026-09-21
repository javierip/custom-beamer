#!/usr/bin/env python3
"""Check every text colour in the theme against its background (WCAG 2.1).

    python3 theme/check-contrast.py

WCAG asks 4.5:1 for body text and 3:1 for large text (>= 18 pt, or >= 14 pt
bold).  Frame titles and the title page are \\Large -- 17.3 pt at beamer's
11 pt base, and projected metres wide -- so they are checked at 3:1.  Anything
set at \\normalsize or smaller is checked at 4.5:1.

Exits non-zero if any pair falls below its threshold.  Keep the pairs below in
step with the \\setbeamercolor calls in beamerthemeUTN-BHI.sty.
"""
import sys

PALETTE = {
    "greenUTN": "CBD300",        # accent only -- never used for text
    "greenUTNtitle": "929800",
    "greenUTNdark": "6F7500",
    "grayUTN": "767577",
    "grayUTNdark": "5A5A5C",
    "alertUTN": "A03000",
    "utnbhiblockbg": "EFEFE6",
    "utnbhicodebg": "F5F5F0",
    "utnbhicodecomment": "5F6B3A",
    "white": "FFFFFF",
}

LARGE = 3.0
BODY = 4.5

# (description, foreground, background, threshold)
PAIRS = [
    ("frametitle",             "greenUTNtitle",     "white",         LARGE),
    ("title / titlelike",      "greenUTNtitle",     "white",         LARGE),
    ("normal text",            "grayUTN",           "white",         BODY),
    ("subtitle",               "greenUTNdark",      "white",         BODY),
    ("section in toc",         "greenUTNdark",      "white",         BODY),
    ("caption name",           "greenUTNdark",      "white",         BODY),
    ("alerted text",           "alertUTN",          "white",         BODY),
    ("block title",            "white",             "greenUTNdark",  BODY),
    ("block body",             "grayUTNdark",       "utnbhiblockbg", BODY),
    ("block title alerted",    "white",             "alertUTN",      BODY),
    ("block title example",    "white",             "grayUTNdark",   BODY),
    ("listing basicstyle",     "grayUTNdark",       "utnbhicodebg",  BODY),
    ("listing keywordstyle",   "greenUTNdark",      "utnbhicodebg",  BODY),
    ("listing commentstyle",   "utnbhicodecomment", "utnbhicodebg",  BODY),
    ("listing stringstyle",    "alertUTN",          "utnbhicodebg",  BODY),
    ("listing numberstyle",    "grayUTNdark",       "utnbhicodebg",  BODY),
    ("bibliography entry",     "grayUTNdark",       "white",         BODY),
]


def lum(rgb):
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = [f(c) for c in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def rgb(name):
    h = PALETTE[name]
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def main():
    failures = 0
    for what, fg, bg, minimum in PAIRS:
        r = ratio(rgb(fg), rgb(bg))
        ok = r >= minimum
        failures += not ok
        print(f"{r:6.2f}:1  {'PASS' if ok else 'FAIL'}  (needs {minimum})  {what}"
              f"  [{fg} #{PALETTE[fg]} on {bg} #{PALETTE[bg]}]")
    print()
    if failures:
        print(f"{failures} pair(s) below threshold")
        return 1
    print(f"all {len(PAIRS)} pairs meet their threshold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
