# CKAN o' Sweave
Collaborative, data-driven, reproducible reporting with content from CKAN.

## What?
CKAN o' Sweave is a Sweave document template with hooks to integrate content
(figures and text) from a CKAN data catalogue.

Sweave combines the powerful typesetting markup language Latex with executable 
chunks of R code, a statistical programming language, similar to RMarkdown 
workbooks (combining Markdown with R) or iPython Notebooks (combining Markdown 
with Python).

CKAN o' Sweave uses the R library ckanR to communicate with the CKAN API of any
available CKAN instance. This opens several possibilities:

* embed PDF, JPEG or PNG CKAN resources as figures, and use their description as 
caption;
* open a CSV CKAN resource, analyse it in real-time and embed the results in the
report;
* open a GeoJSONN CKAN resource and embed it as a map in the report.

## Why?

* Latex is a powerful and flexible typesetting language with a vast user base, 
extensive community support, extensible via a plugin system, and being one of 
the oldest software projects around, is nearly bug-free.
* R is the lingua franca of statisticians and data scientists, with a similarly
large user base, abundant community support, also extensible via packages and 
also capable of general purpose programming (system calls, file management, web 
requests).
* CKAN is a wide-spread data cataloguing software and a very capable digital
asset register for data, data processing code, and processing products.

## Usage
Prerequisites: 

* RStudio (Desktop or Server) with Latex and git installed.
* Optional, but desireable: a CKAN with a few figures as PDF resources

Clone this repository using RStudio, open reports/report01.Rnw and hit "Compile PDF".
Read the PDF and the source code for an explanation of the basic structure and 
instructions on how to extend this template into your report.

