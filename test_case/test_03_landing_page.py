# coding=utf8

from test_case import *

landing_page_id = None


# 还有上传图片和获取表单订单没有做

class TestCreateLandingPages(unittest.TestCase, RequestApi):

    def test_01_create_landing_page_name(self):  # 函数名要以test开头，否则不会被执行
        """创建落地页名称"""
        login_data = get_request_data("/api/v1/landing-page/landing-pages/pmp")

        login_data[0]["data"]["name"] = now_date()

        landing_page_name = self.request(login_data[0])
        self.assertTrue(landing_page_name["name"], msg="创建落地页名称成功")
        global landing_page_id
        landing_page_id = landing_page_name["id"]

    def test_02_create_landing_page_data(self):
        """创建落地页里面的内容"""
        landing_page_content = get_request_data(
            "https://lpedit-asptest.yiye.ai/api/v1/landing-page/landing-pages/pmp/{}")

        landing_page_content[0].update({
                                           "uri": "https://lpedit-asptest.yiye.ai/api/v1/landing-page/landing-pages/pmp/{}".format(
                                               str(landing_page_id))})
        landing_page_data = self.request(landing_page_content)
        self.assertEqual(landing_page_data["id"], landing_page_id, msg="通过返回的id来进行断言")

    def test_03_access_landing_page(self):
        """访问落地页url"""
        landing_page_channel = get_request_data("/api/v1/landing-page/landing-channel/batch/collect/filter/new")
        replace_data(landing_page_channel,
                     {'landingPageId': landing_page_id, 'startTime': start_time(), 'endTime': end_time()})
        # 查询落地页url，pv，uv
        after_landing_page_channel_data = self.request(landing_page_channel)
        landing_page_url = after_landing_page_channel_data["records"][0]["url"]
        open_url(landing_page_url)
        before_landing_page_channel_data = self.request(landing_page_channel)
        self.assertEqual(after_landing_page_channel_data["records"][0]["pageViewNum"] + 1,
                         before_landing_page_channel_data["records"][0]["pageViewNum"], msg="判断pv有没有增加1")
        self.assertEqual(after_landing_page_channel_data["records"][0]["visitorNum"] + 1,
                         before_landing_page_channel_data["records"][0]["visitorNum"], msg="判断uv有没有增加1")


if __name__ == '__main__':
    unittest.main()
