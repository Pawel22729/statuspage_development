#!/usr/bin/python

import requests
import yaml
import os
import time
import threading

def getConfig():
    config = yaml.load(open(os.path.abspath('.')+"/modules/config.yaml"))
    return config

def getTracker():
    conf = getConfig()
    envs = conf['config']['apis']['tracker']['envs']
    lines = []
    for env in envs:
        res = requests.get(envs[env], verify=False)
        y = yaml.load(res.content)
        for k in y.keys():
            line = env+" "+k+" "+str(y[k]['ref']+"\n")
            lines.append(line)

    f = open('/tmp/statusTrackerCache.tmp', 'w')
    for line in lines:
        f.write(str(line))
    f.close()
    return lines

def getSportsbook():
    data = getTracker()
    conf = getConfig()
    envs = conf['config']['apis']['tracker']['envs']
    sportsServ = ["sbw03", "wsc01"]
    versions = {}
    for env in envs:
        versions[env] = []

    for line in data:
        if line.split()[0] in envs and line.split()[1] in sportsServ:
            versions[line.split()[0]].append(line)
        
    return versions

def trackerTimer():
    conf = getConfig()
    timer = conf['config']['apis']['tracker']['tracker_timer']
    while True:
        getTracker()
        time.sleep(timer)

thread = threading.Thread(target=trackerTimer)
#if not threading.enumerate()[1:]:
thread.start()