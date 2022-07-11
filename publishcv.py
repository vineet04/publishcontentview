#!/usr/bin/python
import sys
import requests
import json
import subprocess
import time
import config

USERNAME=config.username
PASSWORD=config.password
BASEURL=config.url
APIURL="/katello/api/content_views"
RHEL="RHEL_Server_7"
STATE="running"

def publish_rhel7cv():
 URL=BASEURL+APIURL
 # where 'X' represents actual if for RHEL 7 content view
 ID="/katello/api/content_views/X/publish"
 POSTURL=BASEURL+ID
 HEADERS={"Content-Type": "application/json"}

# Publish a content view
 print("\n \t \t Publishing Process of RHEL 7 content view begins...\n")
 r = requests.post(POSTURL, auth=(USERNAME, PASSWORD), headers=HEADERS)
 #print(r.text)

# command to get the last occurrence of content view Publish\
# before entering while loop
 CMD = subprocess.Popen("hammer task list| grep -m1 'Publish content_view'| cut -d'|' -f3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 CMD_OUTPUT = CMD.stdout.read()
 #print(CMD_OUTPUT.strip())
 OUTPUT=CMD_OUTPUT.strip()

 while OUTPUT == STATE:
  print("\n \t \t Publishing RHEL 7 content view still in progress, sleeping for next 1 min...\n")
  CMD = subprocess.Popen("hammer task list| grep -m1 'Publish content_view'| cut -d'|' -f3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  CMD_OUTPUT = CMD.stdout.read()
  OUTPUT=CMD_OUTPUT.strip()
  time.sleep(60)
 else:
   print("\n \t \t Publishing completed, moving to next step...\n")
   response=requests.get(URL, auth=(USERNAME, PASSWORD), headers=HEADERS)
   data=response.json()
#   print(json.dumps(data, indent=4))
   for result in data["results"]:
    #print(result["label"])
     if result["label"] == RHEL:
      version = result["latest_version"]
      print("\n \t \t Printing latest content version going to be referred:")
      print(version)
      for value in result["versions"]:
       if value["version"] == version:
        version_id = value["id"]
        print("\n \t \t Printing latest version id which is going to be used for Promoting environments:")
        print(version_id)
        return promote_test_env(version_id)

def promote_test_env(version_id):
 CV_VERSION_ID=version_id
 #print(CV_VERSION_ID)
 APIURL1="/katello/api/content_view_versions/" + str(CV_VERSION_ID) + "/promote"
 URL=BASEURL+APIURL
 POSTURL=BASEURL+APIURL1
 # Where replace 'X' with actual value of environment ID
 ID=X   
 PARAMS={'environment_ids':ID}
 print("\n \t \t Promoting of Test Env begins...\n")
 HEADERS={"Content-Type": "application/json"}
 r = requests.post(POSTURL, auth=(USERNAME, PASSWORD), params=PARAMS, headers=HEADERS)
 #print(r.text)
 CMD = subprocess.Popen("hammer task list| grep -m1 'Promote content_view'| cut -d'|' -f3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 CMD_OUTPUT = CMD.stdout.read()
 OUTPUT=CMD_OUTPUT.strip()
 while OUTPUT == STATE:
  print("\n \t \t Promoting Test Env still in progress, sleeping for next 30 seconds...\n")
  CMD = subprocess.Popen("hammer task list| grep -m1 'Promote content_view'| cut -d'|' -f3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  CMD_OUTPUT = CMD.stdout.read()
  OUTPUT=CMD_OUTPUT.strip()
  time.sleep(30)
 else:
  print("\n \t \t Promoting of Test Env completed, moving on to Development Env...\n")
  return promote_dev_env(CV_VERSION_ID)



def promote_dev_env(version_id):
 CV_VERSION_ID=version_id
 #print(CV_VERSION_ID)
 APIURL1="/katello/api/content_view_versions/" + str(CV_VERSION_ID) + "/promote"
 URL=BASEURL+APIURL
 POSTURL=BASEURL+APIURL1
 # Where replace 'X' with actual value of environment ID
 ID=X
 PARAMS={'environment_ids':ID}
 print("\n \t \t Promoting of Development Env begins...\n")
 HEADERS={"Content-Type": "application/json"}
 r = requests.post(POSTURL, auth=(USERNAME, PASSWORD), params=PARAMS, headers=HEADERS)
 #print(r.text)
 CMD = subprocess.Popen("hammer task list| grep -m1 'Promote content_view'| cut -d'|' -f3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 CMD_OUTPUT = CMD.stdout.read()
 OUTPUT=CMD_OUTPUT.strip()
 while OUTPUT == STATE:
  print("\n \t \t Promoting Development Env still in progress, sleeping for next 30 seconds...\n")
  CMD = subprocess.Popen("hammer task list| grep -m1 'Promote content_view'| cut -d'|' -f3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  CMD_OUTPUT = CMD.stdout.read()
  OUTPUT=CMD_OUTPUT.strip()
  time.sleep(30)
 else:
  print("\n \t \t Promoting of Development Env completed, moving on to PreProduction Env...\n")
  return promote_preprod_env(CV_VERSION_ID)


def promote_preprod_env(version_id):
 CV_VERSION_ID=version_id
 #print(CV_VERSION_ID)
 APIURL1="/katello/api/content_view_versions/" + str(CV_VERSION_ID) + "/promote"
 URL=BASEURL+APIURL
 POSTURL=BASEURL+APIURL1
 # Where replace 'X' with actual value of environment ID
 ID=
 PARAMS={'environment_ids':ID}
 print("\n \t \t Promoting of PreProduction Env begins...\n")
 HEADERS={"Content-Type": "application/json"}
 r = requests.post(POSTURL, auth=(USERNAME, PASSWORD), params=PARAMS, headers=HEADERS)
 #print(r.text)
 CMD = subprocess.Popen("hammer task list| grep -m1 'Promote content_view'| cut -d'|' -f3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 CMD_OUTPUT = CMD.stdout.read()
 OUTPUT=CMD_OUTPUT.strip()
 while OUTPUT == STATE:
  print("\n \t \t Promoting PreProduction Env still in progress, sleeping for next 30 seconds...\n")
  CMD = subprocess.Popen("hammer task list| grep -m1 'Promote content_view'| cut -d'|' -f3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  CMD_OUTPUT = CMD.stdout.read()
  OUTPUT=CMD_OUTPUT.strip()
  time.sleep(30)
 else:
  print("\n \t \t Promoting of PreProduction Env completed, moving on to Production Env...\n")
  return promote_prod_env(CV_VERSION_ID)

def promote_prod_env(version_id):
 CV_VERSION_ID=version_id
 #print(CV_VERSION_ID)
 APIURL1="/katello/api/content_view_versions/" + str(CV_VERSION_ID) + "/promote"
 URL=BASEURL+APIURL
 POSTURL=BASEURL+APIURL1
 # Where replace 'X' with actual value of environment ID
 ID=X
 PARAMS={'environment_ids':ID}
 print("\n \t \t Promoting of Production Env begins...\n")
 HEADERS={"Content-Type": "application/json"}
 r = requests.post(POSTURL, auth=(USERNAME, PASSWORD), params=PARAMS, headers=HEADERS)
 #print(r.text)
 CMD = subprocess.Popen("hammer task list| grep -m1 'Promote content_view'| cut -d'|' -f3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 CMD_OUTPUT = CMD.stdout.read()
 OUTPUT=CMD_OUTPUT.strip()
 while OUTPUT == STATE:
  print("\n \t \t Promoting Production env still in progress, sleeping for next 30 seconds...\n")
  CMD = subprocess.Popen("hammer task list| grep -m1 'Promote content_view'| cut -d'|' -f3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  CMD_OUTPUT = CMD.stdout.read()
  OUTPUT=CMD_OUTPUT.strip()
  time.sleep(30)
 else:
  print("\n \t \t Promoting of Production Env completed, all Env promoted successfully.\n")


def main():
 publish_rhel7cv()

if __name__=="__main__":
 main()
