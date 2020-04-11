#!/usr/bin/env python3

import yaml
from health_check import Check, check_all
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/status/<endpoint>')
def check_single(endpoint):
    test_result = []
    test_result.append(Check(endpoint=endpoint).check_single())
    return str(test_result)

@app.route('/status/all')
def check_multi():
    test_result = check_all()
    return render_template('index.html', results=test_result) 

if __name__ == "__main__":
    app.run(host='0.0.0.0')