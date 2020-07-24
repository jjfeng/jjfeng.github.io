# First, go to paperpile and get bib files for the preprint and the published manuscripts
# Then run these lines
python bib_underliner.py
pdflatex cv.tex
bibtex cv.aux
bibtex paper.aux
bibtex preprint.aux
pdflatex cv.tex
pdflatex cv.tex
