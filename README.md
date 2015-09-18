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
#### Use case 4: Annual reporting
A work group of 10 authors has the annual task of annually producing 12 
data-driven reports. About 700 data sets sit as tidy packages of data (XLS or CSV), 
code (SigmaPlot workbooks or R code) and mostly time series figures (PNG, JPEG 
or PDF) in a CKAN catalogue. They are updated as soon as new data comes in - 
some monthly, some quarterly, some annually and some irregularly.

The CKAN datasets have metadata on when and by whom the data was updated last,
as well as the correct attribution of ownership.

Re-creating the same figure just with the latest data point added 700 times gets old
real quick, so all of the XLS/SigmaPlot workflows are migrated to automated R scripts,
which read the data directly from CKAN, produce the time series figure(s) and 
upload the figures and the R code back to CKAN in one go.

The 12 reports consist of about 200 chapters in total, which are updated 
collaboratively at the end of each financial year. Working under version control 
using git involves a learning curve, some moaning and a few (recoverable) hiccups,
but is far more efficient and secure against accidental data loss than 
emailing Word documents in multiple versions. The project is just not big enough
to warrant the branch/pull request work flow, so everyone works on the master branch.
The authors get away with working on the same branch, as they all work on separate
chapters, and run into very few manual merges.

Layouting and publishing the reports went from 6 weeks of manual typesetting 
in the MS Office / email era to a few minutes compiling the 12 PDFs, 
followed by an automated upload to CKAN.

The target audience of the reports can grab the latest copy off CKAN, which includes
the date of publishing, the date each chapter was written/reviewed/edited, and 
underneath each figure, the date that the data shown in that figure was updated,
as well as a link to the dataset on CKAN. This give the readers full, fine-grained
information about the validity and currency of each morsel of information.

The described process is a real-world scenario at the Marine Science Program of 
the Department of Parks and Wildlife of Western Australia. CKAN-o-Sweave was 
reverse engineered from that use case.

### Solution architecture and data flow

* Keeping data, code and figures as datasets on CKAN allows to re-run the code
whenever the data changes to update the data products (e.g. figures).
* Keeping the narrative in the Sweave reports allows to keep the content under
version control, provides an audit trail of authorship and changes, allows
collaborative editing, provides Latex markup (versus the very restrictive 
Markdown markup in CKAN), and de-couples the report structure from CKAN's structure
and organisation of digital content.
* The solution architecture decouples data (data managers and timing of updates) 
from report structure (defined by report editors) 
from report layout (defined in the template)
from report content (written by authors) while providing fine-grained 
permission management.
* Automation speeds up and simplifies the report publishing process, and makes
reports reproducible and the delivered insight defensible.

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


## How?
To compile this template into a PDF, you'll need:

* RStudio IDE (Desktop or Server) with Latex and git installed system-wide.
* The code, figures, maps and anything else you want to use in your reports 
as CKAN resources. The template will compile as-is, its resources already exist.

With these prerequisites:

* Fork this repo into your own GitHub account and copy the clone URL.
* In RStudio, create new project from version control, paste your fork's clone URL.
* One-off, run `scripts/installation.R` to download and install required R packages.
* Open `reports/report01.Rnw`, hit "Compile PDF" to compile the template PDF.

Read the PDF and the source code for an explanation of the basic structure and 
instructions on how to extend this template into your report.

A quick behind-the-scenes run-down:
* The top-level report file links to all content parts: header, front and 
backmatter, and the chapters.
* The Latex header contains the Latex config (packages used, layout settings, 
custom macros for you to use) from both the Legrand Orange book and this template.
* The R code `scripts/ckan.R` provides connectivity to CKAN using the R library ckanR.
* Before you can upload the report to CKAN, you need to copy `scripts/ckan_secret_template.R`
to `scripts/ckan_secret.R` and set your CKAN API key in there. Do not share this file.

## Need help?
As this template mashes up different technologies and languages (R, Latex, 
Python, make, CKAN), there's a multitude of things that can go drastically right 
or drastically wrong.
Should you stub your toes while getting this template to work, please submit an
[issue](https://github.com/datawagovau/ckan-o-sweave/issues).
Any constructive feedback is appreciated, pull requests even more so.
