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
* open a GeoJSON CKAN resource and embed it as a map in the report.

## Why?

### Reproducible research
#### Use case 1: Research paper
A researcher writes a publication using CKAN o' Sweave. The publication is a 
live document which links to the utilised data, and embeds the data analysis. 
The data analysis is re-run every time the document is compiled. This makes the
inferred insight defensible, as anyone can reproduce the analysis and will always
come to the same result.

#### Use case 2: Technical document
A data analyst implements a tricky workflow, and combines the code with an 
explanatory narrative. The code itself might be hard to understand, but the narrative
provides enough context so that colleagues will be able to follow, and the 
workflow is documented and preserved.

#### Use case 3: This template
CKAN o' Sweave itself demonstrates its capabilities by embedding live R code
into explanations of what's going on.


### Report automation

### Solution architecture and data flow

* Keeping data, code and figures as datasets on CKAN allows to re-run the code
whenever the data changes to update the data products (e.g. figures).
* Keeping the narrative in the Sweave reports allows to keep the content under
version control, provides an audit trail of authorship and changes, allows
collaborative editing, provides Latex markup (versus the very restrictive 
Markdown markup in CKAN), and de-couples the report structure from CKAN's structure
and organisation of digital content.
* The solution architecture decouples data (and data management) from report 
structure (defined by report editors) form report layout (defined in the template)
from report content (written by authors).
* Automation speeds up and simplifies the report publishing process, and makes
reports reproducible and defensible.

### Choice of technologies

* Latex is a powerful and flexible typesetting language with a vast user base, 
extensive community support, extensible via a plugin system, and being one of 
the oldest software projects around, is nearly bug-free.
* R is the lingua franca of statisticians and data scientists, with a similarly
large user base, abundant community support, also extensible via packages and 
also capable of general purpose programming (system calls, file management, web 
requests).
* CKAN is a wide-spread data cataloguing software and a very capable digital
asset register for data, data processing code, and processing products.
* The Legrand Orange Book latex template provides a well-designed mathematical
report template with a few neat layout tweaks, macros and environments.


## Usage
Prerequisites: 

* RStudio (Desktop or Server) with Latex and git installed.
* Optional, but desireable: a CKAN with a few figures as PDF resources

Clone this repository using RStudio, open reports/report01.Rnw and hit "Compile PDF".
Read the PDF and the source code for an explanation of the basic structure and 
instructions on how to extend this template into your report.

