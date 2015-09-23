library(ckanr)
# Save a copy of this file as "ckan_secret.R" in the same folder.

# Your default CKAN instance. Absolutely no trailing slash allowed.
CKAN = "http://catalogue.alpha.data.wa.gov.au"

# Your write-permitted API key for MY_CKAN_URL
API_KEY = "your-api-key-goes-here"

# A fallback resource ID of an image in MY_CKAN_URL
default_resource_id <- "01a47e8a-313c-4e56-a90f-436172942b99"

# Configure ckanr defaults
ckanr::ckanr_setup(url=CKAN, key=API_KEY)
