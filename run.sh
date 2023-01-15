#!/bin/bash

export TEXMFHOME=library/latex-libraries

bin/texlive/2022/bin/x86_64-linux/pdflatex projects/song_selector/a4_half.tex


bin/texlive/2022/bin/x86_64-linux/pdflatex projects/bookletization/booklet_a4_pysty.tex

bin/texlive/2022/bin/x86_64-linux/pdflatex projects/placement/a4_placement.tex

# Cleanup
rm *.log *.aux


