import requests
import time
from selenium import webdriver
from tool.emailService import EmailService
from settings import emailSettings


class wechatVerify(EmailService):



    def __init__(self):
        mainEmail = emailSettings.email
        password = emailSettings.password
        otherEmails = emailSettings.otherEmails
        pop3_server = emailSettings.pop3_server
        smtp_server = emailSettings.smtp_server
        super(wechatVerify, self).__init__(mainEmail=mainEmail, password=password, otherEmails=otherEmails,
                                           pop3Server=pop3_server, smtpServer=smtp_server, emailName='xyz')

    def execute(self,url):
        driver = webdriver.PhantomJS()
        driver.set_window_size(1200, 800)
        driver.get(url)
        #until authenticate successful(count <= 10)
        count = 1
        while True:
            inputElement = driver.find_element_by_id('input')
            commitElement = driver.find_element_by_id('bt')
            #send email
            imageBin = driver.get_screenshot_as_png()
            subjectText = '西洋志-请输入验证码-no:' + str(int(time.time() * 1000))
            self.send(subjectText=subjectText, contentText='hello, from xyzSrapy', imageBin=imageBin)

            #get msg from email
            msg = self.authentication(subjectText)
            inputElement.send_keys(msg)
            commitElement.click()
            time.sleep(5)
            #if current_url != url ,verify successful
            if driver.current_url != url:
                subjectText = 'wechat verify Successful'
                self.send(subjectText=subjectText,contentText="hello,from xyzSrapy",imageBin = driver.get_screenshot_as_png())
                driver.close()
                return True

            count += 1
            if count >10:
                return False



    def authentication(self, searchSubject):
        for i in range(10):
            verifyMsg = self.get(searchSubject=searchSubject)
            if verifyMsg:
                return verifyMsg



