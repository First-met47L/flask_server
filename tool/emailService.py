from email import encoders
from email.header import Header,decode_header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
from email.parser import Parser
import os
import re
import smtplib
import poplib


class EmailService(object):
    @staticmethod
    def format_addr(address):
        name, addr = parseaddr(address)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    @staticmethod
    def decode_str(s):
        '''
        邮件的Subject或者Email中包含的名字都是经过编码后的str，须要decode：
        :param s:
        :return:
        '''
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    @staticmethod
    # 编码设置
    def guess_charset(my_msg):
        charset = my_msg.get_charset()
        if charset is None:
            content_type = my_msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
            return charset

    @staticmethod
    def getVerifyMsg(msgObj,searchSubject):
        subject = msgObj.get('Subject')
        subjectCompile = re.compile(searchSubject)
        if not subject or not re.search(subjectCompile,EmailService.decode_str(subject)):
            return
        content_type = msgObj.get_content_type()
        if msgObj.is_multipart():
            parts = msgObj.get_payload()
            for n,part in enumerate(parts):

                content = part.get_payload(decode=True)
                charset = EmailService.guess_charset(part)
                if charset:
                    content = content.decode(charset)
                regex = re.search('[0-9a-zA-Z]+',content)
                if regex:
                    return regex.group()
                break
        return


    def __new__(cls, *args, **kwargs):
        self = super(EmailService, cls).__new__(cls)
        return self

    def __init__(self, mainEmail, password, otherEmails, pop3Server, smtpServer, emailName='xyz'):
        '''
        :param mainEmail: (str)YourEmail Like 'xxx@xiyanghui.com'
        :param password: (str)YourEmail password
        :param otherEmails: (list<str>)OtherEmails to/get Like ['xxx@xiyanghui.com','xxx@163.com']
        :param pop3Server: (str)
        :param smtpServer: (str)
        :param emailName: (str) default >> emalName='default'
        '''
        self.mainEmail = mainEmail
        self.password = password
        self.pop3Server = pop3Server
        self.smtpServer = smtpServer
        self.otherEmails = otherEmails
        self.emailName = emailName

    def send(self, subjectText='', contentText='', imageBin=None, imageAttachName='defalut.png'):
        '''
        :param subjectText: (str)
        :param contentText: (str)
        :param imageBin: (byte) ImageAttachment base64 bin
        :param imageAttachName: (str) AttahName
        :return:
        '''

        msg = MIMEMultipart()
        msg.attach(MIMEText(contentText, 'plain', 'utf-8'))
        print(self.emailName)
        msg['From'] = EmailService.format_addr('%s <%s>' % (self.emailName, self.mainEmail))
        msg['To'] = ','.join(self.otherEmails)
        msg['Subject'] = Header(subjectText, 'utf-8').encode()

        if imageBin:
            mine = MIMEBase('image', 'png', filename=imageAttachName)
            mine.add_header('Content-Disposition', 'attachment', filename=imageAttachName)
            mine.add_header('Content-ID', '<0>')
            mine.add_header('X-Attachment-Id', '0')
            mine.set_payload(imageBin)
            encoders.encode_base64(mine)
            msg.attach(mine)

        server = smtplib.SMTP_SSL(self.smtpServer, 465)

        #debug level print debug info
        #if level >1 print (datetime.datetime.now().time(), *args, file=sys.stderr)
        #else print (*args, file=sys.stderr) like reply: b'250 Ok: queued as \r\n'
        server.set_debuglevel(1)
        server.login(self.mainEmail, self.password)
        server.sendmail(self.mainEmail, self.otherEmails, msg.as_string())
        server.quit()


    def get(self,searchSubject):
        '''
        :param searchSubject: 匹配邮件的主题
        :return:
        '''
        server = poplib.POP3_SSL(self.pop3Server)
        # server.set_debuglevel(2)
        print(server.getwelcome().decode('utf-8')) #welcome message
        #user authentication
        server.user(self.mainEmail)
        server.pass_(self.password)

        emailNum,spaceSize = server.stat()
        # stat()返回邮件数量和占用空间:
        print('MessagesNum: %s. Size: %s' %(emailNum,spaceSize))
        # list()返回所有邮件的编号:
        resp, mails, octets = server.list()
        # print(mails)

        # 获取最新的5封邮件,(server.retr的索引号从1开始):
        index = len(mails)
        msgs = []
        for i in range(5):
            resp, lines, octets = server.retr(index-i)
            # lines存储了邮件的原始文本的每一行,
            # 可以获得整个邮件的原始文本:
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            msgs.append(Parser().parsestr(msg_content))
        # 关闭连接:
        server.quit()

        for msg in msgs:
            verifyMsg = EmailService.getVerifyMsg(msgObj=msg,searchSubject=searchSubject)
            if verifyMsg:
                return verifyMsg




# 连接数据库
# server = poplib.POP3(pop3_server)

if __name__ == '__main__':
    email = '351264614@xiyanghui.com'
    password = 'zg8FaBvq4cH4fsCF'
    otherEmails = ['351264614@qq.com']
    pop3_server = 'imap.exmail.qq.com'
    smtp_server = 'smtp.exmail.qq.com'
    emailService = EmailService(email, password, otherEmails, pop3_server, smtp_server)
    # with open(os.path.join(os.getcwd(),'static/emoji_ios.jpeg'),'rb') as f:
    #     imageBin = f.read()
    # emailService.send(headerText='西洋志-请输入验证码',contentText='hello,from xyzSrapy',imageBin=imageBin)

    print(emailService.get(searchSubject='西洋志-请输入验证码'))
