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
DC = "http://internal-data.dpaw.wa.gov.au/"

PACKAGE_ID = "0988fd6e-ee4f-47f1-8081-933b71219b51"
REPORTS = [
  {
    "title":"North Kimberley Marine Park",
    "file": "01_NKMP.pdf",
    "resid":"63631108-3d6d-45c7-a2e0-868a8b25ef84"
  }, {
    "title":"Lalang-garram Camden Sound Marine Park",
    "file": "03_LCSMP.pdf",
    "resid":"77dbc720-7df7-4677-9faf-91d54bdd8614"
  }, {
    "title":"Eighty Mile Beach Marine Park",
    "file": "05_EMBMP.pdf",
    "resid":"b7def9cc-9757-4d76-8e1c-65f34253b55a"
  }, {
    "title":"Rowley Shoals Marine Park",
    "file": "10_RSMP.pdf",
    "resid":"f60fe08c-fd2d-40fb-b9b3-bed16b35efe1"
  }, {
    "title":"Montebello Islands Marine Park, Barrow Island Marine Park " + 
            "and Barrow Island Marine Management Area",
    "file": "20_MBIMPA.pdf",
    "resid":"59b3f35d-e055-46b6-a64b-d534c5fd6672"
  }, {
    "title":"Ningaloo Marine Park and Muiron Islands Marine Management Area",
    "file": "30_NMP.pdf",
    "resid":"a5a0b47f-f7c8-42cd-9262-68a23f3b19eb"
  }, {
    "title":"Shark Bay Marine Park and Hamelin Pool Marine Nature Reserve",
    "file": "40_SBMP.pdf",
    "resid":"29f7bf8d-475b-49de-ac08-8294046d410a"
  }, {
    "title":"Jurien Bay Marine Park",
    "file": "50_JBMP.pdf",
    "resid":"ec42c95f-352d-40dd-a434-706e624a67f4"
  }, {
    "title":"Marmion Marine Park",
    "file": "60_MMP.pdf",
    "resid":"7aa99064-c4c9-4249-b2c9-8676ff8abad1"
  }, {
    "title":"Swan Estuary Marine Park",
    "file": "70_SEMP.pdf",
    "resid":"3fba845e-5b51-496b-b915-83e415e4c8ca"
  }, {
    "title":"Shoalwater Islands Marine Park",
    "file": "80_SIMP.pdf",
    "resid":"65d73cbd-0e52-47f1-897d-a6a7b5b70e72"
  }, {
    "title":"Ngari Capes Marine Park",
    "file": "85_NCMP.pdf",
    "resid":"828a10c6-4a7a-45ad-95fa-7fb1e9e79d1d"
  }, {
    "title":"Walpole and Nornalup Inlet Marine Park",
    "file": "90_WNIMP.pdf",
    "resid":"8bf7b060-42f2-44f7-9e27-bea10e3c4083"
  }, {
    "title":"Biodiversity Asset Status Data",
    "file": "cpr.csv",
    "resid":"ece209a7-5974-4e04-9711-ee6457bc4a59"
  }, {
    "title":"Biodiversity Asset Status Overview",
    "file": "cpr.json",
    "resid":"9e8e00b6-3e07-4291-8f89-49b95cc3237e"
  }, {
    "title":"Biodiversity Asset Status Map",
    "file": "cpr.html",
    "resid":"1ae546a8-fea7-4038-8db3-63e49cb1648c"
  }
]

PARKS =  { "type": "FeatureCollection",
    "features": [
  {
        "type": "Feature",
        "geometry": { "type": "Polygon", "coordinates": [ [ 
          [ 124.14415375787712, -15.181391101635331 ], 
          [ 125.05405922357549, -15.13944510498966 ], 
          [ 125.25088274629748, -15.571811531952717 ], 
          [ 125.12827137148706, -15.520185689927278 ], 
          [ 124.99920676642346, -15.545998610939996 ], 
          [ 124.96371400003098, -15.436293696635937 ], 
          [ 124.81206308908125, -15.355628318471188 ], 
          [ 124.7313977109165, -15.487919538661377 ], 
          [ 124.47649511591588, -15.562131686572947 ], 
          [ 124.42164265876386, -16.068710261447574 ], 
          [ 123.74082686705337, -16.068710261447574 ], 
          [ 123.41816535439438, -15.913832735371255 ], 
          [ 124.14415375787712, -15.181391101635331 ] 
          ] ] },
        "properties": {
    "id": "lcsmp",
    "assets": "",
    "title": "Lalang-garram Camden Sound Marine Park",
    "file": "03_LCSMP.pdf",
    "resid": "77dbc720-7df7-4677-9faf-91d54bdd8614",
    "PDF": ("{0}dataset/0988fd6e-ee4f-47f1-8081-933b71219b51/resource/"
    "77dbc720-7df7-4677-9faf-91d54bdd8614/download/03lcsmp.pdf").format(DC)
  }}, {
        "type": "Feature",
        "geometry": { "type": "Polygon", "coordinates": [ [ 
          [ 119.45265536381534, -20.034220252026653 ], 
          [ 119.4623352091951, -19.921288722596003 ], 
          [ 120.56906419761546, -19.711558739367653 ], 
          [ 121.00465723970511, -19.492148910759536 ], 
          [ 121.46283658768088, -19.021063102277399 ], 
          [ 121.55318181122541, -19.040422793036939 ], 
          [ 121.17889445654097, -19.498602141012714 ], 
          [ 120.6239166547675, -19.805130578038764 ], 
          [ 119.77531687647434, -19.989047640254391 ], 
          [ 119.58817319913211, -20.06971301841914 ], 
          [ 119.45265536381534, -20.034220252026653 ] 
          ] ] },
        "properties": {
    "id": "embmp",
    "assets": "",
    "title": "Eighty Mile Beach Marine Park",
    "file": "05_EMBMP.pdf",
    "resid": "b7def9cc-9757-4d76-8e1c-65f34253b55a",
    "PDF": ("{0}dataset/0988fd6e-ee4f-47f1-8081-933b71219b51/resource/"
    "b7def9cc-9757-4d76-8e1c-65f34253b55a/download/05embmp.pdf").format(DC)
  }}, {
        "type": "Feature",
        "geometry": { "type": "Polygon", "coordinates": [ [ 
          [ 119.32681737387836, -17.183505787684503 ], 
        [ 119.41393598229629, -17.19641224819086 ], 
        [ 119.49137474533444, -17.373876080153309 ], 
        [ 118.91381063767486, -17.754616665090918 ], 
        [ 118.76377303428842, -17.543273374299279 ], 
        [ 119.32681737387836, -17.183505787684503 ] 
        ] ] },
        "properties": {
    "id": "rsmp",
    "assets": "",
    "title": "Rowley Shoals Marine Park",
    "file": "10_RSMP.pdf",
    "resid": "f60fe08c-fd2d-40fb-b9b3-bed16b35efe1",
    "PDF": ("{0}dataset/0988fd6e-ee4f-47f1-8081-933b71219b51/resource/"
    "f60fe08c-fd2d-40fb-b9b3-bed16b35efe1/download/10rsmp.pdf").format(DC)
  }}, {
        "type": "Feature",
        "geometry": { "type": "Polygon", "coordinates": [ 
          [ [ 115.46939899004008, -20.293962769717194 ], 
        [ 115.50973167912245, -20.274603078957654 ], 
        [ 115.65170274469241, -20.331068843672977 ], 
        [ 115.71462173966091, -20.518212521015194 ], 
        [ 115.62266320855311, -20.556931902534274 ], 
        [ 115.6258898236797, -20.773115116015802 ], 
        [ 115.57910390434414, -20.78602157652216 ], 
        [ 115.53393129257188, -20.694063045414346 ], 
        [ 115.44681268415395, -20.671476739528217 ], 
        [ 115.32904123203342, -20.826354265604536 ], 
        [ 115.37098722867908, -20.857007109307141 ], 
        [ 115.47423891272996, -20.884433337883156 ], 
        [ 115.54038452282506, -20.86023372443373 ], 
        [ 115.53877121526176, -21.194188390035791 ], 
        [ 115.3968001496918, -21.19741500516238 ], 
        [ 115.32420130934354, -21.094163321111502 ], 
        [ 115.32742792447011, -21.005431405130278 ], 
        [ 115.23385608579902, -20.873140184940091 ],
        [ 115.26612223706491, -20.773115116015802 ], 
        [ 115.26128231437502, -20.739235657186608 ], 
        [ 115.33872107741318, -20.684383200034578 ], 
        [ 115.40486668750827, -20.547252057154505 ], 
        [ 115.38228038162215, -20.50046613781895 ], 
        [ 115.41293322532475, -20.44561368066692 ], 
        [ 115.43713283877418, -20.319775690729912 ], 
        [ 115.46939899004008, -20.293962769717194 ] 
        ] ] },
        "properties": {
    "id": "mbimpa",
    "assets": "",
    "title": ("Montebello Islands Marine Park, Barrow Island Marine Park and "
    "Barrow Island Marine Management Area"),
    "file": "20_MBIMPA.pdf",
    "resid": "59b3f35d-e055-46b6-a64b-d534c5fd6672",
    "PDF": ("{0}dataset/0988fd6e-ee4f-47f1-8081-933b71219b51/resource/"
    "59b3f35d-e055-46b6-a64b-d534c5fd6672/download/20mbimpa.pdf").format(DC)
  }}, {
        "type": "Feature",
        "geometry": { "type": "Polygon", "coordinates": [ [
        [ 114.35460346380319, -21.54104951614417 ], 
        [ 114.47076160836043, -21.628168124562094 ],
        [ 114.45462853272748, -21.763685959878874 ], 
        [ 114.33524377304364, -21.760459344752284 ], 
        [ 114.33847038817024, -21.895977180069064 ], 
        [ 114.12228717468871, -21.895977180069064 ], 
        [ 114.13842025032166, -21.818538417030904 ], 
        [ 114.00612903013148, -21.895977180069064 ], 
        [ 113.69637397797884, -22.592926047412497 ], 
        [ 113.84802488892856, -22.867188333172646 ], 
        [ 113.82866519816902, -23.496378282857691 ], 
        [ 113.64474813595339, -23.648029193807421 ], 
        [ 113.47696414937072, -24.048129469504577 ], 
        [ 113.34144631405394, -24.044902854377987 ], 
        [ 113.52858999139616, -23.589950121528801 ], 
        [ 113.69314736285224, -23.441525825705664 ], 
        [ 113.63829490570022, -23.076918316400995 ], 
        [ 113.6737876720927, -22.993026323109657 ], 
        [ 113.53504322164933, -22.651005119691121 ], 
        [ 113.86093134943492, -21.850804568296805 ], 
        [ 114.35460346380319, -21.54104951614417 ] 
        ] ] },
        "properties": {
    "id": "nmp",
    "assets": "",
    "title": "Ningaloo Marine Park and Muiron Islands Marine Management Area",
    "file": "30_NMP.pdf",
    "resid": "a5a0b47f-f7c8-42cd-9262-68a23f3b19eb",
    "PDF": ("{0}dataset/0988fd6e-ee4f-47f1-8081-933b71219b51/resource/"
    "a5a0b47f-f7c8-42cd-9262-68a23f3b19eb/download/30nmp.pdf").format(DC)
  }}, {
        "type": "Feature",
        "geometry": { "type": "Polygon", "coordinates": [ [ 
          [ 113.56730937291528, -24.916088938557305 ], 
          [ 113.72541351411819, -24.922542168810484 ], 
          [ 114.27393808563848, -25.945379163939499 ],
          [ 114.27071147051188, -26.293853597611218 ], 
          [ 114.12551378981534, -26.484223890080024 ],
          [ 114.01258226038469, -26.406785127041864 ], 
          [ 113.69314736285229, -26.76816602121994 ], 
          [ 113.16075586696495, -26.184148683307157 ],
          [ 112.95102588373659, -25.487199815963727 ],
          [ 113.56730937291528, -24.916088938557305 ] 
          ] ] },
        "properties": {
    "id": "sbmp",
    "assets": "",
    "title": "Shark Bay Marine Park and Hamelin Pool Marine Nature Reserve",
    "file": "40_SBMP.pdf",
    "resid": "29f7bf8d-475b-49de-ac08-8294046d410a",
    "PDF": ("{0}dataset/0988fd6e-ee4f-47f1-8081-933b71219b51/resource/"
    "29f7bf8d-475b-49de-ac08-8294046d410a/download/40sbmp.pdf").format(DC)
  }}, {
        "type": "Feature",
        "geometry": { "type": "Polygon", "coordinates": [ [ 
          [ 114.98702002861485, -30.062540065468301 ], 
          [ 115.04025917820358, -30.235163974740864 ], 
          [ 115.08865840510244, -30.482000031924997 ], 
          [ 115.24353593117876, -30.849834156356255 ], 
          [ 115.12737778662151, -30.849834156356255 ], 
          [ 114.95636718491224, -30.551372257146681 ], 
          [ 114.93216757146281, -30.459413726038868 ], 
          [ 114.86602196136772, -30.062540065468301 ], 
          [ 114.98702002861485, -30.062540065468301 ] 
          ] ] },
        "properties": {
    "id": "jbmp",
    "assets": "",
    "title": "Jurien Bay Marine Park",
    "file": "50_JBMP.pdf",
    "resid": "ec42c95f-352d-40dd-a434-706e624a67f4",
    "PDF": ("{0}dataset/0988fd6e-ee4f-47f1-8081-933b71219b51/resource/"
    "ec42c95f-352d-40dd-a434-706e624a67f4/download/50jbmp.pdf").format(DC)
  }}, {
        "type": "Feature",
        "geometry": { "type": "Polygon", "coordinates": [ [ 
          [ 115.65250939847394, -31.721020240535562 ], 
          [ 115.71865500856903, -31.721020240535562 ], 
          [ 115.75414777496152, -31.835565077529505 ], 
          [ 115.75495442874316, -31.875897766611882 ], 
          [ 115.6944553951196, -31.878317727956823 ],
          [ 115.65250939847394, -31.721020240535562 ] 
          ] ] },
        "properties": {
    "id": "mmp",
    "assets": "",
    "title": "Marmion Marine Park",
    "file": "60_MMP.pdf",
    "resid": "7aa99064-c4c9-4249-b2c9-8676ff8abad1",
    "PDF": ("{0}dataset/0988fd6e-ee4f-47f1-8081-933b71219b51/resource/"
    "7aa99064-c4c9-4249-b2c9-8676ff8abad1/download/60mmp.pdf").format(DC)
  }}, {
        "type": "Feature",
        "geometry": { "type": "Polygon", "coordinates": [ [ 
          [ 115.82029338505662, -31.986006007806768 ], 
          [ 115.84771961363263, -31.973502874191233 ], 
          [ 115.85376951699499, -31.988022642260887 ], 
          [ 115.83118321110886, -32.019078812854318 ], 
          [ 115.81343682791261, -32.030775292688205 ], 
          [ 115.79407713715308, -32.015448870836906 ], 
          [ 115.82029338505662, -31.986006007806768 ] 
          ] ] },
        "properties": {
    "id": "semp",
    "assets": "",
    "title": "Swan Estuary Marine Park",
    "file": "70_SEMP.pdf",
    "resid": "3fba845e-5b51-496b-b915-83e415e4c8ca",
    "PDF": ("{0}dataset/0988fd6e-ee4f-47f1-8081-933b71219b51/resource/"
    "3fba845e-5b51-496b-b915-83e415e4c8ca/download/70semp.pdf").format(DC)
  }}, {
        "type": "Feature",
        "geometry": { "type": "Polygon", "coordinates": [ [ 
          [ 115.66622251276195, -32.262284928021039 ],
          [ 115.66823914721607, -32.259461639785272 ], 
          [ 115.70131195226362, -32.244941871715618 ],
          [ 115.70695852873516, -32.248975140623855 ], 
          [ 115.70252193293609, -32.27075479272834 ],
          [ 115.70494189428103, -32.302617617103415 ], 
          [ 115.72793152705799, -32.305844232230008 ], 
          [ 115.73882135311023, -32.314717423828128 ], 
          [ 115.74608123714505, -32.333270460806027 ],
          [ 115.74366127580011, -32.355050112910504 ], 
          [ 115.72188162369562, -32.377636418796634 ], 
          [ 115.6670291665436, -32.377233091905815 ], 
          [ 115.66622251276195, -32.262284928021039 ] 
          ] ] },
        "properties": {
    "id": "simp",
    "assets": "",
    "title": "Shoalwater Islands Marine Park",
    "file": "80_SIMP.pdf",
    "resid": "65d73cbd-0e52-47f1-897d-a6a7b5b70e72",
    "PDF": ("{0}dataset/0988fd6e-ee4f-47f1-8081-933b71219b51/resource/"
    "65d73cbd-0e52-47f1-897d-a6a7b5b70e72/download/80simp.pdf").format(DC)
  }}, {
        "type": "Feature",
        "geometry": { "type": "Polygon", "coordinates": [ [ 
          [ 115.40930328330724, -33.529134692098488 ], 
          [ 115.47867550852892, -33.588827071940401 ],
          [ 115.29637175387658, -33.674332372795043 ], 
          [ 115.13181438242049, -33.646906144219024 ], 
          [ 115.02372277567972, -33.550107690421321 ], 
          [ 115.04146915887596, -33.633999683712666 ], 
          [ 115.00920300761005, -33.813076823238418 ],
          [ 115.04469577400255, -34.234150097258429 ], 
          [ 115.14956076561673, -34.348694934252379 ],
          [ 115.17698699419275, -34.306748937606706 ], 
          [ 115.2899185236234, -34.297069092226934 ], 
          [ 115.28830521606011, -34.453559925866557 ], 
          [ 115.16085391855979, -34.49066599982234 ],
          [ 115.01565623786324, -34.385801008208162 ], 
          [ 114.93176424457189, -34.298682399790231 ],
          [ 114.88820494036293, -33.82436997618148 ], 
          [ 114.93337755213518, -33.471055619819865 ], 
          [ 115.07696192526845, -33.471055619819865 ], 
          [ 115.18182691688263, -33.569467381180864 ],
          [ 115.30766490681964, -33.574307303870746 ], 
          [ 115.40930328330724, -33.529134692098488 ] 
          ] ] },
        "properties": {
    "id": "ncmp",
    "assets": "",
    "title": "Ngari Capes Marine Park",
    "file": "85_NCMP.pdf",
    "resid": "828a10c6-4a7a-45ad-95fa-7fb1e9e79d1d",
    "PDF": ("{0}dataset/0988fd6e-ee4f-47f1-8081-933b71219b51/resource/"
    "828a10c6-4a7a-45ad-95fa-7fb1e9e79d1d/download/85ncmp.pdf").format(DC)
  }}, {
        "type": "Feature",
        "geometry": { "type": "Polygon", "coordinates": [[ 
        [ 116.72535892806518, -34.972843297802164 ], 
        [ 116.76246500202096, -34.997042911251583 ], 
        [ 116.80622596967534, -34.99845455536947 ], 
        [ 116.81530082471888, -34.979699854946162 ], 
        [ 116.79876442219511, -34.970221673011807 ], 
        [ 116.80279769110334, -34.966995057885214 ], 
        [ 116.82719896799817, -34.979296528055343 ], 
        [ 116.81590581505512, -35.003294478059352 ], 
        [ 116.78968956715157, -35.008739391085477 ], 
        [ 116.75702008899485, -35.003697804950178 ], 
        [ 116.74169366714354, -35.030720706635371 ], 
        [ 116.73544210033577, -35.034148985207374 ], 
        [ 116.69813436293458, -35.014385967557011 ], 
        [ 116.6951094112534, -35.007932737303825 ], 
        [ 116.64469354990042, -35.010352698648774 ], 
        [ 116.64166859821925, -35.004907785622649 ],
        [ 116.69329444024469, -34.999261209151115 ], 
        [ 116.71971235159364, -34.991799661670875 ], 
        [ 116.71547741924, -34.980103181836988 ], 
        [ 116.72535892806518, -34.972843297802164 ] 
        ] ] },
        "properties": {
    "id": "wnimp",
    "assets": "",
    "title": "Walpole and Nornalup Inlet Marine Park",
    "file": "90_WNIMP.pdf",
    "resid": "8bf7b060-42f2-44f7-9e27-bea10e3c4083",
    "PDF": ("{0}dataset/0988fd6e-ee4f-47f1-8081-933b71219b51/resource/"
    "d95f7045-1f06-4043-853b-d7ecc3c72be1/download/90wnimp.pdf").format(DC)
  }}
]}


#-----------------------------------------------------------------------------#
# CKAN API interaction
#-----------------------------------------------------------------------------#
def package_show(dataset_id, api_url="{0}api/3/action/".format(DC)):
    """Return a JSON dictionary of dataset details for a given dataset id.

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
    """Return a JSON dictionary of dataset details for a given dataset id.

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
    """Updates a dataset dictionary and posts back to CKAN.

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
  """Update the file attachment of a given resource ID.

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
    
#   r = resource_show(res_id)
#   print(res["name"], res["state"])
#   if res["state"] == "deleted":
#     print("Resource marked as deleted: {0}".format(res["name"]))
#     res["state"] = active
#     r = requests.post("{0}resource_update".format(api_url),
#               data=res, headers={"Authorization": api_key})
#     print("Resource reactivated: {0}".format(res["name"]))

#------------------------------------------------------------------------------#
# Local post-processing
#------------------------------------------------------------------------------#
def extract_cpr(filedir):
  """Extracts CPR status from MPA reports into CSV file.
  
  Extracts marine park and asset slugs from filename (excl. chapter templates);
  extracts CPR metrics from \cpr{}{}{}{}{}{} macro (excluding examples).
  
  Will pull in multiple lines if multiple \cpr macros occur.
  """
  macro = re.compile(r"^\\\w+\{(?P<c>(.)*)\}\{(?P<cc>.)\}\{(?P<p>.)\}" +
                     r"\{(?P<pc>.)\}\{(?P<d>.)\}")
  template = re.compile(r"template")
  asset = re.compile(r"(?P<park>\w+)-(?P<asset>\w+)\.\w+")

  with open(os.path.join(filedir, 'cpr.csv'), 'wb') as out_f:
    writer = csv.writer(out_f)    
    writer.writerow(["park", "asset", "condition", "cconf", 
    "pressure", "pconf", "data"])
    
    for root, path, files in os.walk(os.path.join(filedir, "./assets")):
      for file in files:
        if not template.match(file):
          with open(os.path.join(root, file)) as f:
            a = asset.match(file)
            for line in f:
              m = macro.match(line)
              if m:
                writer.writerow([a.group("park"), a.group("asset"), 
                m.group("c"), m.group("cc"), m.group("p"), 
                m.group("pc"), m.group("d")])
         
def getCprDict(filedir):
  with open(os.path.join(filedir, 'cpr.csv'), 'rb') as cpr_f:
      cpr = csv.DictReader(cpr_f)
      return [x for x in cpr]
    
condMap = {
          "++" : "success",
          "+" : "success",
          "0" : "default",
          "-": "warning",
          "--": "danger"
          }         
trendMap = {
    "+":"glyphicon glyphicon-arrow-down",
    "0":"glyphicon glyphicon-arrow-right",
    "-":"glyphicon glyphicon-arrow-up",
}

confMap = {
    "+":"glyphicon glyphicon-thumbs-up",
    "0":"glyphicon glyphicon-hand-right",
    "-":"glyphicon glyphicon-thumbs-down"
}
dataMap = {
           "+": "",
           "-": ' <div class="label label-info label-xs">D <span ' +\
           'class="glyphicon glyphicon-warning-sign"></span></div>'
           }
    
def makeHTML(a, c, cc, p, pc, pt, d):
    html = """
    <div class="row"><div class="col-md-12"><strong>{0}</strong></div></div>
    <div class="row"><div class="col-md-12">
    <div class="label label-xs label-{1}">C <span class="{2}"></span></div>
    <div class="label label-xs label-{3}">P <span class="{4}"></span></div>
    <div class="label label-xs label-{5}">T <span class="{6}"></span></div>{7}
    </div></div>""".format(a.title().replace("_", " "), 
    condMap[c], confMap[cc], condMap[p], confMap[pc], 
    condMap[pt], trendMap[pt], dataMap[d])
    return html

def makeAssetHtml(parkname, parktitle, pdf, cpr):
    html = '''<h3>{0}</h3>
    <a href="{1}" target="_" class="btn btn-danger btn-xs">
    PDF (Updated on {2})</a>{3}
    '''.format(
      parktitle, pdf, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      ' '.join(
          [makeHTML(x["asset"], x["condition"], x["cconf"], 
          x["pressure"], x["pconf"], x["ptrend"], x["data"]) 
          for x in cpr if x['park']==parkname]
        )
      )
    return html
    
def writeAssets(filedir):
    cpr = getCprDict(filedir)
    for x in PARKS["features"]:
        x["properties"]["assets"] = makeAssetHtml(x["properties"]["id"], 
            x["properties"]["title"], x["properties"]["PDF"], cpr)

    with open(os.path.join(filedir, 'cpr.json'), 'w') as outfile:
        json.dump(PARKS, outfile)
        
def refresh_cpr_csv(filedir, api_url="{0}api/3/action/".format(DC), api_key=None):
  """Refreshes and uploads CPR overview CSV to data catalog
  
  Call this before compiling PDFs if CPR assessments have changed.
  """
  extract_cpr(filedir)
  resource_update(filedir, "ece209a7-5974-4e04-9711-ee6457bc4a59", "cpr.csv", 
    api_url=api_url, api_key=api_key)
  

#------------------------------------------------------------------------------#
# Build automation: Compile PDFs
#------------------------------------------------------------------------------#
def sweaveOne(filepath, filename):
  """Sweave one Rnw file at filepath into a PDF.
  """
  refresh_cpr_csv(filepath)
  with lcd(filepath):
    print("Sweaving {0}...".format(filename))
    local("R CMD Sweave --encoding=utf-8 {0}.Rnw".format(filename))
    local("pdflatex {0}.tex".format(filename))
    print("Done, written {0}.pdf".format(filename))

def sweaveEmAll(filepath, geojson):
  """From a GeoJSON of features with at least the property "file" containing
  the PDF filename of a Rnw file, call sweaveOne on each file.
  """
  for feature in geojson["features"]:
    fn = feature["properties"]["file"].strip(".pdf")
    sweaveOne(filepath, fn)
  

#-----------------------------------------------------------------------------#
# Main routine
#-----------------------------------------------------------------------------#
if __name__ == "__main__":
    """Publish reports to DC/dataset/mpa-reports
    Requires a text file `secret.py` containing `CKAN="your-ckan-api-key"`

    TODO: compile PDFs twice
    TODO: delete temp files
    TODO: compress PDFs to /prepress before upload
    """
    
    d = os.path.dirname(os.path.realpath(__file__))

#     sweaveOne(d, "01_NKMP")
#     sweaveOne(d, "03_LCSMP")
#     sweaveOne(d, "05_EMBMP")
    
#     sweaveEmAll(d, PARKS)
    
#     print("Extracting CPR status from reports...")
#     extract_cpr(d)
    
#     print("Writing CPR status summary...")
#     writeAssets(d)
    
    try:
        from secret import CKAN
    except ImportError:
        print("Authorisation key not found. Follow instructions in "
        "secret.py.template. Skipping PDF upload.")
        sys.exit(0)
    
    p = package_show(PACKAGE_ID);

    if not p:
        print("Data catalog not responding, skipping PDF upload.")
        sys.exit(0)
    
    print("Uploading report PDFs to {0}dataset/mpa-reports".format(DC))
    [resource_update(d, r["resid"], r["file"], api_key=CKAN) for r in REPORTS]

    set_last_updated_fields(p, api_key=CKAN, lub=os.environ["LOGNAME"],
        luo=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    print("Successfully uploaded all files to the data catalog.")
