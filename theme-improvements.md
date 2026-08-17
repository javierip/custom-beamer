# UTN-BHI Beamer theme — review and improvement brief

Review of [javierip/custom-beamer](https://github.com/javierip/custom-beamer)
(`beamerthemeUTN-BHI.sty`, its `theme/` assets, `main.tex`, `run.sh` and the
README), written while adapting the theme for the 16:9 deck in
`class-extra-c-styles/slides.tex`.

All the changes below belong in the **theme repository**, not in this one.

---

## Findings, worst first

### 1. Frame titles are unreadable — 1.63:1 contrast

`greenUTN` is `#CBD300`. Against the white slide background that measures
**1.63:1**, where WCAG asks for 4.5:1 (3:1 for large text). It is the colour of
every frame title and of the title-page title, i.e. the text that has to survive
a bright classroom and a washed-out projector.

`#6F7500` measures **4.98:1** and keeps the same hue. The brand green stays for
accents: rules, itemize bullets, the logo.

For reference, `grayUTN` (`#767577`, the body text colour) measures 4.59:1 —
it passes, but only just.

### 2. The background is a raster image, stretched

```latex
\usebackgroundtemplate{\includegraphics[width=\paperwidth,height=\paperheight]{theme/utn-bhi-page}}
```

`theme/utn-bhi-page.png` is 1512×1134 (4:3). On a 16:9 deck this stretches the
logo by 33%. It is also a 20 KB bitmap that is ~98% white, painted on every
page, while `theme/utn-bhi.svg` already exists as a vector source.

### 3. Nothing reserves space for the logo

The theme sets `\setbeamertemplate{footline}{}`, so beamer gives the text block
the full page height and any well-filled slide prints straight through the logo.
Drawing the logo *in* the footline fixes this and the previous point at once,
because beamer then subtracts the footline height from the text area
automatically.

### 4. The listing style lives in the sample deck, not in the theme

`\lstdefinestyle{myC++Style}` is defined in `main.tex`, hardcodes
`language=C++` and `\small`, and is never applied globally (no `\lstset`), so a
deck that copies the preamble — the documented way to start — gets unstyled code
that overflows the slide. Every deck ends up re-inventing this.

### 5. Assets are addressed relative to the compilation directory

`theme/utn-bhi-page` only resolves if the deck is compiled from the theme's own
folder. Using the theme from another project requires either copying the files
in (what the pong presentation's README tells you to do) or setting `TEXINPUTS`.
An overridable asset-path macro removes the coupling.

### 6. Package hygiene

No `\NeedsTeXFormat`, no `\ProvidesPackage`, no `\mode<presentation>` wrapper,
no options, and `\usetheme{default}` is called from inside a theme file, where
the supported mechanism is the inner/outer/colour/font theme calls.

### 7. Docs and tooling

- The README points at `example.pdf`, which was deleted in commit `13bfc11`.
- `run.sh` starts with `#!/bin/bash` but the README documents `sh run.sh`.
- `run.sh` runs `rm -f *.eps` in the repository root — that is exactly what
  `theme/convert-ALL-jpg-png-to-EPS.sh` generates.
- `.gitignore` does not cover the `output/` directory it creates.

---

## Brief for the agent

Copy everything below this line into the agent's prompt.

---

# Task: improve the UTN-BHI Beamer theme

Repo: https://github.com/javierip/custom-beamer (work on a branch, open a PR).
The theme is `beamerthemeUTN-BHI.sty`, used as `\usetheme{UTN-BHI}`. Assets are
in `theme/`. `main.tex` is the sample deck, built by `run.sh`.

## Hard constraints

- Existing decks must keep compiling unchanged: the file name, the theme name,
  `\usetheme{UTN-BHI}` and `theme/utn-bhi-page{,-blank}.png` must all survive.
  Anything new is opt-in via theme options, with today's look as the default
  wherever a change would be visible — EXCEPT the colour fix in task 1, which is
  a deliberate visual change.
- Do not commit PDFs or build output. Keep the GPL-3.0 header.
- pdflatex + TeX Live only; do not require lualatex, xelatex or minted.

## Task 1 — Fix text contrast (highest priority)

`greenUTN` = `#CBD300` measures 1.63:1 against white and is used for
`frametitle` and `title`. Keep it as an accent (rules, itemize bullets, logo)
and introduce a darker text green, `#6F7500` (4.98:1), for
frametitle/title/structure text. Verify with the script under "Verification":
every text colour must be at least 4.5:1 against its background.

## Task 2 — Replace the full-page background with a footline logo

- Produce `theme/utn-bhi-logo.pdf`: crop the logo out of `theme/utn-bhi.svg` and
  export to PDF (`inkscape --export-type=pdf --export-area-drawing`). Commit the
  PDF and keep the SVG as the source.
- Define the footline as a centred logo at a fixed height (~0.6 cm) with ~0.25 cm
  of padding above and below. This draws the logo *and* reserves its space, so
  slide text can no longer overlap it.
- Drop `\usebackgroundtemplate` from the default path. Keep a `pagebackground`
  theme option that restores the old raster background for backwards
  compatibility, and when it is used, letterbox instead of stretching:
  `\includegraphics[height=\paperheight]`, centred horizontally.
- The result must look the same in 4:3 and 16:9, apart from the logo finally
  being correctly proportioned in 16:9.

## Task 3 — Make asset paths relocatable

Introduce `\providecommand{\utnbhiassetpath}{theme/}` (or an `assetpath=`
option) and use it in every `\includegraphics` inside the theme, so a deck that
keeps the theme in a sibling directory can point at it instead of copying files.
Document the `TEXINPUTS="./custom-beamer:"` alternative in the README.

## Task 4 — Ship the code-listing style in the theme

Move the listing style out of `main.tex` into the theme as
`\lstdefinestyle{utnbhi}`, language-agnostic (no `language=C++` baked in) and
sized to fit two-column comparison slides: `\ttfamily\scriptsize`,
`columns=flexible`, `breaklines=true`, frame plus light background, line
numbers. Load `listings` only under a `listings` theme option, so decks that
don't use it pay nothing. Update `main.tex` to `\lstset{style=utnbhi, language=C}`.

## Task 5 — Complete the colour palette

Beamer's default red `alerted text` and its default block colours clash with the
green/gray palette. Define `alerted text`, `block title`, `block body`,
`block title alerted`, `block title example` and `caption name` from the brand
palette, again respecting the 4.5:1 rule.

## Task 6 — Package hygiene

Add `\NeedsTeXFormat` and `\ProvidesPackage{beamerthemeUTN-BHI}[<date> vX.Y ...]`,
wrap the body in `\mode<presentation>`, and declare the options with
`\DeclareOptionBeamer` / `\ProcessOptionsBeamer`. Replace the internal
`\usetheme{default}` with explicit `\useinnertheme` / `\useoutertheme` /
`\usecolortheme` / `\usefonttheme` calls.

## Task 7 — Sample deck and docs

- `main.tex`: build it 16:9 (`\documentclass[aspectratio=169]{beamer}`) and add
  a slide per theme option, a two-column code-comparison slide, and a booktabs
  table with `p{}` columns.
- README: remove the reference to `example.pdf` (deleted in `13bfc11`), document
  the theme options, the required TeX Live packages, the asset-path / `TEXINPUTS`
  story, and how to use the theme from another project without copying files.
- `run.sh`: make the shebang match the documented invocation, drop the
  `rm -f *.eps` in the repository root (it deletes generated assets), and prefer
  `latexmk -pdf` when available, keeping the current three-pass path as fallback.
- Add `output/` to `.gitignore`.

## Task 8 — CI

Add a GitHub Actions workflow that installs TeX Live and compiles `main.tex` in
both 4:3 and 16:9, failing on any LaTeX error and on any `Overfull \hbox` in the
sample deck. Upload the PDF as a build artifact.

## Verification (run before opening the PR)

1. Build the 4:3 and 16:9 sample decks; both must exit 0 and log zero
   `Overfull \hbox`.
2. Rasterise and actually LOOK at every page
   (`mutool draw -o p%02d.png -r 130 main.pdf`): no text may touch the logo, and
   the logo must be undistorted in both aspect ratios.
3. Check every text colour against its background:

   ```python
   def lum(rgb):
       f = lambda c: c/12.92 if c <= 0.03928 else ((c + 0.055)/1.055)**2.4
       r, g, b = [f(c) for c in rgb]
       return 0.2126*r + 0.7152*g + 0.0722*b

   def ratio(a, b):
       la, lb = lum(a), lum(b)
       return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)
   ```

4. Regression: compile an *unmodified* pre-existing deck — for example
   `project-game-pong/pong-presentation` in javierip/structured-programming-C —
   against the new theme, and confirm it still builds and still looks right.

## Report back

A summary of each change, before/after screenshots of a text-heavy slide in both
aspect ratios, and the measured contrast ratios.

---

## Follow-up in this repository

Once tasks 2–4 are released upstream, the workarounds in the preamble of
`class-extra-c-styles/slides.tex` become redundant and should be removed:

- the centred `\usebackgroundtemplate` override,
- the `\setbeamertemplate{footline}{\rule{0pt}{0.9cm}}` spacer,
- the global `\lstset` that applies `myC++Style` in C at `\scriptsize`.

Worth mentioning in the PR description so both sides are cleaned up together.
