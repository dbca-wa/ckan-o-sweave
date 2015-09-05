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
	python publish.py
	@echo done!

clean:
	@echo Deleting temporary files...
	rm -fv *-concordance.tex *.synctex.gz *.log *.idx *.ilg *.blg \
	*.ind *.aux *.bcf *.bbl *.out *.toc *.ptc *.run.xml *.pyc *.tex
	@echo done!

# Dependencies: Re-compile the reports only of one of their asset updates changes
# More generic: To get from "XX_PARK.Rnw" to "park":
# echo "99_TEST.Rnw" | cut -d "_" -f 2 | cut -d "." -f 1 | tr '[:upper:]' '[:lower:]'
# returns "test"
01_NKMP.pdf: $(wildcard ./assets/*/nkmp-*.Rnw)
03_LCSMP.pdf: $(wildcard ./assets/*/lcsmp-*.Rnw)
05_EMBMP.pdf: $(wildcard ./assets/*/embmp-*.Rnw)
10_RSMP.pdf: $(wildcard ./assets/*/rsmp-*.Rnw)
20_MBIMPA.pdf: $(wildcard ./assets/*/mbimpa-*.Rnw)
30_NMP.pdf: $(wildcard ./assets/*/nmp-*.Rnw)
40_SBMP.pdf: $(wildcard ./assets/*/sbmp-*.Rnw)
50_JBMP.pdf: $(wildcard ./assets/*/jbmp-*.Rnw)
60_MMP.pdf: $(wildcard ./assets/*/mmp-*.Rnw)
70_SEMP.pdf: $(wildcard ./assets/*/semp-*.Rnw)
80_SIMP.pdf: $(wildcard ./assets/*/simp-*.Rnw)
85_NCMP.pdf: $(wildcard ./assets/*/ncmp-*.Rnw)
90_WNIMP.pdf: $(wildcard ./assets/*/wnimp-*.Rnw)
