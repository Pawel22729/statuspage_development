from flask import Flask, render_template, request
from modules import getStingray, getTracker, getCert

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/status/stingray')
def stingrayStatus():
    data = getStingray.getBuildsHistory()
    return render_template('index.html', data=data)

@app.route('/status/stingray/cache')
def stingrayStatusCache():
    data =  open('/tmp/statusStingrayCache.tmp').readlines()
    return render_template('index.html', data=data)

@app.route('/status/tracker')
def trackerStatus():
    data = getTracker.getTracker()
    return render_template('index.html', data=data)

@app.route('/status/tracker/cache')
def trackerStatusCache():
    data =  open('/tmp/statusTrackerCache.tmp').readlines()
    return render_template('index.html', data=data)

@app.route('/statusall')
def statusall():
    stingrayData =  open('/tmp/statusStingrayCache.tmp').readlines()
    trackerData = open('/tmp/statusTrackerCache.tmp').readlines()
    certsData = getCert.combineData()
    return render_template('statusall.html', stingrayData=stingrayData, trackerData=trackerData, certsData=certsData)

@app.route('/sportsbook')
def sportsbook():
    data = getTracker.getSportsbook()
    return render_template('sportsbook.html', data=data)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
