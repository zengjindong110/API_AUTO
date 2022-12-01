# -*- coding: utf-8 -*-
from datetime import datetime
from time import sleep

from common.get_config_data import GetConfig
from test_case import *

GC = GetConfig()
log = Log(__file__)


class VisitLandingPageJumpUrl(unittest.TestCase, RequestApi, AddFriend):

    def tearDown(self):  # 每个用例运行之后运行的
        pass

    @classmethod
    def tearDownClass(cls):  # 在所有用例都执行完之后运行的
        # warnings.simplefilter('ignore', ResourceWarning)
        pass

    def test_applets_add_friend(self):
        """
        H5跳转到企业小程序添加好友
        """
        click_id = GC.splicing_click_id()
        # 获取当前时间
        now_data = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        land_page_url = "http://bbb.dbq.yiye.ai/dbq/slLPIPXr?_cl=ffcf" + click_id["params"]
        self.h5_applet_add(land_page_url)
        sleep(80)
        customer = Customer()
        assert_data = customer.applet_add_friends_assert(now_data, click_id["click_id"])

        self.assertTrue(True if False not in assert_data else False, msg=f"H5跳转到小程序添加好友链路失败{assert_data}")


if __name__ == '__main__':
    unittest.main()
