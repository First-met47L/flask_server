from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
import smtplib



def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def send(ImageBin):
    mine = MIMEBase('image','png',filename='verify.png')
    mine.add_header('Content-Disposition','attachment',filename = 'verify.png')
    mine.add_header('Content-ID','<0>')
    mine.add_header('X-Attachment-Id','0')
    mine.set_payload(ImageBin)


    from_addr = '13288247797@163.com'
    password = 'gwj123456'
    # to_addr = '351264614@qq.com'
    to_addr = '351264614@qq.com'
    smtp_server = 'smtp.163.com'

    msg = MIMEMultipart()
    msg.attach(MIMEText('亲,请输入验证码', 'plain', 'utf-8'))
    msg['From'] = _format_addr('verifyWechat <%s>' % from_addr)
    msg['To'] = _format_addr('351264614@qq.com <%s>' % to_addr)
    msg['Subject'] = Header('来处理问题了啊', 'utf-8').encode()
    encoders.encode_base64(mine)
    msg.attach(mine)
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()