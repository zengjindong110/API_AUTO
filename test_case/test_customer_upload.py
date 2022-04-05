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
    def test_02_configure_upload(self):
        # 获取所有新建的渠道
        get_channel_data = get_request_data("/api/v1/landing-page/landing-channel/batch/collect/filter/new")
        channel_list = self.request(get_channel_data[0])

        # 查询advertiserAccountId
        advertiserAccountId_params = get_request_data("/api/v1/marketing/advertiser-accounts/collect/filtering/from/management")
        data = self.request(advertiserAccountId_params[0])

        # 设置上报的条件
        upload_data = get_request_data("/api/v1/landing-page/upload-configuration/collect/batch-save")
        self.request(upload_data[1])







    def visit_landing_page(self):
        pass