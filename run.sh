#!/bin/bash

pdflatex projects/song_selector/a4_half.tex && pdflatex projects/bookletization/booklet_a4_pysty.tex && pdflatex projects/placement/a4_placement.tex && rm *.log *.aux


