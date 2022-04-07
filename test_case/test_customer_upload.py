# coding=utf8
from test_case import *
import ddt


class TestCustomerUpload(unittest.TestCase, RequestApi):
    # 新建渠道
    def test_01_create_channel(self):
        create_channel_request_data = get_request_data("/api/v1/landing-page/landing-channel/batch/save")
        create_channel_data = {"advertiseAccountGroupId": 126, "createNum": 4, "landingPageId": 732}
        # 替换一些参数
        replace_data(create_channel_request_data, create_channel_data)
        # 创建落地页渠道地址
        resa = self.request(create_channel_request_data[0])
        print(resa)

    # 配置上报
    a = get_request_data("/index")
    b = dict(a)

    def test_02_configure_upload(self):
        # 落地页id
        landingPageId = "732"
        # 获取所有新建的渠道
        get_channel_data = get_request_data("/api/v1/landing-page/landing-channel/batch/collect/filter/new")
        get_channel_data["landingPageId"] = landingPageId

        channel_list = self.request(get_channel_data[0])

        # 查询advertiserAccountId
        advertiserAccountId_params = get_request_data(
            "/api/v1/marketing/advertiser-accounts/collect/filtering/from/management")
        advertiserAccountId = self.request(advertiserAccountId_params[0]).json()[0]

        # 设置上报的条件
        upload_data = get_request_data("/api/v1/landing-page/upload-configuration/collect/batch-save")
        # 需要动态传入的数据
        # 广告平台id
        accountId = upload_data[0]["accountId"]
        # 渠道id
        channelId = ""

        id = ""
        # 广告平台id的id
        advertiserAccountId = ""

        self.request(upload_data[0])


def visit_landing_page(self):
    pass
