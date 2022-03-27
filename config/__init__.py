import json

import requests

from common.log import Log
from config.get_config_data import GetConfig
from config.get_verification_code import get_verify_code

TOKEN = {
    'token': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ5aXllX2FnZW50X3Rlc3QiLCJ1aWQiOjEsImFnZW50SWQiOiJkYnEiLCJhY2Nlc3NfdG9rZW4iOiIwMGZjYjYxNDM1NTY0MzA3OWRmNjI4YmI0MjRkZjM4OCIsInN5c3RlbV90eXBlIjoiYWdlbnRfcHJpdmF0ZSIsImV4cCI6MTY0OTQ2OTY5NX0.tKcuOy1Rnyv-6EFCohqL_sfuTveuZ-9moxBk9axEeJAe7ysxrvdOcq9FAHOJOzgMLT5mz0sJpXGEFmrG4Jyccw'}
PMP_ID = ""
get_config = GetConfig()
gateway = get_config.get_config_data("USER")["HOST"]

logger = Log(__file__)


class GetToken(object):

    def __init__(self):
        global TOKEN
        # TOKEN = self.get_token()
        global PMP_ID
        PMP_ID = self.get_pmp_id()

    def get_verify_code(self):

        def get_code():
            image_url = gateway + "/api/v1/ucenter/captchas/fetch/graphic?captchaKey=f3affef4"
            img_data = requests.get(url=image_url, headers=get_config.get_header()).content
            files = {
                'img_data': ('img_data', img_data)
            }
            captcha_value = get_verify_code(files)
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
            'rememberMe': 'true'
        }
        respond = requests.post(url=url, headers=get_config.get_header(), data=requests_data).json()
        return respond

    def get_token(self):
        for i in range(1):
            token = self.login_asp()
            if "token" in token.keys():
                return token
            else:
                continue

    def get_pmp_id(self):
        # 查看当前pmp是否有api_test的pmp
        pmp_url = gateway + "/api/v1/marketing/advertiser-account-groups/collect/list"
        params = {"name": "api_test"}
        respond = requests.get(url=pmp_url, headers=get_config.get_header(), params=params).json()
        try:
            if respond["records"]:

                return respond["records"][0]["id"]

            else:

                create_pmp_url = gateway + "/api/v1/marketing/advertiser-account-groups"
                data = {"name": "api_test", "advertiserAccountIndustryId": 2, "managerList": [], "leaderId": None,
                        "advertiserAccountIds": [], "target": []}
                global PMP_ID
                PMP_ID = requests.post(url=create_pmp_url, headers=get_config.get_header(), json=data).json()
            raise respond
        except KeyError:
            logger.error("查询pmp_id出现错误:{}".format(str(respond)))


GetToken()
