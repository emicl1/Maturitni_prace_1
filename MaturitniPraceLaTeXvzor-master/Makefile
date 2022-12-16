#### Makefile for systems using GNU Make

PDFLATEX=pdflatex
BIBTEX=bibtex


VzorMP.pdf: VzorMP.tex VzorMP.bib
	$(PDFLATEX) VzorMP
	$(PDFLATEX) VzorMP

VzorMP.bib: Bibliografie.bib 
	$(PDFLATEX) VzorMP
	$(BIBTEX) VzorMP


clean:
	$(RM) -v VzorMP.aux
	$(RM) -v VzorMP.bbl
	$(RM) -v VzorMP.blg
	$(RM) -v VzorMP.glg
	$(RM) -v VzorMP.glo
	$(RM) -v VzorMP.gls
	$(RM) -v VzorMP.ist
	$(RM) -v VzorMP.lof
	$(RM) -v VzorMP.log
	$(RM) -v VzorMP.lot
	$(RM) -v VzorMP.out
	$(RM) -v VzorMP.run.xml
	$(RM) -v VzorMP.toc
	$(RM) -v VzorMP-blx.bib

mrproper: clean
	$(RM) -v VzorMP.pdf

