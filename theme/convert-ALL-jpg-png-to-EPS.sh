#!/bin/bash

# remove previous files
rm *.eps

# generate *.eps files
for file in `ls *.png`; do
     convert -density 600 -depth 32 $file ${file%.*}.eps;
done

for file in `ls *.jpg`; do
     convert -density 600 -depth 32 $file ${file%.*}.eps;
done

