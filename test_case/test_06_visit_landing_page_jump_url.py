# -*- coding: utf-8 -*-

from time import sleep

from common.get_config_data import GetConfig
from test_case import *
from unittest import skip

GC = GetConfig()
customer = Customer()
log = Log(__file__)

landing_page_table = AssertLandingPageTable()

cus = CustomerService()

once_jump_landing_page_name = "一跳-小程序-加粉"
second_jump_landing_page_name = "二跳-H5-二维码"

once_jump_landing_page_name03 = "一跳-手动-->原生加粉小程序"
second_jump_landing_page_name03 = "二跳--加粉二维码小程序原生"

once_jump_landing_page_name04 = "一跳-自动-->旧组件二维码"
second_jump_landing_page_name04 = "二跳--旧组件二维码"

# click_id = GC.splicing_click_id()
click_id = {}

start_time = ""


class VisitLandingPageJumpUrl(unittest.TestCase, RequestApi, AddFriend):

    def setUp(self) -> None:
        global click_id
        click_id = GC.splicing_click_id()

        # 第一次获取微信客服列表数据
        cus.once_wechat_customer_service(wechat_customer_service)

    def tearDown(self):  # 每个用例运行之后运行的
        assert_once_page_data = landing_page_table.assert_once_page_data()
        self.assertTrue(assert_once_page_data,
                        msg=f"断言一跳页的数据是否正确")

        assert_second_page_data = landing_page_table.assert_second_page_data()
        self.assertTrue(assert_second_page_data,
                        msg=f"断言二跳页的数据是否正确")

        assert_data = customer.applet_add_friends_assert(start_time, click_id["click_id"])
        self.assertTrue(assert_data, msg=f"H5跳转到小程序添加好友客资列表{assert_data}")

        cus.second_wechat_customer_service(wechat_customer_service)

        assert_wechat_customer = cus.assert_wechat_customer_service_list()
        self.assertTrue(assert_wechat_customer, msg=f"微信客服列表断言")

    def test_01_applets_add_friend(self):
        """
        H5跳转到企业小程序添加好友
        """
        # 获取落地页列表一跳页二跳页访问前的数据，传入落地页名称
        landing_page_table.applet_add_friend_before(once_jump_landing_page_name, second_jump_landing_page_name)
        land_page_url = "http://bbb.dbq.yiye.ai/dbq/slLPIPXr?_cl=ffcf" + click_id["params"]
        global start_time
        start_time = GC.now_date()
        self.h5_applet_add(land_page_url)
        # 第二次获取落地页列表数据
        landing_page_table.applet_add_friend_after(once_jump_landing_page_name, second_jump_landing_page_name)

    @skip("跳过")
    def test_02_douying_applet_add_friend(self):
        """
        抖音原生页跳转到小程序添加好友
        """
        # 获取落地页列表一跳页二跳页访问前的数据，传入落地页名称
        landing_page_table.applet_add_friend_before(once_jump_landing_page_name, second_jump_landing_page_name)
        land_page_url = "https://dbq.asptest.yiye-a.com/site/dbq/slLPIPXr/97bc?lynx_enable=1&adid=__AID__&creativeid=__CID__&creativetype=__CTYPE__" + \
                        click_id["params"]
        global start_time
        start_time = GC.now_date()
        self.h5_applet_add(land_page_url)
        # 第二次获取落地页列表数据
        landing_page_table.applet_add_friend_after(once_jump_landing_page_name03, second_jump_landing_page_name)


    def test_03_H5_tenxun_applet(self):
        """
        H5跳转到腾讯原生小程序页面添加好友
        """
        # 获取落地页列表一跳页二跳页访问前的数据，传入落地页名称
        landing_page_table.applet_add_friend_before(once_jump_landing_page_name03, second_jump_landing_page_name03)
        land_page_url = "http://bbb.dbq.yiye.ai/dbq/JFDh2s5U?_cl=e7be" + \
                        click_id["params"]
        global start_time
        start_time = GC.now_date()
        self.h5_applet_add(land_page_url)
        # 第二次获取落地页列表数据
        landing_page_table.applet_add_friend_after(once_jump_landing_page_name03, second_jump_landing_page_name03)

    def test_04_H5_jiu_QR_code(self):
        """
        H5跳转到旧的二维码组件添加好友
        """
        # 获取落地页列表一跳页二跳页访问前的数据，传入落地页名称
        landing_page_table.applet_add_friend_before(once_jump_landing_page_name04, second_jump_landing_page_name04)
        land_page_url = "http://bbb.dbq.yiye.ai/dbq/IC8AxBLy?_cl=5cfa" + \
                        click_id["params"]
        global start_time
        start_time = GC.now_date()
        self.h5_applet_add(land_page_url)
        # 第二次获取落地页列表数据
        landing_page_table.applet_add_friend_after(once_jump_landing_page_name04, second_jump_landing_page_name04)

if __name__ == '__main__':
    unittest.main()
