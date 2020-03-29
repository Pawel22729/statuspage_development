#!/usr/bin/env python3

import requests
import yaml
import json

class Check():
    def __init__(self, *args, **kwargs):
        self.endpoint = kwargs['endpoint']
        with open('endpoints.yml', 'r') as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
        for c in config['endpoints'][self.endpoint]:
            setattr(self, str(c), str(config['endpoints'][self.endpoint][c]))

    def make_check(self):
        """Perform check and assert results based on configuration."""
        is_code_ok, is_string_ok = False, False
        self.check = json.loads(self.check.replace("'", "\""))
        if self.check['type'] == 'http':
            req = requests.get(self.check['endpoint_url'])
            if self.check['expect_codes']:
                if req.status_code in self.check['expect_codes']:
                    is_code_ok = True
            
            if self.check['expect_strings']:
                for expect_string in self.check['expect_strings']:
                    if expect_string in str(req.content):
                       is_string_ok = True

        return (is_code_ok and is_string_ok)
