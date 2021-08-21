# coding=gbk

import unittest
from common.get_verification_code import *
from common.get_request_data import *
from common.assert_data import *
from common.request_api import RequestApi
import warnings
import config


class TestUserLogin(unittest.TestCase):

    def tearDown(self):  # 每个用例运行之后运行的
        key_list.clear()

    @classmethod
    def tearDownClass(cls):  # 在所有用例都执行完之后运行的
        warnings.simplefilter('ignore', ResourceWarning)

    def test_saveOrder(self):  # 函数名要以test开头，否则不会被执行
        """平台端用户账号密码登陆"""
        login_data = get_request_data("dfasdfasdf")[0]

        image_url = "{}/lbdj/web/user/loginverify?v=0.2705254559664316&u=omUm1iyj".format(
            config.environment["test"]["gateway"])
        code = get_verify_code(image_url)["RspData"]
        code = json.loads(code)["result"]
        login_res = json.loads(login_data["data"])
        login_res["userLoginDto"]["password"] = config.environment["test"]["login_password"]
        login_res["userLoginDto"]["veriftyRecordCode"] = code
        login_res = RequestApi.request(login_data["method"], login_data["uri"], login_res)
        if login_res.json()["msg"] == "验证码错误或失效":
            login_res = RequestApi.request(login_data["method"], login_data["uri"], login_res)

        self.assertTrue(assert_key(login_data["assert"], login_res.text), msg=login_res.text)


if __name__ == '__main__':
    unittest.main()
