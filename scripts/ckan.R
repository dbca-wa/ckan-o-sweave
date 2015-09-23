#' R functions to retrieve content from CKAN
#'
#' Source "ckan_secret.R" before sourcing this file
#'
#' @author Florian.Mayer@dpaw.wa.gov.au
#'
require(ckanr)
require(ggplot2)
require(Hmisc)
require(knitr)
require(lubridate)
require(markdown)
require(RCurl)
require(rjson)
require(scales)

#' Texify a string of text
#'
#' Substitutes special characters with their Latex counterpart.
#'
#' @param text A string of text to be substituted.
#' @return The input text after substitution.
#' @import Hmisc
#' @export
#' @usage
#' texify("Testing % ~ $ & _ m2 sqm mL-1 L-1 < > ≥ ≤ °")
texify <- function(text){
  text = gsub("%", "\\\\%", text)
  text = gsub("~", "\\\\~", text)
  #text = gsub("$", "\\\\$", text)
  text = gsub("&", "\\\\&", text)
  text = gsub("_", " ", text)
  text = gsub("R2", "$R^2$", text)
  text = gsub("m2", "$m^2$", text)
  text = gsub("m-2", "$m^-2$", text)
  text = gsub("sqm ", "$m^2$ ", text)
  text = gsub(" mL-1 ", " $mL^{-1}$ ", text)
  text = gsub(" L-1 ", " $L^{-1}$ ", text)
  text = gsub("<", "$<$", text)
  text = gsub(">", "$>$", text)
  text = gsub("≥", "$\\\\geq$", text)
  text = gsub("≤", "$\\\\leq$", text)
  text = gsub("±", "$\\\\pm$", text)
  text = gsub("+/-", "$\\\\pm$", text)
  text = gsub("=", "$=$", text)
  text = gsub("°", "$\\\\textdegree$", text)

  # add more substitutions as required
  return(Hmisc::escapeBS(text))
}

#' Return the value of a key in a dictionary or display a "missing" message
#'
#' @param dict A dictionary, as returned by ckanr::package_show
#' @param key A key as quoted string
#' @param texify Whether to convert the value from markdown to latex (default: F)
get_key <- function(dict, key, texify=F){
  val = dict[[key]]
  if (is.null(val)) {
    val = "not available"
    print(paste("Missing key:", key, "at", dict$url))
  }
  if (texify==T){ val <- texify(val)}
  val
}

#' Return a named list of metadata of a CKAN resource and its dataset
#'
#' Onto a named list containing CKAN API's resource_show() response result,
#' various useful bits are added, such as the resource's package_show result,
#' as well as vigorously abbreviated important bits of metadata used in
#' Latex macros.
#'
#' @param resource_id An existing CKAN resource id
#' @param url The base url of the resource's CKAN catalogue,
#'  optional, default: configured ckanr default
#' @return A named list containing resource and dataset metadata:
#'  top level:
#'    23 default `ckanr::resource_show` keys
#'    d (containing 34 default `ckanr::package_show` keys)
#'    ind - the dataset's title (heading, texified)
#'    syn - the dataset's description (synopsis, texified)
#'    pth - the local file path if the url is downloaded with wget
#'    cap - the resource's description (caption, texified)
#'    ori - the dataset's url
#'    src - the dataset's extra field "citation", texified
#'    luo <- the dataset's "last updated on"
#'    lub <- the dataset's maintainer (last updated by)
#'
ckan_res <- function(resource_id,
                     url = ckanr::get_default_url()){
  if (resource_id == "") resource_id <- default_resource_id
  r <- ckanr::resource_show(resource_id, url = url)
  d <- ckanr::package_show(r$package_id, url = url)
  r$d <- d
  r$ind <- texify(d$title)
  r$syn <- texify(d$notes)
  r$pth <- strsplit(r$url, "//")[[1]][2]
  r$cap <- texify(r$description)
  r$ori <- paste(url, "dataset", d$id, sep="/")
  r$src <- get_key(d, "citation", texify=T)
  r$luo <- get_key(d, "last_updated_on")
  r$lub <- d$maintainer
  r
}

#' Load a CSV from a URL, parse nominated date columns as dates
#'
#' @param url The URL of a CSV file
#' @param date_colnames The column names of date columns, default:
#'    'date', 'Date', date.start', 'date.end', 'year', 'Year'
#' @param date_formats The date formats to expect, default:
#'    'YmdHMSz', 'YmdHMS','Ymd','dmY', 'Y'
#' @param timezone The timezone, default: 'Australia/Perth'
#' @return A data.frame of the CSV, with parsed dates and strings as factors
load_csv <- function(url,
                     date_colnames = c('date', 'Date',
                                       'date.start', 'date.end',
                                       'start.date','end.date',
                                       'year', 'Year'),
                     date_formats = c('YmdHMSz', 'YmdHMS','Ymd','dmY', 'Y'),
                     timezone = 'Australia/Perth'){
  df <-read.csv(url, as.is = F)
  cn <- names(df)
  df[cn %in% date_colnames] <- lapply(
    df[cn %in% date_colnames],
    function(x){x<- lubridate::parse_date_time(x,
                                               orders = date_formats,
                                               tz = timezone)}
  )
  names(df) <- Hmisc::capitalize(names(df))
  df
}

#' Load CSV from CKAN given a resource id
#'
#' @param res_id The resource id of a CKAN CSV resource
#' @param ckanurl The base url of the CKAN catalogue, default: ckanr::get_default_url()
#' @param parse_dates Whether to parse date_colnames as dates of format date_formats
#'    into PosixCt
#' @param date_colnames The column names of date columns, default: 'date', 'Date',
#'    'date.start', 'date.end', 'year', 'Year'
#' @param date_formats The date formats to expect, default: 'YmdHMSz', 'YmdHMS','Ymd','dmY', 'Y'
#' @param timezone The timezone, default: 'Australia/Perth'
#' @return A data.frame of the CSV, with parsed dates and strings as factors
load_ckan_csv <- function(res_id,
                          ckanurl = ckanr::get_default_url(),
                          parse_dates = T,
                          date_colnames = c('date', 'Date',
                                            'date.start', 'date.end',
                                            'start.date','end.date',
                                            'year', 'Year'),
                          date_formats = c('YmdHMSz', 'YmdHMS','Ymd','dmY', 'Y'),
                          timezone = 'Australia/Perth'){
  r <- ckan_res(res_id, url = ckanurl)
  df <- load_csv(r$url,
                 date_colnames = date_colnames,
                 date_formats = date_formats,
                 timezone = timezone)
  df
}
