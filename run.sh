#!/bin/sh

# This script compiles the LaTeX presentation without user interaction.
# All output files are placed in the 'output' directory.
#
#   sh run.sh            compile main.tex
#   sh run.sh slides     compile slides.tex

set -e # Exit immediately if a command exits with a non-zero status

OUTPUT_DIR="output"
MAIN_FILE="${1:-main}"

mkdir -p "$OUTPUT_DIR"

echo "--- Starting LaTeX compilation ---"

# Clean previous build output. Only the output directory is touched: the
# repository root holds generated assets (theme/*.eps) that must survive.
rm -f "$OUTPUT_DIR"/*

if command -v latexmk >/dev/null 2>&1; then
    echo "--- Using latexmk ---"
    latexmk -pdf -interaction=nonstopmode -halt-on-error \
            -output-directory="$OUTPUT_DIR" "$MAIN_FILE.tex"
else
    echo "--- latexmk not found, falling back to three pdflatex passes ---"

    echo "--- Compiling LaTeX (pass 1) ---"
    pdflatex -interaction=nonstopmode -output-directory="$OUTPUT_DIR" "$MAIN_FILE.tex"

    echo "--- Running BibTeX ---"
    bibtex "$OUTPUT_DIR/$MAIN_FILE" || true

    echo "--- Compiling LaTeX (pass 2) ---"
    pdflatex -interaction=nonstopmode -output-directory="$OUTPUT_DIR" "$MAIN_FILE.tex"

    echo "--- Compiling LaTeX (final pass) ---"
    pdflatex -interaction=nonstopmode -output-directory="$OUTPUT_DIR" "$MAIN_FILE.tex"
fi

echo "---"
echo "Compilation complete!"
echo "Output PDF: $OUTPUT_DIR/$MAIN_FILE.pdf"

if [ -f "$OUTPUT_DIR/$MAIN_FILE.pdf" ]; then
    echo "OK - PDF generated successfully"
else
    echo "FAILED - check the log file: $OUTPUT_DIR/$MAIN_FILE.log"
    exit 1
fi

# Report overfull boxes; they are the usual cause of text running off a slide.
# Note that beamer does not warn about a frame whose body is simply taller
# than the slide, so a clean run here is not a promise that nothing overflows.
OVERFULL=$(grep -c 'Overfull \\[hv]box' "$OUTPUT_DIR/$MAIN_FILE.log" || true)
if [ "${OVERFULL:-0}" -gt 0 ]; then
    echo "Warning: $OVERFULL overfull box(es) in $OUTPUT_DIR/$MAIN_FILE.log"
fi
