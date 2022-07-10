# coding=utf8
from ddt import data
from ddt import ddt

from test_case import *

landingPageId = "762"


def get_upload_params():
    res = RequestApi()
    all_upload_data = get_request_data("/api/v1/landing-page/upload-configuration/collect/batch-save")
    # accountId = 1642912301664260 advertiserAccountId=302 channelId=1861 landingPageId=732
    # oceanEngineUploadType=EVENT_MANAGE platformId=OCEAN_ENGINE uploadConfigurationTypesList uploadType=REAL_TIME
    # 获取所有的渠道id
    get_channel_data = get_request_data("/api/v1/landing-page/landing-channel/batch/collect/filter/new")
    get_channel_data[0]["data"]["landingPageId"] = landingPageId
    channel_list = [i["id"] for i in res.request(get_channel_data[0])["records"]]
    for index in range(len(all_upload_data)):
        # 获取每个媒体平台广告账户
        accountId = all_upload_data[index]["data"][0]["accountId"]
        # 获取advertiserAccountId（媒体平台账户在我们系统里面的id）
        advertiserAccountId_params = get_request_data(
            "/api/v1/marketing/advertiser-accounts/collect/filtering/from/management")
        advertiserAccountId_params[0]["data"]["filtering"][1]["values"] = [accountId]
        advertiserAccountId_params[0]["data"]["filtering"][2]["values"] = [accountId]
        advertiserAccountId_params[0]["data"]["filtering"][3]["values"] = [accountId]
        advertiserAccountId = res.request(advertiserAccountId_params[0])["records"][0]["id"]
        # 获取单个的渠道id
        channelId = channel_list[index]

        all_upload_data[index]["data"][0]["landingPageId"] = landingPageId
        all_upload_data[index]["data"][0]["channelId"] = channelId
        all_upload_data[index]["data"][0]["advertiserAccountId"] = advertiserAccountId
        if "id" in all_upload_data[index]["data"][0].keys():
            all_upload_data[index]["data"][0].pop("id")

    return all_upload_data


all_upload_data = get_upload_params()


@ddt
class TestCustomerUpload(unittest.TestCase, RequestApi):

    # 新建渠道
    def test_01_create_channel(self):
        create_channel_request_data = get_request_data("/api/v1/landing-page/landing-channel/batch/save")
        create_channel_data = {"advertiseAccountGroupId": 126, "createNum": 4, "landingPageId": landingPageId}
        # 替换一些参数
        replace_data(create_channel_request_data, create_channel_data)
        # 创建落地页渠道地址
        self.request(create_channel_request_data[0])

    @data(all_upload_data[0], all_upload_data[1],all_upload_data[2],all_upload_data[3])
    def test_02_configure_upload(self, value):
        self.request(value)


if __name__ == '__main__':
    print(all_upload_data)
    unittest.main()
