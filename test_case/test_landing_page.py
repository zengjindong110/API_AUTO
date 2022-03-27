# coding=utf8
import random
import string

from test_case import *


class TestCreateLandingPages(unittest.TestCase, RequestApi):

    def test_create_order_landing_page(self):  # 函数名要以test开头，否则不会被执行
        login_data = get_request_data("/api/v1/landing-page/landing-pages/pmp")

        login_data[0]["data"]["name"] = "自动化测试" + ''.join(random.sample(string.digits + string.ascii_letters, 8))

        self.request(login_data[0])


if __name__ == '__main__':
    unittest.main()
