#!/usr/bin/env python3

import requests
import yaml
import json
import logging

logger = logging.getLogger('my_healthcheck_app')
logger.setLevel(logging.DEBUG)

class Check():
    def __init__(self, *args, **kwargs):
        self.endpoint = kwargs['endpoint']
        with open('endpoints.yml', 'r') as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
        for c in config['endpoints'][self.endpoint]:
            setattr(self, str(c), str(config['endpoints'][self.endpoint][c]))

    def check_single(self):
        """Perform check and assert results based on configuration."""
        is_alive = {
            'endpoint_name': self.endpoint,
            'is_alive': 'no'
        }
        self.check = json.loads(self.check.replace("'", "\""))
        if self.check['type'] == 'http':
            req = requests.get(self.check['endpoint_url'])
            if self.check['expect_codes']:
                if req.status_code in self.check['expect_codes']:
                    is_alive['is_alive'] = 'yes'
                else:
                    is_alive['is_alive'] = 'no'  
            
            if self.check['expect_strings']:
                for expect_string in self.check['expect_strings']:
                    if expect_string in str(req.content):
                        is_alive['is_alive'] = 'yes'
                    else:
                        is_alive['is_alive'] = 'no'

        elif self.check['ping']:
            pass                   

        return json.dumps(is_alive)

    
def check_all():
    results = []
    with open('endpoints.yml', 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    for e in config['endpoints']:
        result = Check(endpoint=e).check_single()
        results.append(result)
    return results