
import requests
import time

from selenium import webdriver

from tool.emailService import EmailService

driver = webdriver.PhantomJS()
url = 'https://mp.weixin.qq.com/profile?src=3&timestamp=1505376389&ver=1&signature=jmaYw3DkdTVDWD0SCOphrtO4IoQZEQSpixhkVNBEMpHFVxfOgcyO5mqUjQWFwcpdb6AkD5SoLH2GhsLSZpkdNQ=='
driver.set_window_size(1200, 800)
cookies = driver.get_cookies()


# print(cookies)
# driver.get(url)
# for k, v in cookies.iteritems():
#     cookie_dict = {'name': k, 'value': v}
#     driver.add_cookie(cookie_dict)
driver.get(url)

inputElement = driver.find_element_by_id('input')

commitElement = driver.find_element_by_id('bt')


imageBin = driver.get_screenshot_as_png()
email = '351264614@xiyanghui.com'
password = 'zg8FaBvq4cH4fsCF'
otherEmails = ['351264614@qq.com']
pop3_server = 'imap.exmail.qq.com'
smtp_server = 'smtp.exmail.qq.com'
emailService = EmailService(email, password, otherEmails, pop3_server, smtp_server)
subjectText = '西洋志-请输入验证码-no:'+str(int(time.time()*1000))
emailService.send(subjectText=subjectText, contentText='hello,from xyzSrapy', imageBin=imageBin)

msg = None
for i in range(10):
    try:
        res = requests.get('http://localhost:5000/email/verify/%s'%subjectText,timeout=60)
        msg = res.text
        if msg:
            break
    except requests.exceptions.Timeout as e:
        pass


print(msg)
inputElement.send_keys(msg)
commitElement.click()
time.sleep(5)
imageBin = driver.get_screenshot_as_png()
subjectText='result'
emailService.send(subjectText=subjectText, contentText='hello,from xyzSrapy', imageBin=imageBin)
# element = driver.find_element_by_id('seccodeImage')
# left = int(element.location['x'])
# top = int(element.location['y'])
# right = int(element.location['x'] + element.size['width'])
# bottom = int(element.location['y'] + element.size['height'])
#
# im = Image.open('screenshot.png')
# im = im.crop((left, top, right, bottom))
# im.save('code.png')

