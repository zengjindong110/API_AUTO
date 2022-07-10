# coding=utf8
import json

from test_case import *


class TestCreatePmp(unittest.TestCase, RequestApi):

    def tearDown(self):  # 每个用例运行之后运行的
        pass

    @classmethod
    def tearDownClass(cls):  # 在所有用例都执行完之后运行的
        # warnings.simplefilter('ignore', ResourceWarning)
        pass

    def check_user(self):  # 函数名要以test开头，否则不会被执行

        data = get_request_data("/api/v1/marketing/advertiser-account-groups/collect/list")

        # respond = json.loads(self.request(data[0]).text)
        # 判断搜索pmp账号接口有没有“api_test”的账号，没有的返回false，有就返回true
        # pass
        respond = self.request(data[0])
        if respond["records"]:
            repose = respond["records"][0]

            return repose
        else:
            return False

    def test_create_user(self):
        """pmp已经创建成功默认该用例通过"""
        is_true = self.check_user()

        if is_true:

            self.assertTrue(True, "已经创建了test_api的pmp")

        else:
            advertiserGroupId = self.request({'uri': "/api/v1/marketing/advertiser-account-groups", 'method': 'POST',
                                              'data': {"name": "api_test", "advertiserAccountIndustryId": 125,
                                                       "managerList": [],
                                                       "leaderId": None,
                                                       "advertiserAccountIds": [], "target": []}, "id": 9999})
            self.assertEqual(advertiserGroupId.status_code, 200, msg="创建pmp账号")


if __name__ == '__main__':
    unittest.main()
