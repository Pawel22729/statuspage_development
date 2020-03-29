#!/usr/bin/python

import yaml
import requests
import yaml
import json
import os
import time
import threading

def getConfig():
    config = yaml.load(open(os.path.abspath('.')+"/modules/config.yaml"))
    return config

def getBuilds():
    conf = getConfig()
    url = conf['config']['apis']['jenkins']['wendy_scripts']
    req = requests.get(url, verify=False)
    buildList = json.loads(req.content.decode("utf-8"))['builds']
    return buildList

def getBuildInfo(buildDict):
    buildJson = json.loads(buildDict.decode('utf-8'))
    buildLog = {}
    buildLog[buildJson['timestamp']] = buildJson['displayName'].split()[2:]
    return buildLog

def getBuildsHistory():
    buildList = getBuilds()
    buildLog = []
    session = requests.Session()
    for build in buildList:
        req = session.get(build['url']+"api/json?pretty=true", verify=False)
        line = getBuildInfo(req.content)
        buildLog.append(line)
    
    f = open('/tmp/statusStingrayCache.tmp', 'w')
    for line in buildLog:
        f.write(str(line)+'\n')
    f.close()
    return buildLog

def jenkinsTimer():
    conf = getConfig()
    timer = conf['config']['apis']['jenkins']['jenkins_timer']
    while True:
        getBuildsHistory()
        time.sleep(timer)

thread = threading.Thread(target=jenkinsTimer)
#if not threading.enumerate()[1:]:
thread.start()