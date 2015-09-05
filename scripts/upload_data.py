# /usr/bin/python
import os, sys, requests, json, urllib, re, csv
from datetime import datetime
from fabric.api import env, local, run
from fabric.context_managers import lcd

import ckan as ck
env.use_ssh_config = True

#-----------------------------------------------------------------------------#
# Config
#
# Register all files for automatic upload to CKAN here with attributes:
# title - the Resource title
# file - the file path incl. file name relative to this file
# dsid - the CKAN dataset id, under which the file has been uploaded as resource
# rsid - the CKAN resource id of the file
#------------------------------------------------------------------------------#
DC = "http://internal-data.dpaw.wa.gov.au/"
RES = [
  {
    # 14 mile = coral bay
    "title":"NOAA SST and mISST at Coral Bay data",
    "file": "indicators/water_temp/data_CoralBay.csv",
    "dsid":"8a26010a-4be3-462d-adec-56d5d8e65734",
    "resid":"4856e417-f6c4-4b61-887e-536107a91f89"
  },
  {
    # Murat = Ningaloo
    "title":"NOAA SST and mISST at Ningaloo MPA data",
    "file": "indicators/water_temp/data_Ningaloo.csv",
    "dsid":"8a26010a-4be3-462d-adec-56d5d8e65734",
    "resid":"53cb93c3-c2a0-410a-af38-a94e0a74b3f9"
  },
#   {
#     "title":"NOAA SST and mISST at Dampier Archipelago data",
#     "file": "indicators/water_temp/data_DampierArchipelago.csv",
#     "dsid":"",
#     "resid":""
#   },
  {
    "title":"NOAA SST and mISST at Eighty Mile Beach MP data",
    "file": "indicators/water_temp/data_EightyMileBeach.csv",
    "dsid":"10631b53-1b1e-46e9-89fa-0dce756a225b",
    "resid":"d2dcbf39-0c42-4864-93d0-90abd50b6760"
  },
  {
    "title":"NOAA SST and mISST at Jurien Bay MP data",
    "file": "indicators/water_temp/data_JurienBay.csv",
    "dsid":"dea18e2c-a63c-4a2e-820f-ef59751f7efa",
    "resid":"3da1eaa8-e8c1-4fe2-8eb4-70472c3dd33e"
  },
  {
    "title":"NOAA SST and mISST at Marmion MP data",
    "file": "indicators/water_temp/data_Marmion.csv",
    "dsid":"031a7186-2d02-4c47-9151-cdce6d270cd8",
    "resid":"2ad65f43-fe7a-4c8b-b700-3eea2eb95699"
  },
  {
    "title":"NOAA SST and mISST at Montebello Islands MPA data",
    "file": "indicators/water_temp/data_MontebelloIslands.csv",
    "dsid":"d5b39aa7-4a0f-4173-8dfa-164d800ff421",
    "resid":"f4b3ca65-4945-4ef1-9c11-24a9a299ecd2"
  },
  {
    "title":"NOAA SST and mISST at Camden Sound data",
    "file": "indicators/water_temp/data_MontgomeryReef.csv",
    "dsid":"21d57496-7d8f-4eeb-9c55-d0b38c312645",
    "resid":"ccd17e18-ef9f-4509-bd51-8de3988ec6b0"
  },
  {
    "title":"NOAA SST and mISST at Ngari Capes MP data",
    "file": "indicators/water_temp/data_NgariCapes.csv",
    "dsid":"686aea24-2f6d-4abf-916b-2cba0aae5d9c",
    "resid":"2a1b9cbd-d3a6-4fbf-b25b-5428e400d29e"
  },
  {
    "title":"NOAA SST and mISST at Rowley Shoals MP data",
    "file": "indicators/water_temp/data_RowleyShoals.csv",
    "dsid":"bdbfa413-a6e9-4a29-b964-fef095ae3de9",
    "resid":"2f123c1b-6c6f-432d-a0a9-d1b30287604b"
  },
  {
    "title":"NOAA SST and mISST at Shark Bay MPA data",
    "file": "indicators/water_temp/data_SharkBay.csv",
    "dsid":"8680e884-f301-4fae-aac1-6a293207d9a8",
    "resid":"cea2c210-353a-40b4-9093-937002bbca60"
  },
  {
    "title":"NOAA SST and mISST at Shoalwater Islands MP data",
    "file": "indicators/water_temp/data_ShoalwaterIslands.csv",
    "dsid":"c41884df-f464-4d85-bac0-8a5b15473823",
    "resid":"2dec5601-46d5-4169-bfa9-2f771e1d125e"
  }
  # add more datasets here
]
#-----------------------------------------------------------------------------#
# Main routine
#-----------------------------------------------------------------------------#
if __name__ == "__main__":
    """Publish data to data cataloue
    Requires a text file `secret.py` containing `CKAN="your-ckan-api-key"`

    """
    
    d = os.path.dirname(os.path.realpath(__file__))
    
    try:
        from secret import CKAN
    except ImportError:
        print("Authorisation key not found. Follow instructions in "
        "secret.py.template. Skipping upload.")
        sys.exit(0)
    
    print("Uploading Data to {0}".format(DC))
    [ck.resource_update(d, r["resid"], r["file"], api_key=CKAN) for r in RES]

    [ck.set_last_updated_fields(
      ck.package_show(r["dsid"]), 
      api_key=CKAN, 
      lub=os.environ["LOGNAME"], 
      luo=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ) for r in RES]

    print("Successfully uploaded all files to the data catalogue.")
