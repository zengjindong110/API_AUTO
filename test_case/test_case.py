# coding=utf-8
from common.get_request_data import get_request_data
import unittest
import warnings


class TestUserLogin(unittest.TestCase):

    def tearDown(self):  # 每个用例运行之后运行的
        pass

    @classmethod
    def tearDownClass(cls):  # 在所有用例都执行完之后运行的
        warnings.simplefilter('ignore', ResourceWarning)

    def test_saveOrder(self):  # 函数名要以test开头，否则不会被执行
        """平台端用户账号密码登陆"""
        login_data = get_request_data("dfasdfasdf")[0]
        print(login_data)


if __name__ == '__main__':
    unittest.main()
