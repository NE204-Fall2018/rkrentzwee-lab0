# NE 204 Lab 0

This repo contains lab report 0 for NE 204 by Rebecca Krentz-Wee. From a new clone of the repo, run `make all` to download the data, validate the data is correct, run the analysis, and build the report. The finished report is report.pdf.

## Individual make commands

`make data` downloads the data from Dropbox.

`make validate` checks the md5 of the downloaded txt file against the provided md5.

`make analysis` replicates the analysis, producing figures of the gaussian fits of peaks in the calibration data and csv files of the sources used to validate the calibration.

`make test` runs the software test suite.

`make` by itself generates the report
