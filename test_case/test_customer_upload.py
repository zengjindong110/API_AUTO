# coding=utf8
from test_case import *
from ddt import ddt
from ddt import data

all_upload_data = []


# @ddt
class TestCustomerUpload(unittest.TestCase, RequestApi):
    @classmethod
    def setUpClass(cls) -> None:
        global all_upload_data

        all_upload_data = cls().make_upload_data()

    # 初始化上报的参数

    def make_upload_data(self):
        all_request_data = get_request_data("/api/v1/landing-page/upload-configuration/collect/batch-save")
        # 落地页id
        landingPageId = "732"

        # accountId = 1642912301664260 advertiserAccountId=302 channelId=1861 landingPageId=732
        # oceanEngineUploadType=EVENT_MANAGE platformId=OCEAN_ENGINE uploadConfigurationTypesList uploadType=REAL_TIME

        for index in range(len(all_request_data)):
            # 获取accountId
            accountId = all_request_data[index]["data"][0]["accountId"]
            # 获取advertiserAccountId
            advertiserAccountId_params = get_request_data(
                "/api/v1/marketing/advertiser-accounts/collect/filtering/from/management")
            advertiserAccountId_params[0]["data"]["filtering"][1]["values"] = [accountId]
            advertiserAccountId_params[0]["data"]["filtering"][2]["values"] = [accountId]
            advertiserAccountId_params[0]["data"]["filtering"][3]["values"] = [accountId]
            advertiserAccountId = self.request(advertiserAccountId_params[0]).json()["records"][0]["id"]
            # 获取所有的渠道id
            get_channel_data = get_request_data("/api/v1/landing-page/landing-channel/batch/collect/filter/new")
            get_channel_data[0]["landingPageId"] = landingPageId
            channel_list = [i["id"] for i in self.request(get_channel_data[0]).json()["records"]]
            channelId = channel_list[index]
            all_request_data[index]["data"][0]["channelId"] = channelId
            all_request_data[index]["data"][0]["advertiserAccountId"] = advertiserAccountId
        return all_request_data

    # 新建渠道
    def test_01_create_channel(self):
        create_channel_request_data = get_request_data("/api/v1/landing-page/landing-channel/batch/save")
        create_channel_data = {"advertiseAccountGroupId": 126, "createNum": 4, "landingPageId": 732}
        # 替换一些参数
        replace_data(create_channel_request_data, create_channel_data)
        # 创建落地页渠道地址
        resa = self.request(create_channel_request_data[0])
        print(all_upload_data)
    @data(all_upload_data)
    def test_02_configure_upload(self, upload_data):
        print(1112,upload_data)
        #
        # self.request(upload_data)

    def visit_landing_page(self):
        pass


if __name__ == '__main__':
    print(all_upload_data)
    unittest.main()
