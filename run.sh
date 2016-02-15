#!/bin/bash

rm *.aux
rm *.bbl
rm *.blg
rm *.dvi
rm *.log
rm *.nav
rm *.out
rm *.pdf
rm *.snm
rm *.toc
sh theme/convert-ALL-jpg-png-to-EPS.sh 
latex main.tex 
latex main.tex 
bibtex main
latex main.tex 
pdflatex main.tex 


