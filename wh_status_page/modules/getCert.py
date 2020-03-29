#!/usr/bin/env python

import os
import yaml
from OpenSSL import crypto

def getConfig():
    config = yaml.load(open(os.path.abspath('.')+"/modules/config.yaml"))
    return config

def findCerts():
    conf = getConfig()
    certs = []
    where = conf['config']['apis']['certs']['certs_path']
    what = conf['config']['apis']['certs']['certs_exten']
    for r, d, f in os.walk(where):
        for name in f:
            if name.endswith(what): 
                certs.append(os.path.join(r, name))
    return certs

def certData(cert):
    cert_data = []
    crt = crypto.load_certificate(crypto.FILETYPE_PEM, open(cert).read())
    expire_date = crt.get_notAfter().decode('utf-8')
    expire_date = expire_date[:4]+"/"+expire_date[4:6]+"/"+expire_date[6:8]+" "+expire_date[8:10]+":"+expire_date[10:12]
    issuer = crt.get_issuer().get_components()
    for i in issuer:
        cert_data.append(i[0].decode('utf-8')+" "+i[1].decode('utf-8'))
    cert_data.append(expire_date)
    return cert_data

def combineData():
    certs = findCerts()
    results = {}
    for c in certs:
        cert_data = certData(c)
        results[' '.join(c.split('/')[-2:])] = cert_data
    return results