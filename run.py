# coding=gbk
import unittest
from BeautifulReport import BeautifulReport
import os
from common.send_email import send_email
import sys
from config import *

source_route = os.getcwd() + "/report"

"""
外部传参不传参默认为test环境
传参：
test 为测试环境
pre  为预发环境
prod 为线上环境    
"""
# app的请求头
header = {
    "deviceType": "Android",
    "versionCode": str(worker_test["versionCode"]),
    "deviceModel": "HUAWEI-TAS-AN00",
    "appProduct": "share",
    "Content-Type": "application/json; charset=UTF-8",
    "User-Agent": "okhttp/3.11.0",
    "Connection": "keep-alive"
}


# 获取token
try:
    worker_test_token = requests.post(worker_test["gateway"] + "/lbdj/app/worker/AppLoginApiRequest",
                                      json={"phone": "17786451825", "type": "1", "password": "123456a"},
                                      headers=header).json()["data"]["token"]

    worker_test["token"] = worker_test_token

    worker_prod_token = requests.post(worker_prod["gateway"] + "/lbdj/app/worker/AppLoginApiRequest",
                                      json={"phone": "17786451825", "type": "1", "password": "abc123"},
                                      headers=header).json()["data"]["token"]
    worker_prod["token"] = worker_prod_token

    worker_pre_token = requests.post(worker_pre["gateway"] + "/lbdj/app/worker/AppLoginApiRequest",
                                     json={"phone": "17786451825", "type": "1", "password": "123456a"},
                                     headers=header).json()["data"]["token"]

    worker_pre["token"] = worker_pre_token
    print(worker_prod_token)

except:
    pass

if __name__ == '__main__':
    try:
        envi = sys.argv[1]
    except Exception:
        envi = "test"
    environment["test"] = eval("user_" + envi)
    worker_environment["test"] = eval("worker_" + envi)
    test_suite = unittest.defaultTestLoader.discover('./test_case', pattern='test_*.py')
    result = BeautifulReport(test_suite)
    result.report(filename='test_report', description='api_test_report', report_dir=source_route)
    send_email()
