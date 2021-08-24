import json

import requests
from common.get_verification_code import get_verify_code
from common.get_config_data import GetConfig

# # 获取当前文件的路径
# current_file_name = inspect.getfile(inspect.currentframe())
# # 获取当前文件的父级目录
# # os.path.dirname(current_file_name) 为获取当前路径下面的父级路径
# current_path = os.path.dirname(os.path.dirname(current_file_name)) + "/config"

get_config = GetConfig()

gateway = get_config.get_config_data("GATEWAY")["AGENT_HOST"]

TOKEN = {}


class GetToken(object):
    def __init__(self):
        self.header = {
            'Host': 'agent.yiye.ai',
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json, text/plain, */*',
        }

        global TOKEN
        TOKEN = self.get_token()

    @staticmethod
    def get_verify_code():

        def get_code():

            captcha_value = get_verify_code(gateway + "/api/v1/ucenter/captchas/fetch/graphic?captchaKey=7de649d9")

            code = str(json.loads(captcha_value["RspData"])["result"])
            return code

        # 如果验证码不是数字和长度不是四位就再次执行
        for i in range(3):
            verify_code = get_code()
            if len(verify_code) == 4 and verify_code.isdigit():
                return verify_code
            else:
                continue

    def login_asp(self):
        url = gateway + "/api/v1/ucenter/sessions/action/login"

        requests_data = {
            'loginKey': 'yiye_agent_test@yiye.ai',
            'password': '111111',
            'captchaType': 'GRAPHIC',
            'captchaKey': '7de649d9',
            'captchaValue': str(self.get_verify_code()),
            'rememberMe': 'true'
        }
        respond = requests.post(url=url, data=requests_data).json()

        return respond

    def get_token(self):
        for i in range(3):
            token = self.login_asp()
            if "token" in token.keys():
                return token
            else:
                continue


GetToken()
#
# GetToken()
# print(TOKEN)

