# Custom Beamer Template

Custom Beamer template that follows UTN BHI (Universidad Tecnológica Nacional - Bahía Blanca) design guidelines.

![Sample slide](sample-slide.png)

## Features

- **Modern LaTeX Best Practices**: Uses `pdflatex` with proper font encoding and typography
- **Professional Styling**: Includes enhanced code highlighting, tables with `booktabs`, and mathematical expressions
- **Clean Build Process**: All compilation output goes to the `output/` directory
- **UTN BHI Branding**: Custom colors, logos, and visual elements following university guidelines
- **Ready-to-Use Examples**: Includes slides for figures, tables, code, math, and references

## Project Structure

```
├── main.tex                    # Main LaTeX document (start here)
├── beamerthemeUTN-BHI.sty     # Custom Beamer theme
├── references.bib             # Bibliography file
├── run.sh                     # Compilation script
├── theme/                     # Theme assets (logos, backgrounds)
├── output/                    # Compiled files (auto-generated)
└── README.md                  # This file
```

## Requirements

- LaTeX distribution with `pdflatex`
- Required packages: `beamer`, `graphicx`, `booktabs`, `listings`, `xcolor`, `amsmath`
- Linux/Unix environment with bash

## Compile Instructions

The file `main.tex` is the starting point. To compile the presentation:

### Quick Start
```bash
sh run.sh
```

### What the script does:
1. Creates an `output/` directory for all compilation files
2. Runs `pdflatex` three times to resolve citations and cross-references
3. Processes bibliography with `bibtex`
4. Generates the final PDF in `output/main.pdf`

### Manual Compilation
If you prefer manual control:
```bash
mkdir -p output
pdflatex -output-directory=output main.tex
bibtex output/main
pdflatex -output-directory=output main.tex
pdflatex -output-directory=output main.tex
```

## Output

After successful compilation, you'll find:
- **`output/main.pdf`** - The final presentation
- **`output/main.log`** - Compilation log (useful for debugging)
- Other auxiliary files in the `output/` directory

The file `example.pdf` shows a typical output of the template.

## Customization

1. **Content**: Edit `main.tex` to add your slides and content
2. **Bibliography**: Add references to `references.bib`
3. **Theme Colors**: Modify `beamerthemeUTN-BHI.sty` to change colors or styling
4. **Language**: Uncomment `\usepackage[spanish]{babel}` for Spanish support

## Features Included

- **Section slides**: Automatic section dividers
- **Code highlighting**: Enhanced syntax highlighting for multiple languages
- **Professional tables**: Using `booktabs` package
- **Mathematical expressions**: Full `amsmath` support
- **Figure handling**: Optimized for PNG/JPG images
- **Clean typography**: Modern font encoding and microtype

## Troubleshooting

- If compilation fails, check `output/main.log` for errors
- Ensure all required LaTeX packages are installed
- Verify that image files exist in the `theme/` directory
- The script uses non-interactive mode to prevent hanging on errors

## Author

Javier Iparraguirre  
Universidad Tecnológica Nacional - Bahía Blanca  
jiparraguirre@frbb.utn.edu.ar
