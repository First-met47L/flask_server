from flask import Flask, render_template
import requests, json, time
import EmailService
from urllib import parse

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


@app.route('/email/verify/<string:subject>')
def getVerifyMsg(subject):
    '''
    :param subject:匹配标题
    :return:
    '''
    email = '351264614@xiyanghui.com'
    password = 'zg8FaBvq4cH4fsCF'
    otherEmails = ['351264614@qq.com']
    pop3_server = 'imap.exmail.qq.com'
    smtp_server = 'smtp.exmail.qq.com'
    emailService = EmailService.EmailService(email, password, otherEmails, pop3_server, smtp_server)
    subject = parse.unquote(subject)
    for i in range(10):
        verifyMsg = emailService.get(subject)
        if verifyMsg:
            print(verifyMsg)
            return verifyMsg
        time.sleep(10)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='17250')
