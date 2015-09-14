#------------------------------------------------------------------------------
# Installation of R packages
#
# Run once on a new server as su
#------------------------------------------------------------------------------

# Shiny: interactive R analyses
# http://rstudio.github.io/shiny/tutorial/
install.packages('bitops')
install.packages('caTools')
install.packages('shiny')

# GGplot: nicer graphs
install.packages('colorspace')
install.packages('RColorBrewer')
install.packages('scales')
install.packages('ggplot2')

# for ckan.R
install.packages('RCurl')
install.packages('rjson')
install.packages('markdown')
install.packages('knitr')
install.packages('stringr')
install.packages('dplyr')
install.packages('httr')

install.packages('devtools')
library(devtools); devtools::install_github('ropensci/ckanr')
