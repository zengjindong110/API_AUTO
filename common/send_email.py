# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from common.get_config_data import GetConfig
from common.log import Log
con = GetConfig()
get_config = con.get_config_data("EMAIL")

logger = Log(__file__)

def send_email():
    s = smtplib.SMTP_SSL(get_config["MAIL_HOST"], 465, timeout=5)
    s.login(get_config["MAIL_USER"], get_config["MAIL_PWD"])
    mail = get_config["CONTENT"]
    msg = MIMEMultipart()
    msgtext = MIMEText(mail.encode('utf8'), _subtype='html', _charset='utf8')
    msg['From'] = get_config["MAIL_USER"]
    msg['Subject'] = get_config["SUBJECT"]
    to_mail = eval(get_config["TO_LIST"])
    msg['To'] = ",".join(to_mail)
    # print(22,eval(get_config["TO_LIST"])[1])
    # msg['To'] = get_config["TO_LIST"]

    unpatch = "./report/test_report.html"
    if unpatch is not None:
        file = open(unpatch, 'rb').read()
        att1 = MIMEText(file, 'base64', "utf-8")
        att1["Content-Type"] = 'application/octet-stream'
        att1.add_header('Content-Disposition', 'attachment', filename='test_report.html')
        msg.attach(att1)
    msg.attach(msgtext)
    try:
        s.sendmail(get_config["MAIL_USER"], to_mail, msg.as_string())
        logger.info(f"邮件以发送到{get_config['MAIL_USER']}")
        s.close()

    except Exception as e:
        logger.error(f"发送失败，查看报错{e}")


if __name__ == '__main__':
    send_email()
