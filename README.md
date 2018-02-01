# NE 204 Lab 0 

This repo contains lab report 0 for NE 204 by Rebecca Krentz-Wee. It can be built from source  using `make` and `pdflatex` (texlive).

To download the data, run `make data`. To validate that the data is correct, run `make validate`. This checks the md5 of the downloaded file against the provided md5. 

To replicate the analysis, run `make analysis` after downloading the data. This will produce figures of the gaussian fits of peaks in the data,  

Run `make test` to run the software test suite. 

To generate the report, run `make`. 
