# Custom Beamer Template

Beamer theme following UTN BHI (Universidad Tecnológica Nacional - Bahía Blanca)
design guidelines.

![Sample slide](sample-slide.png)

## Build

```sh
sh run.sh
```

Produces `output/main.pdf`. Uses `latexmk` when available, otherwise three
`pdflatex` passes plus `bibtex`. To build another file: `sh run.sh slides`.

### On Windows (WSL)

`run.sh` needs a POSIX shell, so build from WSL rather than PowerShell:

```powershell
wsl sh run.sh
```

One-time setup inside WSL (Ubuntu):

```sh
sudo apt update
sudo apt install -y texlive-latex-recommended texlive-latex-extra \
                    texlive-fonts-recommended texlive-bibtex-extra latexmk
```

The repository can live on the Windows drive; WSL reaches it under
`/mnt/c/...`. Open the PDF with `explorer.exe output/main.pdf`.

### Requirements

`pdflatex` and `bibtex`, plus the packages `beamer`, `graphicx`, `xcolor`,
`booktabs`, `listings`, `microtype`, `amsmath`, `amsfonts`, `amssymb`, `url`.

## Using the theme

```latex
\usetheme{UTN-BHI}
\usetheme[listings]{UTN-BHI}
```

| Option | Effect |
| --- | --- |
| `listings` | Loads `listings` and defines `\lstdefinestyle{utnbhi}`. Without it the theme pulls in nothing extra. |
| `pagebackground` | Uses the legacy full-page raster background instead of the footline logo. Letterboxed, never stretched. |
| `nologo` | Draws no logo, but still reserves its space. |
| `classicgreen` | Restores the original `#CBD300` frame titles (1.63:1 — unreadable on a projector). |

`\utnbhinologo` hides the logo for the rest of the current group without
changing the text area, so slides do not shift:

```latex
{ \utnbhinologo \begin{frame} ... \end{frame} }
```

Logo geometry is adjustable with `\utnbhilogoheight` and `\utnbhilogosep`.

With the `listings` option, apply the bundled style:

```latex
\lstset{style=utnbhi, language=C}
```

Set the aspect ratio on the document class: `\documentclass[aspectratio=169]{beamer}`
(the default here) or `aspectratio=43`. The theme looks the same in both.

## Using the theme from another project

Assets are found through `\utnbhiassetpath`, which defaults to `theme/`. You do
not have to copy files into your own project — put the checkout on `TEXINPUTS`:

```sh
TEXINPUTS="./custom-beamer:$TEXINPUTS" pdflatex slides.tex
```

The trailing entry separator matters (`:` on Unix, `;` on Windows). To point
only the assets somewhere else, define the path before `\usetheme`:

```latex
\providecommand{\utnbhiassetpath}{../custom-beamer/theme/}
```

## Colours

`greenUTN` (`#CBD300`) measures **1.63:1** against white, where WCAG asks 4.5:1
for body text and 3:1 for large text. Up to v1.x it coloured every frame title,
which is why titles washed out on a projector. It is now an accent only.

| Colour | Hex | On white | Used for |
| --- | --- | --- | --- |
| `greenUTN` | `#CBD300` | 1.63:1 | accent: bullets, logo |
| `greenUTNtitle` | `#929800` | 3.13:1 | frame titles, title page (large text) |
| `greenUTNdark` | `#6F7500` | 4.98:1 | subtitle, captions, toc, code keywords |
| `grayUTN` | `#767577` | 4.58:1 | body text |
| `grayUTNdark` | `#5A5A5C` | 6.88:1 | text on tints (blocks, code) |
| `alertUTN` | `#A03000` | 7.20:1 | `\alert`, alert blocks, code strings |

`greenUTNtitle` is the brightest point on the logo's own hue that still clears
3:1, so titles stay brand green instead of going olive. Verify the palette with
`python3 theme/check-contrast.py`.

## Layout

| File | Role |
| --- | --- |
| `main.tex` | Sample deck — start here |
| `beamerthemeUTN-BHI.sty` | The theme |
| `references.bib` | Bibliography |
| `run.sh` | Build script |
| `theme/utn-bhi-logo.png` | Logo drawn in the footline |
| `theme/utn-bhi-page{,-blank}.png` | Legacy backgrounds, kept for compatibility |
| `theme/utn-bhi.svg` | Source artwork (one embedded JPEG, not true vector) |
| `theme/make-logo.py` | Regenerates the logo from the SVG (needs Pillow) |
| `theme/check-contrast.py` | Checks the palette against WCAG |

## Troubleshooting

- Compilation fails — read `output/main.log`
- `File 'theme/utn-bhi-logo' not found` — compiling from another directory; see
  *Using the theme from another project*
- Text overlapping the logo — you are on v1.x, or you have overridden the
  `footline` template; the theme reserves the logo's space itself
- `run.sh: not found` or `\r` errors in WSL — the file must keep LF line endings

## Author

Javier Iparraguirre  
Universidad Tecnológica Nacional - Bahía Blanca  
<jiparraguirre@frbb.utn.edu.ar>

Licensed GPL-3.0-or-later.
