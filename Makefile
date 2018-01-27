manuscript = report
latexopt = -file-line-error -halt-on-error
dataurl = https://www.dropbox.com/s/k692avun0144n90/lab0_spectral_data.txt
datamd5 = https://www.dropbox.com/s/6jquiryg6jskii0/lab0_spectral_data.md5
data = lab0_spectral_data

# Build the PDF of the lab report from the source files
$(manuscript).pdf: $(manuscript).tex text/*.tex references.bib images/*.png
	pdflatex $(latexopt) $(manuscript).tex
	bibtex $(manuscript).aux
	bibtex $(manuscript).aux
	pdflatex $(latexopt) $(manuscript).tex
	pdflatex $(latexopt) $(manuscript).tex

# Get/download necessary data
data :
	[[ -d data ]] || mkdir data 
	cd data/ && wget $(datamd5) $(dataurl)

# Validate that downloaded data is not corrupted
validate :
	cd data/ && cat ${data}.txt | md5sum --check ${data}.md5 

# Run tests on analysis code
test :
	nosetests --no-byte-compile test/*

# Automate running the analysis code
analysis :
	cd code/ && python example.py

clean :
	rm -f *.aux *.log *.bbl *.lof *.lot *.blg *.out *.toc *.run.xml *.bcf
	rm -f text/*.aux
	rm $(manuscript).pdf
	rm code/*.pyc

# Make keyword for commands that don't have dependencies
.PHONY : test data validate analysis clean
