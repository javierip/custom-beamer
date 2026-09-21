#!/usr/bin/env python3
"""Regenerate theme/utn-bhi-logo.png from theme/utn-bhi.svg.

    python3 theme/make-logo.py

utn-bhi.svg is not really vector art: it is a single 2618x854 JPEG embedded as
a base64 data URI.  This script pulls that JPEG out, crops it to the logo,
recovers a clean alpha channel (the logo is two flat brand colours over white,
so per-pixel coverage can be solved for exactly) and writes a transparent PNG.

Requires Pillow.  Only needs re-running if the source artwork changes.
"""
import base64
import io
import os
import re
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "utn-bhi.svg")
DST = os.path.join(HERE, "utn-bhi-logo.png")

GRAY = np.array([0x76, 0x75, 0x77], float)
GREEN = np.array([0xCB, 0xD3, 0x00], float)
WHITE = np.array([255.0, 255.0, 255.0])

# 200 px tall is ~850 dpi at the 0.5 cm the footline draws it at.
TARGET_HEIGHT = 200
# Alpha quantised to 32 levels: visually identical, but PNG-compresses far
# better because it flattens the JPEG's ringing around the glyph edges.
ALPHA_LEVELS = 31


def embedded_jpeg(svg_path):
    svg = open(svg_path, encoding="utf-8").read()
    m = re.search(r'xlink:href="data:image/jpeg;base64,([^"]+)"', svg)
    if not m:
        sys.exit(f"no embedded JPEG found in {svg_path}")
    raw = base64.b64decode(re.sub(r"\s", "", m.group(1)))
    return Image.open(io.BytesIO(raw)).convert("RGB")


def solve_coverage(pixels, colour):
    """Alpha and residual error for  pixel = alpha*colour + (1-alpha)*white."""
    num = np.einsum("ijk,k->ij", WHITE - pixels, WHITE - colour)
    den = float(np.dot(WHITE - colour, WHITE - colour))
    alpha = np.clip(num / den, 0.0, 1.0)
    residual = pixels - (alpha[..., None] * colour + (1 - alpha[..., None]) * WHITE)
    return alpha, np.einsum("ijk,ijk->ij", residual, residual)


def main():
    pixels = np.array(embedded_jpeg(SRC)).astype(float)

    ink = pixels.sum(axis=2) < 700
    ys, xs = np.nonzero(ink)
    pixels = pixels[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    height, width = pixels.shape[:2]

    alpha_gray, err_gray = solve_coverage(pixels, GRAY)
    alpha_green, err_green = solve_coverage(pixels, GREEN)
    is_green = err_green < err_gray

    alpha = np.where(is_green, alpha_green, alpha_gray)
    alpha[alpha < 0.012] = 0.0
    colour = np.where(is_green[..., None], GREEN, GRAY)

    rgba = np.dstack([colour, alpha * 255]).astype(np.uint8)
    img = Image.fromarray(rgba, "RGBA")
    img = img.resize(
        (round(width * TARGET_HEIGHT / height), TARGET_HEIGHT), Image.LANCZOS
    )

    # Quantise after resampling, otherwise the interpolation puts the noise back.
    out = np.array(img)
    out[:, :, 3] = np.round(
        out[:, :, 3].astype(float) / 255 * ALPHA_LEVELS
    ) / ALPHA_LEVELS * 255
    Image.fromarray(out, "RGBA").save(DST, optimize=True)
    print(f"wrote {DST} ({img.width}x{img.height}) from a {width}x{height} crop")


if __name__ == "__main__":
    main()
