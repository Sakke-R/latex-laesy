#!/bin/bash

export TEXMFHOME=library/latex-libraries

compile_cmd="bin/texlive/2022/bin/x86_64-linux/pdflatex projects/song_selector/a4_half_generated.tex"

while getopts 'l' OPTION; do
  case "$OPTION" in
    l)
      echo "Latter compilation. Generating final products from pregeneration."
      compile_cmd="bin/texlive/2022/bin/x86_64-linux/pdflatex projects/bookletization/booklet_a4_pysty.tex"
      compile_cmd+=" && bin/texlive/2022/bin/x86_64-linux/pdflatex projects/placement/a4_placement.tex"
      ;;
    *)
      echo "Unknown switch. Defaulting to full compilation."
      compile_cmd+=" && bin/texlive/2022/bin/x86_64-linux/pdflatex projects/bookletization/booklet_a4_pysty.tex"
      compile_cmd+=" && bin/texlive/2022/bin/x86_64-linux/pdflatex projects/placement/a4_placement.tex"
      ;;
  esac
done

echo $compile_cmd
eval $compile_cmd

# Cleanup
rm *.log *.aux


