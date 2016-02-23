#!/bin/bash

# prepare theme figures
cd theme/
sh convert-ALL-jpg-png-to-EPS.sh 
cd ..

# clean previous files (optional)
rm *.aux
rm *.bbl
rm *.blg
rm *.dvi
rm *.log
rm *.nav
rm *.out
rm *.snm
rm *.toc
rm *.eps

# compile (full version)
latex main.tex 
latex main.tex 
bibtex main
latex main.tex 
pdflatex main.tex 


