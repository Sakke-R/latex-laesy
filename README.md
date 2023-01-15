init with:
sudo apt install texlive texlive-lang-european




cd projects
run e.g.
pdflatex song_selector/a4_half.tex && pdflatex bookletization/booklet_a4_pysty.tex && pdflatex placement/a4_placement.tex && rm *.log *.aux

*Initializing latex from a fresh installation*

- Unpack texlive:
	zcat library/install-tl-unx.tar.gz | tar xf - -C tmp/
- Run installation with profile:
	TEXLIVE_INSTALL_TEXDIR=bin/texlive/2022 TEXLIVE_INSTALL_PREFIX=bin/texlive perl tmp/install-tl-20230115/install-tl -profile texlive.profile

- Initialize tlmgr usertree
	tlmgr init-usertree --usertree library/latex-libraries/

- Install required libraries:
	tlmgr --usertree library/latex-libraries/ --usermode install latex lastpage latexconfig graphics titlesec pgfornament pgfopts tfm texmf texmf-dist palatino mathpazo fpl babel-finnish ulem pgf xcolor float eso-pic pdfpages pdflscape lastpage

- Remove inflated files and tmp folder
