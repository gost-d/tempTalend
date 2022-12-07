#!/usr/bin/python

import requests as rq
import json
from datetime import datetime
import sys


pToken = ""


def getWorkSpaceAndEnvIds(env="default", wrkSpaceOwner = "", wrkSpaceName = "", personalToken = pToken):
    """
    Function to get workspace and environment id`s
    @env environment name same as it in a cloud
    @personaToken - personal or service Token as a string
    witn Bearer in the begining
    returns workspaceId, environmentId and information of 
    """
    wrkSpcId = ""
    envId = ""
    envData = ""
    talendWorkspaces = "https://api.eu.cloud.talend.com/orchestration/workspaces"
    headers = {'Authorization': personalToken}
    response = rq.get(talendWorkspaces, headers=headers)
    txtResp = response.text
    jsonResp = json.loads(txtResp)
    for i in jsonResp:
        if i["environment"]["name"] == env and i["owner"] == wrkSpaceOwner and i["name"] == wrkSpaceName:
            wrkSpcId = i["id"]
            envId = i["environment"]["id"]
            envData = i
            break
    if envId == "" or wrkSpcId == "":
        print("No such environment or workspace! Engine Will Not Be Created!")
    else:
        print("Information About Environment \nRemote Engine Will Be On\n")
        print(envData)
    return wrkSpcId, envId


def createRemoteEngine(vmDistribution = 'ubuntu', enableDebugInStudio = True, wrkSpaceOwner = "", wrkSpaceName = "", name="testName", env = "R&D", personalToken = pToken):
    """
    Function creates remote engine at Talend Cloud
    @vmDistribution distribution of virtual machine ubuntu or windows
    @enableDebugInStudio Boolean (True or False) to enables RE to run/debug jobs from Talend Studio
    @name - name of remoteEngine
    @env - environment for remote engine
    @personalToken - personal Token or service acc Token
    in Talend Cloud current datetime added to RE name
    returns pre-authorized key and data about created engine
    """
    urlRemoteEng = "https://api.eu.cloud.talend.com/tmc/v1.3/runtimes/remote-engines"
    tmp = name + str(datetime.now())
    name = tmp.replace(" ", "")
    ids = getWorkSpaceAndEnvIds(env,wrkSpaceOwner, wrkSpaceName, pToken)
    vmPubIp = open('/home/python/' + vmDistribution + 'PublicIP.txt', 'r')
    Ip = vmPubIp.read()

    if enableDebugInStudio == "True":
        payload = {
        "name": name,
        "environmentId": ids[1],  
        "workspaceId":  ids[0],
        "debug": {
        "host": Ip
        },
        "description": "Automatically Created Remote Engine With Debugging Jobs In Studio Option Enabled",
        }

    else:
        payload = {
        "name": name,
        "environmentId": ids[1],  
        "workspaceId":  ids[0]
        }

    headers = {'Authorization': personalToken, "Content-Type": "application/json", "Accept": "application/json"}
    response = rq.post(url = urlRemoteEng, headers=headers, json=payload)
    txtResp = response.text
    jsonResp = json.loads(txtResp)

    print(" \nInformation about newly created Remote Engine \n")
    print(jsonResp)

    return jsonResp["preAuthorizedKey"], jsonResp["name"]


try:
    vmDistribution = sys.argv[1]
    enableDebugInStudio = sys.argv[2]
    env = sys.argv[6]
    workSpaceName = sys.argv[5]
    workSpaceOwner = sys.argv[4]
    pToken = "Bearer " + sys.argv[3]
    name="testName"
    key, engineName = createRemoteEngine(vmDistribution=vmDistribution, enableDebugInStudio=enableDebugInStudio, wrkSpaceName=workSpaceName, wrkSpaceOwner = workSpaceOwner, name=name, env=env, personalToken = pToken)
    with open('/home/python/preauthorized.key.cfg', 'w') as f:
        f.write(key)
except TypeError:
    print("\n Please Check Your Access Token \n")
