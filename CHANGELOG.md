# Changelog

## v2.0.0 — 2026-09-21

A breaking release. It fixes frame titles that were unreadable on a projector,
stops slide text printing through the logo, and brings the theme in line with
the *Manual de Identidad Visual Institucional* (UTN-FRBB, FEB 2014).

### Breaking

- **Frame titles changed colour.** `#CBD300` measured 1.63:1 against white,
  where WCAG asks 3:1 for large text. Titles now use `#929800`, the brightest
  point on the logo's own hue that clears that bar. Pass `classicgreen` to
  `\usetheme` to restore the old colour.
- **Removed `theme/utn-bhi-page.png`, `theme/utn-bhi-page-blank.png`,
  `theme/utn-bhi.svg` and `theme/utn-bhi-blank.svg`**, superseded by the
  designer's master logo. A deck that hid the logo with
  `\usebackgroundtemplate{...utn-bhi-page-blank.png}` should use
  `\utnbhinologo` instead; one that drew `utn-bhi-page.png` should drop the
  `\usebackgroundtemplate` line, since the theme now draws the logo itself.
- **Removed the `pagebackground` option**, whose raster asset is gone.
- **`\utnbhilogoheight` is now `\utnbhilogowidth`**, and sets the width of the
  isologotipo itself (default `3cm`, the minimum of §2.6).
- **The default font is now Arial/Helvetica** (§3.2), via `helvet`. Pass
  `nobrandfont` to keep Beamer's default sans.
- **The sample deck is 16:9** (`aspectratio=169`). The theme renders the same
  in 4:3.

### Added

- `theme/utn_bhi_isologotipo.jpg` — the designer's master logo, committed
  unmodified. It is CMYK, so it cannot be used in a deck directly: `pdflatex`
  embeds it as DeviceCMYK and an uncolour-managed viewer renders it
  `#A6FF07 / #4F6675`. `theme/make-logo.py` separates the two institutional
  inks and repaints them at the RGB values §2.8 specifies, producing the sRGB
  `theme/utn-bhi-logo.png` the theme draws.
- The logo is drawn in the footline, so Beamer subtracts its height from
  `\textheight` and slide content can no longer overlap it. The master's own
  frame carries the *área de protección* of §2.3 and is never cropped.
- Theme options `listings`, `nologo`, `nobrandfont`, `classicgreen`.
- `\lstdefinestyle{utnbhi}` — a language-agnostic listing style, loaded only
  under the `listings` option.
- `\utnbhiassetpath`, so the theme can be used from another project without
  copying files in. `TEXINPUTS` works too.
- `\utnbhinologo` / `\utnbhiwithlogo` to suppress the logo per group of frames
  while keeping its space reserved.
- A complete colour palette: `alerted text`, block colours and `caption name`
  now come from the brand palette instead of Beamer's stock red and blue.
- `theme/check-contrast.py`, which checks every text colour against its
  background and runs in CI.
- GitHub Actions workflows: build (both aspect ratios) and release.

### Changed

- Package hygiene: `\NeedsTeXFormat`, `\ProvidesPackage`, a `\mode<presentation>`
  wrapper, and options declared with `\DeclareOptionBeamer`. The internal
  `\usetheme{default}` is replaced by explicit inner/outer/colour/font themes.
- `run.sh` uses `latexmk` when available, no longer deletes generated `*.eps`
  from the repository root, takes an optional file name, and reports overfull
  boxes.
- README rewritten: WSL build instructions, theme options, brand compliance.

### Fixed

- Every text colour now meets its WCAG threshold — 4.5:1 for body text, 3:1
  for large text. Verified by `theme/check-contrast.py`.
- The 4:3 background is no longer stretched 33% wider on a 16:9 deck.

## 1.1.0

Earlier releases predate this changelog.
