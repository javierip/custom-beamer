#!/usr/bin/env python3
"""Derive the on-screen logo from the print master.

    python3 theme/make-logo.py

theme/utn_bhi_isologotipo.jpg is the designer's master: a CMYK JPEG carrying
the two institutional inks, Pantone 382 and Pantone Cool Gray 9.  It is the
file of record and must not be edited.

It cannot be used in a slide deck as-is.  pdflatex embeds it as DeviceCMYK,
and a viewer without colour management renders it #A6FF07 / #4F6675 instead
of the #CBD300 / #767577 that section 2.8 of the Manual de Identidad Visual
specifies for RGB media.  This script separates the master into its two inks,
recovers per-pixel coverage, and repaints them at the manual's RGB values on a
transparent background.

The master's own frame is kept intact.  Its padding is 1.05a above, 1.22a
below and 1.69a at the sides, where a is the height of the "arañita" -- so the
file already carries the area de proteccion that section 2.3 requires, and
cropping it would destroy that.  Nothing here changes the isologotipo's
proportions, colours or composition (section 2.5).

Requires Pillow and NumPy.
"""
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "utn_bhi_isologotipo.jpg")
DST = os.path.join(HERE, "utn-bhi-logo.png")

# The two institutional inks as they are stored in the master, and the RGB
# values the manual gives for each (section 2.8).
INKS = [
    # name,               CMYK in master,          RGB for screen
    ("Pantone 382",       (89, 0, 248, 0),         (0xCB, 0xD3, 0x00)),
    ("Pantone Cool Gray 9", (148, 125, 110, 28),   (0x76, 0x75, 0x77)),
]

# Full frame 2618 px wide; this keeps the isologotipo itself at ~717 px, i.e.
# about 600 dpi at the 3 cm minimum width of section 2.6.
TARGET_WIDTH = 1000
ALPHA_LEVELS = 31


def coverage(pixels, ink):
    """Per-pixel tint of a single ink, plus how well it explains the pixel."""
    ink = np.asarray(ink, float)
    tint = np.clip(np.einsum("ijk,k->ij", pixels, ink) / float(ink @ ink), 0.0, 1.0)
    residual = pixels - tint[..., None] * ink
    return tint, np.einsum("ijk,ijk->ij", residual, residual)


def main():
    master = Image.open(SRC)
    if master.mode != "CMYK":
        sys.exit(f"expected a CMYK master, got {master.mode}")
    pixels = np.array(master).astype(float)

    tints, errors = zip(*(coverage(pixels, cmyk) for _, cmyk, _ in INKS))
    winner = np.argmin(np.stack(errors), axis=0)

    alpha = np.choose(winner, tints)
    alpha[alpha < 0.012] = 0.0
    rgb = np.stack(
        [np.choose(winner, [float(srgb[c]) for _, _, srgb in INKS]) for c in range(3)],
        axis=-1,
    )

    img = Image.fromarray(np.dstack([rgb, alpha * 255]).astype(np.uint8), "RGBA")
    height = round(img.height * TARGET_WIDTH / img.width)
    img = img.resize((TARGET_WIDTH, height), Image.LANCZOS)

    # Quantise after resampling, otherwise the interpolation puts back the
    # JPEG ringing that costs most of the file size.
    out = np.array(img)
    out[:, :, 3] = (
        np.round(out[:, :, 3].astype(float) / 255 * ALPHA_LEVELS) / ALPHA_LEVELS * 255
    )
    Image.fromarray(out, "RGBA").save(DST, optimize=True)
    print(f"wrote {DST} ({img.width}x{img.height}) from {master.width}x{master.height}")


if __name__ == "__main__":
    main()
