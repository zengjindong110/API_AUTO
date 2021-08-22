#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from get_config_data import GetConfig

config = GetConfig("base")
get_config = config.get_config_data("email")

def send_email():
    s = smtplib.SMTP_SSL(get_config["mail_host"], 465, timeout=5)
    s.login(get_config["mail_user"], get_config["mail_pwd"])

    mail = get_config["content"]
    msg = MIMEMultipart()
    msgtext = MIMEText(mail.encode('utf8'), _subtype='html', _charset='utf8')
    msg['From'] = get_config["mail_user"]
    msg['Subject'] = get_config["subject"]
    # msg['To'] = ",".join(get_config["to_list"])
    msg['To'] = get_config["to_list"]
    unpatch = "../report/test_report.html"
    if unpatch is not None:
        file = open(unpatch, 'rb').read()
        att1 = MIMEText(file, 'base64', "utf-8")
        att1["Content-Type"] = 'application/octet-stream'
        att1.add_header('Content-Disposition', 'attachment', filename='test_report.html')
        msg.attach(att1)
    msg.attach(msgtext)
    try:
        s.sendmail(get_config["mail_user"], get_config["to_list"], msg.as_string())
        s.close()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    send_email()
