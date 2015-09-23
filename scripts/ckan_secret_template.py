#-----------------------------------------------------------------------------#
# Settings
# Rename this file to "secret.py" and DO NOT SHARE
#
# Reports were uploaded manually for the first time, resulting resource id
# is used to overwrite existing PDFs with newer versions.
#-----------------------------------------------------------------------------#

# The CKAN instance where data (figures) come from, and reports are uploaded to
CKAN = "http://catalogue.alpha.data.wa.gov.au/"

# A write-privileged CKAN API key
API_KEY = "your-api-key-goes-here"

# The ID of the CKAN dataset to which reports are uploaded to as resources
PACKAGE_ID = "1c91771c-8103-45db-9d49-47ea3615fffe"

# A list of dicts of report title, local file name and CKAN resource ID
REPORTS = [
  {
    "title":"Example Report",
    "file": "report01.pdf",
    "resid":"caf8062e-668f-4349-8de3-28a7591e7178"
  }
]
# Add resource IDs of your reports to REPORTS and set PACKAGE_ID to the
# package id of the dataset which stores these reports.
