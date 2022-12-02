# -*- coding: utf-8 -*-
from datetime import datetime
from time import sleep

from common.get_config_data import GetConfig
from test_case import *

GC = GetConfig()
customer = Customer()
log = Log(__file__)

landing_page_table = AssertLandingPageTable()


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
        once_jump_landing_page_name = "一跳-小程序-加粉"
        second_jump_landing_page_name = "二跳-H5-二维码"

        # 获取一跳页二跳页访问前的数据，传入落地页名称
        landing_page_table.applet_add_friend_before(once_jump_landing_page_name, second_jump_landing_page_name)

        click_id = GC.splicing_click_id()
        # 获取当前时间
        now_data = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        land_page_url = "http://bbb.dbq.yiye.ai/dbq/slLPIPXr?_cl=ffcf" + click_id["params"]
        self.h5_applet_add(land_page_url)
        sleep(80)

        landing_page_table.applet_add_friend_after(once_jump_landing_page_name, second_jump_landing_page_name)
        self.assertTrue(True if landing_page_table.assert_once_page_data() else False,
                        msg=f"断言一跳页的数据是否正确")
        self.assertTrue(True if landing_page_table.assert_second_page_data() else False,
                        msg=f"断言二跳页的数据是否正确")

        assert_data = customer.applet_add_friends_assert(now_data, click_id["click_id"])
        self.assertTrue(True if False not in assert_data else False, msg=f"H5跳转到小程序添加好友链路失败{assert_data}")


if __name__ == '__main__':
    unittest.main()
