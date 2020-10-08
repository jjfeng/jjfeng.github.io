# First, go to paperpile and get bib files for the preprint and the published manuscripts
# Then run these lines
python3 bib_underliner.py
python3 generate_publications.py
pdflatex cv.tex
bibtex cv.aux
bibtex paper.aux
bibtex preprint.aux
pdflatex cv.tex
pdflatex cv.tex
