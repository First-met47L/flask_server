from urllib import parse

import json
import requests
from flask import Flask
from wechatVerify import wechatVerify

app = Flask(__name__)


@app.route('/')
def helloWorld():
    return 'Hello World!'


@app.route('/spider/exec/<string:name>')  # <string:name> convert string
def add(name):
    data = dict(project='xyh_magazine', spider=name)
    res = requests.post('http://localhost:6800/schedule.json', data=data)
    resDict = json.loads(res.text)
    resDict.pop('node_name')
    resDict['name'] = name
    return json.dumps(resDict)


@app.route('/wechat/email/verify/<string:url>')
def verify(url):
    result = wechatVerify().execute(url=url)
    if result:
        data = dict(project='xyh_magazine', spider='wechat')
        res = requests.post('http://localhost:6800/schedule.json', data=data)
    



if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000')
