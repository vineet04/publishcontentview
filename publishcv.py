#!/usr/bin/python

#########################################################################
#Script to automatically publish RHEL 7                                 #
#content view and promote each                                          #
#life cycle environment                                                 #
#Author:Vineet Sinha                                                    #
#Modified: 30/08/2022 : Added fix for encryption and check for api call #
#########################################################################

import sys
import requests
import json
import subprocess
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from encrypt import *

# Encryption fix
def check_for_encrypt():
    with open('/home/satellite/scripts/config.py') as r:
         if 'password' in r.read():
             enc()
             print "\n \t \t Config file was not encrypted but now encrypted successfully."
         else:
             print "\n \t \t Config file already encrypted. No action required."
             pass

check_for_encrypt()

from decrypt import *
dec()
print "\n \t \t File decrypted for assigning variables"

# import now config module
import config
username=config.username
password=config.password
BASEURL=config.url

#encrypt config file back
enc()
print "\n \t \t File encrypted back successfully"

APIURL="/katello/api/content_views"
RHEL="RHEL_Server_7"
STATE="running"
exit_code = 1
request_headers = {'Content-Type': 'application/json'}

## api function call
def call_api(request_url,request_type="GET",params=None):
    if request_type == "POST":
       response = requests.post(request_url, auth=(username, password), verify=False, headers=request_headers, params=params)
       if response.ok:
            print "\n \t \t POST api call succeeded"
       else:
            print response.json()
            exit(exit_code)
    else:
       response = requests.get(request_url, auth=(username, password), verify=False)
       if response.ok:
            print "\n \t \t GET api call succeeded"
       else:
            print response.json()
            exit(exit_code)
    return {'data': response.json()}


def publish_rhel7cv():
 ID="/katello/api/content_views/7/publish"
 request_url = BASEURL+ID

# Publish a content view
 print("\n \t \t Publishing Process of RHEL 7 content view begins...\n")
 response = call_api(request_url, "POST")


# command to get the last occurrence of content view Publish\
# before entering while loop
 CMD = subprocess.Popen("hammer task list| grep -m1 'Publish content_view'| cut -d'|' -f3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 CMD_OUTPUT = CMD.stdout.read()
 #print(CMD_OUTPUT.strip())
 OUTPUT=CMD_OUTPUT.strip()

 while OUTPUT == STATE:
  print("\n \t \t Publishing RHEL 7 content view still in progress, please wait...\n")
  CMD = subprocess.Popen("hammer task list| grep -m1 'Publish content_view'| cut -d'|' -f3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  CMD_OUTPUT = CMD.stdout.read()
  OUTPUT=CMD_OUTPUT.strip()
  time.sleep(60)
 else:
   print("\n \t \t Publishing completed, moving to next step...\n")
   request_url = BASEURL+APIURL
   response = call_api(request_url)
   data=response['data']
   for result in data["results"]:
     if result["label"] == RHEL:
      version = result["latest_version"]
      print("\n \t \t Printing latest content version going to be referred:  " + str(version))
      for value in result["versions"]:
       if value["version"] == version:
        version_id = value["id"]
        print("\n \t \t Printing latest version id which is going to be used for Promoting environments:  " + str(version_id))
        return promote_env(version_id)

def get_env_info(ID,COUNTER):
    request_url = BASEURL+APIURL
    response = call_api(request_url)
    data=response['data']
    for result in data["results"]:
     for env in result["environments"]:
      if env["id"] == ID[COUNTER]:
       print("\n \t \t Environment Id is:  " + str(ID[COUNTER]))
       print("\n \t \t Promoting of  "  + env["name"] + "  begins...\n")


def promote_env(version_id):
 CV_VERSION_ID=version_id
 APIURL="/katello/api/content_view_versions/" + str(CV_VERSION_ID) + "/promote"
 ID=[11,12,13,15]
 LEN=len(ID)
 COUNTER=0
 while COUNTER < LEN:
  params = {'environment_ids': ID[COUNTER]}
  get_env_info(ID,COUNTER)
  request_url = BASEURL+APIURL
  r = call_api(request_url, "POST",params)
  print(r['data'])
  CMD = subprocess.Popen("hammer task list| grep -m1 'Promote content_view'| cut -d'|' -f3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  CMD_OUTPUT = CMD.stdout.read()
  OUTPUT=CMD_OUTPUT.strip()
  while OUTPUT == STATE:
   print("\n \t \t Promoting still in progress for current environment, please wait...\n")
   CMD = subprocess.Popen("hammer task list| grep -m1 'Promote content_view'| cut -d'|' -f3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   CMD_OUTPUT = CMD.stdout.read()
   OUTPUT=CMD_OUTPUT.strip()
   time.sleep(30)
  else:
   print("\n \t \t Promoting completed for current environment, moving on to the next environment...\n")
   COUNTER = COUNTER + 1
 else:
   print("\n\n \t \t All environment patched")


def main():
 publish_rhel7cv()

if __name__=="__main__":
 main()
