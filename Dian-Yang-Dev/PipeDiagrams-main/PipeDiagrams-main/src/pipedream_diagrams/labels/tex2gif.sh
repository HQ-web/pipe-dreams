#!/bin/bash
#
for file in $*; do
    echo "Processing $file"
    latex $file >& /dev/null
    dvigif ${file%.tex}.dvi -o ${file%.tex}.gif >& /dev/null
done
rm *.aux *.log *.dvi
