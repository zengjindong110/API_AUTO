import json

import requests

from common.get_config_data import GetConfig
from common.get_verification_code import get_verify_code

# # 获取当前文件的路径
# current_file_name = inspect.getfile(inspect.currentframe())
# # 获取当前文件的父级目录
# # os.path.dirname(current_file_name) 为获取当前路径下面的父级路径
# current_path = os.path.dirname(os.path.dirname(current_file_name)) + "/config"

get_config = GetConfig()
gateway = get_config.get_config_data("GATEWAY")["AGENT_HOST"]
#
# TOKEN = {
#     "token": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ5aXllX2FnZW50X3Rlc3QiLCJ1aWQiOjEsImFnZW50SWQiOiJ6amQiLCJhY2Nlc3NfdG9rZW4iOiIyYzMzMGI2M2RjZTg0MzZjODYyYWY0NzJlNWVhYjBlMiIsInN5c3RlbV90eXBlIjoiYWdlbnRfcHJpdmF0ZSIsImV4cCI6MTYzOTg4OTM5MH0.vuDeO_B1kfHd5jf0ON-mbtdpHJMgAkhmIy9VpWPFB6BwGDDa5yvoqV5y5p2QrflWRTPX-j0dtEizzKa2JUfiWA"}
TOKEN = ""


class GetToken(object):
    # def __call__(self, *args, **kwargs):
    #     print(1111)
    #     TOKEN =  self.get_token()

    def __init__(self):
        print(111)
        self.header = {
            "host": "dbq.asptest.yiye.ai",
            "connection": "keep-alive",
            "contenT-length": "124",
            "pragma": "no-cache",
            "cachE-control": "no-cache",
            "DNT": "1",
            "sec-ch-ua-mobile": "?0",
            "authorization": "",
            "contenT-type": "application/x-www-form-urlencoded",
            "accept": "application/json, text/plain, */*",
            "useR-agent": "mozilla/5.0 (windOWs NT 10.0; Win64; x64) aPplEwebKit/537.36 (KHTml, lIke gecKo) chrome/99.0.4844.51 safari/537.36",
            "type": "",
            "X-Y-version": "1.130.0",
            "sec-ch-ua-platform": "windows",
            "origin": "https://dbq.asptest.yiye.ai",
            "seC-fetcH-site": "same-origin",
            "seC-fetcH-mode": "cors",
            "seC-fetcH-dest": "empty",
            "referer": "https://dbq.asptest.yiye.ai/login",
            "accepT-encoding": "gzip, deflate, br",
            "accepT-language": "Zh-cN,zh;q=0.9,En-US;q=0.8,en;q=0.7,Zh-TW;q=0.6",
        }
        global TOKEN
        TOKEN = self.get_token()

    @staticmethod
    def get_verify_code():

        def get_code():
            image_url = gateway + "/api/v1/ucenter/captchas/fetch/graphic?captchaKey=f3affef4"
            captcha_value = get_verify_code(image_url)
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
            'captchaKey': 'f3affef4',
            'captchaValue': str(self.get_verify_code()),
            # 'captchaValue': "5947",
            'rememberMe': 'true'
        }
        respond = requests.post(url=url, headers=self.header, data=requests_data).json()
        return respond

    def get_token(self):
        for i in range(1):
            token = self.login_asp()
            if "token" in token.keys():
                return token
            else:
                continue


GetToken()


# if __name__ == '__main__':
#     xx = GetToken()
#     xx.login_asp()
#     xx.get_verify_code()
# # print(TOKEN)
# a = GetToken()
# a.login_asp()
