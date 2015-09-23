# The nightbare-fuel below is the Makefile for project "mpa-reports"
# Variables
.SUFFIXES: .Rnw .tex .pdf
.SECONDARY: %.tex
TEX = pdflatex -shell-escape -interaction=nonstopmode -file-line-error
SRC = 01_NKMP 03_LCSMP 05_EMBMP 10_RSMP 20_MBIMPA 30_NMP 40_SBMP 50_JBMP \
	60_MMP 70_SEMP 80_SIMP 85_NCMP 90_WNIMP
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
	@echo    done!
	# PDF compression not required, as all graphics vector or optimized raster
	#gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dUseCIEColor \
	#-dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH -sOutputFile=$*_print.pdf $*.pdf

# Make targets
#all: clean $(PDF) clean publish
all: clean publish

publish:
	@echo Publishing PDFs to data catalog...
	python scripts/publish.py
	@echo done!

clean:
	@echo Deleting temporary files...
	rm -fv *-concordance.tex *.synctex.gz *.log *.idx *.ilg *.blg \
	*.ind *.aux *.bcf *.bbl *.out *.toc *.ptc *.run.xml *.pyc *.tex
	@echo done!
