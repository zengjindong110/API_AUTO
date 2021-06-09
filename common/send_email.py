# coding=gbk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config

"""
发送邮件模块
"""


# 发送邮件
def send_email():
    s = smtplib.SMTP_SSL(config.mail_host, 465, timeout=5)
    s.login(config.mail_user, config.mail_pwd)

    # 邮件内容
    mail = config.content
    msg = MIMEMultipart()
    msgtext = MIMEText(mail.encode('utf8'), _subtype='html', _charset='utf8')
    msg['From'] = config.mail_user
    msg['Subject'] = config.subject
    msg['To'] = ",".join(config.to_list)
    unpatch = "./report/test_report.html"
    if unpatch is not None:
        file = open(unpatch, 'rb').read()
        att1 = MIMEText(file, 'base64', "utf-8")
        att1["Content-Type"] = 'application/octet-stream'
        att1.add_header('Content-Disposition', 'attachment', filename='test_report.html')
        msg.attach(att1)
    msg.attach(msgtext)
    try:
        s.sendmail(config.mail_user, config.to_list, msg.as_string())
        s.close()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    send_email()
