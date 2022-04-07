# coding=utf8
from test_case import *


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
        # 获取所有的渠道id
        get_channel_data = get_request_data("/api/v1/landing-page/landing-channel/batch/collect/filter/new")
        get_channel_data[0]["landingPageId"] = landingPageId
        channel_list = [i["id"] for i in self.request(get_channel_data[0]).json()["records"]]

        # 获取设置上报的条件
        upload_data = get_request_data("/api/v1/landing-page/upload-configuration/collect/batch-save")

        # 需要动态传入的数据
        #  需要传入以下数据
        # accountId = 1642912301664260 advertiserAccountId=302 channelId=1861 landingPageId=732
        # oceanEngineUploadType=EVENT_MANAGE platformId=OCEAN_ENGINE uploadConfigurationTypesList uploadType=REAL_TIME

        # 媒体平台广告账户id
        accountId = upload_data[0]["data"][0]["accountId"]

        # 查询advertiserAccountId
        advertiserAccountId_params = get_request_data(
            "/api/v1/marketing/advertiser-accounts/collect/filtering/from/management")
        advertiserAccountId_params[0]["data"]["filtering"][1]["values"] = [accountId]
        advertiserAccountId_params[0]["data"]["filtering"][2]["values"] = [accountId]
        advertiserAccountId_params[0]["data"]["filtering"][3]["values"] = [accountId]
        advertiserAccountId = self.request(advertiserAccountId_params[0]).json()["records"][0]["id"]


        # id字段是更新上报配置的时候才会有,新设置上报配置没有id字段
        id = ""

        # 渠道id
        channelId = channel_list[0]
        upload_data[0]["data"][0]["channelId"] = channelId
        # 媒体平台广告账户id的id
        upload_data[0]["data"][0]["advertiserAccountId"] = advertiserAccountId
        self.request(upload_data[0])


def visit_landing_page(self):
    pass
