# The nightbare-fuel below is the Makefile for project "ckan-o-sweave"
# Variables
.SUFFIXES: .Rnw .tex .pdf
.SECONDARY: %.tex
TEX = pdflatex -shell-escape -interaction=nonstopmode -file-line-error
# Add your report filenames (without extension .Rnw) to next line
SRC = report01
PDF = $(SRC:=.pdf)

# Meta-rules: Rnw -> tex; tex -> pdf
.Rnw.tex:
	@echo Running R code chunks in report $< to fetch figures...
	#R CMD Sweave --encoding=utf-8 --options=concordance=TRUE $*.Rnw
	R CMD Sweave --encoding=utf-8 $*.Rnw
	@echo done!

.tex.pdf:
	@echo Typesetting $<...
	$(TEX) $*.tex
	# add bibtex, rerun tex twice
	@echo Compressing $<...
	gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4	-dPDFSETTINGS=/printer \
  -dNOPAUSE -dQUIET -dBATCH -sOutputFile=$*_print.pdf $*.pdf
	@echo    done!

# Make targets
all: clean $(PDF) publish clean

publish:
	@echo Publishing PDFs to data catalog...
	python scripts/publish.py
	@echo done!

clean:
	@echo Deleting temporary files...
	rm -fv *-concordance.tex *.synctex.gz *.log *.idx *.ilg *.blg \
	*.ind *.aux *.bcf *.bbl *.out *.toc *.ptc *.run.xml *.pyc *.tex\
	scripts/*.pyc
	@echo done!

# Dependencies: list chapters for reports, or use wildcards
# This will compile PDFs only for reports with recently modified chapters
report01.pdf: $(wildcard ./chapters/*.Rnw)
