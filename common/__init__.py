import json
import os
import requests
from common.get_verification_code import get_verify_code
from common.get_config_data import GetConfig
import inspect

# 获取当前文件的路径
current_file_name = inspect.getfile(inspect.currentframe())
# 获取当前文件的父级目录
current_path = os.path.dirname(current_file_name)
current_path = os.path.dirname(current_path) + "/config"

print(current_path)

token = ""

get_config = GetConfig(current_path)

gateway = get_config.get_config_data("GATEWAY")["AGENT_HOST"]

headers = {
    'Host': 'agent.yiye.ai',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json, text/plain, */*',
}

captchaValue = get_verify_code(gateway + "/api/v1/ucenter/captchas/fetch/graphic?captchaKey=7de649d9")

verify_code = str(json.loads(captchaValue["RspData"])["result"])


def login_asp():
    url = gateway + "/api/v1/ucenter/sessions/action/login"
    if len(verify_code) == 4 and verify_code.isdigit():
        requests_data = {
            'loginKey': 'yiye_agent_test@yiye.ai',
            'password': '111111',
            'captchaType': 'GRAPHIC',
            'captchaKey': '7de649d9',
            'captchaValue': str(verify_code),
            'rememberMe': 'true'
        }

        return requests.post(url=url, data=requests_data).json()

    else:
        captchaValue = get_verify_code(gateway + "/api/v1/ucenter/captchas/fetch/graphic?captchaKey=7de649d9")


token = login_asp()
for i in range(3):
    if "token" in token.keys():
        token = token
    else:
        token = login_asp()

print(token)
