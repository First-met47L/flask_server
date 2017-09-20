from urllib import parse
from tool import log
import json
import requests

from flask import Flask
from flask import request
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


@app.route('/wechat/email/verify')
def verify():
    url = request.args.get('url')
    result = None
    try:
        result = wechatVerify().execute(url=url)
    except Exception as e:
        log.Log.getLog("verify").exception(e)
    if result:
        data = dict(project='xyh_magazine', spider='wechat')
        res = requests.post('http://localhost:6800/schedule.json', data=data)
        return "verify successful"
    return "verify faild"





    



if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000')
