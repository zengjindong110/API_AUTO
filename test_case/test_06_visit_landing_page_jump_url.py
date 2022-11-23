# coding=utf8
import json

from test_case import *


class VisitLandingPageJumpUrl(unittest.TestCase, RequestApi):

    def tearDown(self):  # 每个用例运行之后运行的
        pass

    @classmethod
    def tearDownClass(cls):  # 在所有用例都执行完之后运行的
        # warnings.simplefilter('ignore', ResourceWarning)
        pass

    def visit_landing_page(self):
        land_page_url = "http://bbb.dbq.yiye.ai/dbq/OKXiTErF?_cl=9413"
