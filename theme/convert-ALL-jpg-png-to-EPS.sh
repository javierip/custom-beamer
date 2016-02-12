
for f in `ls *.png`; do
     convert -density 300 -depth 32 $f ${f%.*}.eps;
done

for f in `ls *.jpg`; do
     convert -density 300 -depth 32 $f ${f%.*}.eps;
done

