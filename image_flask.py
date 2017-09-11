from flask import Flask,render_template
import requests,json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/spider/exec/<string:name>') #<string:name> convert string
def add(name):
    data = dict(project='xyh_magazine', spider= name)
    res = requests.post('http://localhost:6800/schedule.json', data=data)
    resDict = json.loads(res.text)
    resDict.pop('node_name')
    resDict['name'] = name
    return json.dumps(resDict)


if __name__ == '__main__':
    app.run('0.0.0.0')
