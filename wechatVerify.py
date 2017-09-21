import requests
import time
from selenium import webdriver
import selenium
from tool.emailService import EmailService
from settings import emailSettings
from tool import log

class wechatVerify(EmailService):
    logger = log.Log.getLog("verify")
    def __init__(self):
        mainEmail = emailSettings.email
        password = emailSettings.password
        otherEmails = emailSettings.otherEmails
        pop3_server = emailSettings.pop3_server
        smtp_server = emailSettings.smtp_server
        super(wechatVerify, self).__init__(mainEmail=mainEmail, password=password, otherEmails=otherEmails,
                                           pop3Server=pop3_server, smtpServer=smtp_server, emailName='xyz')

    def execute(self, url):
        driver = webdriver.PhantomJS()
        driver.set_window_size(1200, 800)
        driver.get(url)
        # until authenticate successful(count <= 10)
        count = 1
        while True:
            imageBin = driver.get_screenshot_as_png()

            try:
                inputElement = driver.find_element_by_id('input')
                commitElement = driver.find_element_by_id('bt')
            except Exception as e:
                self.logger.info("successful")
                self.send(subjectText="selenium.common.exceptions.NoSuchElementException",
                          contentText='hello, from xyzSrapy', imageBin=imageBin)
                return True
            # send email
            subjectText = '西洋志-请输入验证码-no:' + str(int(time.time() * 1000))
            self.send(subjectText=subjectText, contentText='hello, from xyzSrapy', imageBin=imageBin)

            # get msg from email
            msg = self.authentication(subjectText)
            self.logger.info("return msg >> %s"%msg)
            if msg:
                inputElement.send_keys(msg)
                commitElement.click()
            time.sleep(5)
            # if current_url != url ,verify successful

            if count > 30:
                subjectText = "wechat verify failed"
                self.send(subjectText=subjectText, contentText="hello,from xyzScrapy")
                return False
            count += 1

    def authentication(self, searchSubject):
        for i in range(10):
            time.sleep(5)
            verifyMsg = self.get(searchSubject=searchSubject)
            if verifyMsg:
                return verifyMsg
