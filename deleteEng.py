#!/usr/bin/python

import requests as rq
import json
import sys

pToken = ''

def getAvailableRemoteEngines(accessToken = pToken):
    """
    Returns information about available remote engines
    """
    urlRemoteEng = "https://api.eu.cloud.talend.com/tmc/v1.3/runtimes/remote-engines"
    headers = {'Authorization': accessToken, "Content-Type": "application/json", "Accept": "application/json"}
    response = rq.get(url = urlRemoteEng, headers=headers)
    txtResp = response.text
    jsonResp = json.loads(txtResp)
    return jsonResp


def deleteRemoteEngine(name, accessToken = pToken):
    """
    Function for deling engine by name
    @name engine name (same as in TMC) 
    """
    url = "https://api.eu.cloud.talend.com/tmc/v2.6/runtimes/remote-engines"
    engineId = ""
    engines = getAvailableRemoteEngines(pToken)
    headers = {'Authorization': accessToken, "Content-Type": "application/json"}
    for i in engines:
        try:
            if i["name"] == name:
                engineId = i["id"]
        except:
            pass
    endpoint = url + "/" + engineId 
    response = rq.delete(endpoint, headers=headers)
    print(response.text)
    

try:
    engName = sys.argv[1]
    userToken = sys.argv[2]
    pToken = "Bearer " + str(userToken)
    deleteRemoteEngine(name=engName, accessToken=pToken)
except TypeError:
    print("\n Please Check Your Access Token \n")