# /usr/bin/python
import os, sys, requests, json, urllib, re, csv
from datetime import datetime
from fabric.api import env, local, run
from fabric.context_managers import lcd

env.use_ssh_config = True

#-----------------------------------------------------------------------------#
# Settings
#
# Reports were uploaded manually for the first time, resulting resource id
# is used to overwrite existing PDFs with newer versions.
#-----------------------------------------------------------------------------#
DC = "http://catalogue.alpha.data.wa.gov.au/"

#-----------------------------------------------------------------------------#
# CKAN API interaction
#-----------------------------------------------------------------------------#
def package_show(dataset_id, api_url="{0}api/3/action/".format(DC)):
    """
    Return a JSON dictionary of dataset details for a given dataset id.

    :param dataset_id: A CKAN dataset id
    :param api_url: A live CKAN API URL, default: "<DC>/api/3/action/"

    :return: a JSON dictionary of dataset details
    """
    r = requests.get("{0}package_show?id={1}".format(api_url, dataset_id))
    if r.status_code == 200:
      return json.loads(r.content)["result"]
    else:
      return None

def resource_show(resource_id, api_url="{0}api/3/action/".format(DC)):
    """
    Return a JSON dictionary of dataset details for a given dataset id.

    :param dataset_id: A CKAN dataset id
    :param api_url: A live CKAN API URL, default: "<DC>/api/3/action/"

    :return: a JSON dictionary of dataset details
    """
    r = requests.get("{0}resource_show?id={1}".format(api_url, resource_id))
    if r.status_code == 200:
      return json.loads(r.content)["result"]
    else:
      return None

def set_last_updated_fields(dataset_dict, api_url="{0}api/3/action/".format(DC),
    api_key=None, lub="", luo=datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
    """
    Updates a dataset dictionary and posts back to CKAN.

    :param dataset_dict: The dataset as dict from CKAN
    :param api_url: A live CKAN API URL,
    default: "http://internal-data.dpaw.wa.gov.au/api/3/action/"
    :param api_key: A write-privileged CKAN API key
    :param lub: email of person updating
    :param luo: date string of update
    :return: None
    """
    update_url = "{0}package_update".format(api_url)
    headers = {'Authorization': api_key,
        'content-type': 'application/x-www-form-urlencoded'}

    dataset_dict["maintainer"] = lub
    dataset_dict["last_updated_on"] = luo

    # to drop all resources not in REPORTS:
    #dataset_dict["resources"] = [resource_show(x["resid"]) for x in REPORTS]

    datadict = urllib.quote(json.dumps(dataset_dict))
    r = requests.post(update_url, data=datadict, headers=headers)
    print("Setting 'Last updated by (Maintainer)' to "
          "{0}, 'Last updated on' to {1}".format(lub, luo))

def resource_update(filedir, res_id, filepath,
  api_url="{0}api/3/action/".format(DC), api_key=None):
  """
  Update the file attachment of a given resource ID.

  :param res_id: The resource ID of an existing resource
  :param filepath: The path to a local file to be uploaded
  :param api_url: A live CKAN API URL, default: "<DC>/api/3/action/"
  :param api_key: A write-privileged API key (sensitive data)

  :return: None
  """
  res = resource_show(res_id)
  res["state"] = "active"
  res["last_modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  if os.path.isfile(os.path.join(filedir, filepath)):
    r = requests.post("{0}resource_update".format(api_url),
              #data={"id": res_id},
              data=res,
              headers={"Authorization": api_key},
              files=[('upload', file(os.path.join(filedir, filepath)))])
    print("Uploaded {0}".format(filepath))
  else:
    print("File {0} not found, skipping upload".format(filepath))

