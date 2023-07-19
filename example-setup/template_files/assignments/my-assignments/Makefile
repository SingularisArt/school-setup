DOCNAME=master
PDF_VIEWER=zathura

.PHONY:
	clean

all:
	make compile
	make clean

doall:
	make clean compile clean view

compile:
	pdflatex -synctex=1 -shell-escape $(DOCNAME).tex
	pdflatex -synctex=1 -shell-escape $(DOCNAME).tex
	bibtex master
	bibtex master
	pdflatex -synctex=1 -shell-escape $(DOCNAME).tex
	pdflatex -synctex=1 -shell-escape $(DOCNAME).tex

clean:
	rm -rf *.aux *.bcf *.fdb_latexmk *.fls *.log *.out *.toc *.synctex* *.tdo *.loe *.snm *.nav *.auxlock *.bib *.bbl *.blg *.xml *.mtc *.ptc *.mtc0 *.maf

view:
	make compile
	make clean
	$(PDF_VIEWER) $(DOCNAME).pdf
