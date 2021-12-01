import json
import unittest
from common.request_api import RequestApi
from common.get_request_data import get_request_data

__all__ = ['RequestApi', 'get_request_data', 'unittest', ]

R = RequestApi()



class CheckPmp(object):
    def __init__(self):
        self.creat_user()

    @staticmethod
    def check_user():
        data = {'uri': "/api/v1/marketing/advertiser-account-groups/collect/list", 'method': 'GET',
                'data': {"name": "api_test"}}

        respond = json.loads(R.request(data))
        # 判断搜索pmp账号接口有没有“api_test”的账号，没有的返回false，有就返回true

        if respond["records"]:
            repose = respond["records"][0]

            return repose
        else:
            return False

    def creat_user(self):
        advertiserGroupId = self.check_user()
        if advertiserGroupId:
            print(advertiserGroupId)
            return advertiserGroupId
        else:
            advertiserGroupId = R.request({'uri': "/api/v1/marketing/advertiser-account-groups", 'method': 'POST',
                                           'data': {"name": "api_test", "advertiserAccountIndustryId": 125,
                                                    "managerList": [],
                                                    "leaderId": None,
                                                    "advertiserAccountIds": [], "target": []}})
            return advertiserGroupId


CheckPmp()

