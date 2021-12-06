# coding=utf8
import random
import string
from test_case import *


# import unittest
# from common.request_api import RequestApi
# from common.get_request_data import get_request_data


class TestUserLogin(unittest.TestCase, RequestApi):
    # def __init__(self):
    #     RequestApi.__init__(self)

    def tearDown(self):  # 每个用例运行之后运行的
        pass

    @classmethod
    def tearDownClass(cls):  # 在所有用例都执行完之后运行的
        # warnings.simplefilter('ignore', ResourceWarning)
        pass

    def test_saveOrder(self):  # 函数名要以test开头，否则不会被执行
        login_data = get_request_data("/api/v1/landing-page/landing-pages/pmp")

        print(login_data)
        login_data[0]["data"]["name"] = "自动化测试" + ''.join(random.sample(string.digits + string.ascii_letters, 8))
        # r = RequestApi()
        self.request(login_data[0])


if __name__ == '__main__':
    unittest.main()
