# coding=utf8

from test_case import *


class TestCreateLandingPages(unittest.TestCase, RequestApi):

    def test_01_order_submit(self):
        """订单提交"""
        order_submit("http://bbb.dbq.yiye.ai/dbq/L4mTNVRP?_cl=253e")

    def test_02_table_submit(self):
        """表单提价"""
        table_submit("https://dbq.asptest.yiye-a.com/dbq/Aa2lwmNB?_cl=8fbf")

