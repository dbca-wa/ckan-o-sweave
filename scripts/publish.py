# /usr/bin/python
from datetime import datetime
import json
import os
import urllib
import requests
import sys

#------------------------------------------------------------------------------#
# CKAN API interaction
#
# This section pre-dates the use of ckanapi and provides comms between
# ckan-o-sweave and a configured CKAN instance.
#------------------------------------------------------------------------------#
def package_show(dataset_id, ckan_url):
    """
    Return a JSON dictionary of dataset details for a given dataset id.

    :param dataset_id: A CKAN dataset id
    :param ckan_url: A live CKAN API URL, default: "<CKAN>/api/3/action/"

    :return: a JSON dictionary of dataset details
    """
    r = requests.get("{0}api/3/action/package_show?id={1}".format(ckan_url,
                                                                  dataset_id))
    if r.status_code == 200:
      return json.loads(r.content)["result"]
    else:
      return None

def resource_show(resource_id, ckan_url):
    """
    Return a JSON dictionary of dataset details for a given dataset id.

    :param dataset_id: A CKAN dataset id
    :param ckan_url: A live CKAN URL

    :return: a JSON dictionary of dataset details
    """
    r = requests.get("{0}api/3/action/resource_show?id={1}".format(ckan_url, resource_id))
    if r.status_code == 200:
      return json.loads(r.content)["result"]
    else:
      return None

def set_last_updated_fields(dataset_dict, ckan_url,
    api_key=None, lub="", luo=datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
    """
    Update a dataset dictionary and posts back to CKAN.

    :param dataset_dict: The dataset as dict from CKAN
    :param ckan_url: A live CKAN API URL
    :param api_key: A write-privileged CKAN API key
    :param lub: email of person updating
    :param luo: date string of update
    :return: None
    """
    update_url = "{0}api/3/action/package_update".format(ckan_url)
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


def resource_update(filedir, res_id, filepath, ckan_url, api_key=None):
  """
  Update the file attachment of a given resource ID.

  :param res_id: The resource ID of an existing resource
  :param filepath: The path to a local file to be uploaded
  :param ckan_url: A live CKAN URL
  :param api_key: A write-privileged API key (sensitive data)

  :return: None
  """
  res = resource_show(res_id, ckan_url)
  res["state"] = "active"
  res["last_modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  if os.path.isfile(os.path.join(filedir, filepath)):
    r = requests.post("{0}resource_update".format(ckan_url),
              #data={"id": res_id},
              data=res,
              headers={"Authorization": api_key},
              files=[('upload', file(os.path.join(filedir, filepath)))])
    print("Uploaded {0}".format(filepath))
  else:
    print("File {0} not found, skipping upload".format(filepath))

## Re-activate deleted resources
#   r = resource_show(res_id)
#   print(res["name"], res["state"])
#   if res["state"] == "deleted":
#     print("Resource marked as deleted: {0}".format(res["name"]))
#     res["state"] = active
#     r = requests.post("{0}resource_update".format(ckan_url),
#               data=res, headers={"Authorization": api_key})
#     print("Resource reactivated: {0}".format(res["name"]))


#------------------------------------------------------------------------------#
# Main routine
#------------------------------------------------------------------------------#
if __name__ == "__main__":
    """
    Publish reports to CKAN
    Requires a text file `ckan_secret.py` based on `ckan_secret_template.py`
    """
    try:
        from ckan_secret import CKAN, API_KEY, PACKAGE_ID, REPORTS
    except ImportError:
        print("CKAN settings not found. Follow instructions in "
        "ckan_secret_template.py. Skipping PDF upload.")
        sys.exit(0)

    d = os.path.abspath(os.path.join(
      os.path.dirname(os.path.realpath(__file__)), '..'))
    print("Working directory is {0}".format(d))

    p = package_show(PACKAGE_ID, CKAN)

    if not p:
        print("Data catalogue not responding, skipping PDF upload.")
        sys.exit(0)

    print("Uploading report PDFs to {0}".format(CKAN))
    me = os.environ["LOGNAME"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    [resource_update(d, r["resid"], r["file"], CKAN, api_key=CKAN) for r in REPORTS]
    set_last_updated_fields(p, CKAN, api_key=CKAN, lub=me, luo=now)

    print("Successfully uploaded all files to the data catalogue.")
