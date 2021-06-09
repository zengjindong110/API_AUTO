import os
import requests

# 账号token  账号： 13691994354 密码 123465


token = "f90f0afb21319170785c72a795ab77a9"
timeout = 20
gateway = "http://192.168.100.93:9061"

user_pre = {"token": "6a29053e534326ee2276844d4b1bf95d", "timeout": 20, "gateway": "http://192.168.100.102:9061",
            "pay_password": "123456", "login_password": "654321"}  # 预发环境

user_prod = {"token": "632bfa00cd0385d35197eff77ff91382", "timeout": 20, "gateway": "https://order.lbdj.com",
             "pay_password": "lbdj93", "login_password": "wode2008"}  # 线上环境

user_test = {"token": "8570e593064532e90ce52684382895db", "timeout": 20, "gateway": "http://192.168.100.93:9061",
             "pay_password": "654321", "login_password": "654321"}  # 测试环境

worker_test = {"token": "51518e7aaffb4556ad9d7355f9cce57f", "timeout": 20, "gateway": "http://192.168.100.80:9030",
               "versionCode": 76}  # 测试环境

worker_pre = {"token": "40e17701e1e342f998a7f004e1f10abb", "timeout": 20, "gateway": "http://192.168.100.118:9030",
              "versionCode": 76}  # 预发环境

worker_prod = {"token": "e05e55802cc64a7280056a900e450cb9", "timeout": 20, "gateway": "http://app-api.lb-dj.com",
               "versionCode": 76}  # 线上环境


environment = {"test": user_test}

# worker_environment = {"test": worker_live}
worker_environment = {"test": worker_test}

# 发送邮件给哪些人
to_list = [
    # 多用户使用的list
    'cengjindong1825@dingtalk.com',
    '17786451825@163.com'
]
# 邮件内容
content = "接口测试报告"  # 邮件内容
subject = "自动化接口测试报告"  # 邮件主题
mail_user = '248381089@qq.com'  # 发件人邮箱密码(当时申请smtp给的口令)
mail_pwd = 'gufjyfdzorolbjcd'  # SMTP密码
mail_host = 'smtp.qq.com'  # 邮箱服务器

# 请求参数数据库连接
mysql_host = 'rm-wz9325c14dsxj3l0kko.mysql.rds.aliyuncs.com'
mysql_user = 'root'
mysql_passworld = 'AZFZhh@H55XAuMu'
mysql_port = 3306
mysql_db = 'project'
