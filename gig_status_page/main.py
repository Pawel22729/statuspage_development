#!/usr/bin/env python3

import yaml
from health_check import Check
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/status')
def main_status():
    endpoints_list = ['wp_endpoint', 'onet_endpoint']

    live_report = []
    for endpoint in endpoints_list:
        print(endpoint)
        test_result = Check(endpoint=endpoint).make_check()
        live_report.append( { 'name': endpoint, 'result': test_result } )
        
    return render_template('index.html', results=live_report) 

if __name__ == "__main__":
    app.run(host='0.0.0.0')