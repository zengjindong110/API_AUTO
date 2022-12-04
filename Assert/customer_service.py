from common.get_config_data import GetConfig
from common.log import Log
from common.request_api import RequestApi

log = Log(__file__)
gc = GetConfig()


class CustomerService(RequestApi):
    def __init__(self):
        super().__init__()

        self.once_wechat_customer_service_data = {}
        self.second_wechat_customer_service_data = {}

    def get_customer_service_list(self, name):
        params = {
            "method": "POST",
            "id": 20,
            "uri": "/api/v1/landing-page/wechat-customer-service/collect/filtering",
            "data": {
                "advertiserAccountGroupId": gc.get_pmp_id(),
                "wechatCustomerServiceGroupId": "",
                "wechatUserName": name,
                "startTime": gc.start_time()[1],
                "endTime": gc.end_time()[1]
            }
        }
        respond = self.request(params)
        try:
            respond = respond["records"][0]
            # respond = respond
        except KeyError:
            log.error(f"查询的接口返回的客资不是字典{respond}")
        else:
            return respond

    def once_wechat_customer_service(self, name):
        """
        第一次查询微信客服列表的数据
        """
        self.once_wechat_customer_service_data = self.get_customer_service_list(name)
        # print(self.once_wechat_customer_service_list)

    def second_wechat_customer_service(self, name):
        """
        第二次查询微信客服列表的数据
        """
        self.second_wechat_customer_service_data = self.get_customer_service_list(name)

    def assert_wechat_customer_service_list(self):
        """
        微信客服列表断言方式：
        二维码展示数 +1
        二维码长按识别数 +1
        落地页链路成功加企业微信数 +1
        """
        # 二维码展示数
        qrCodeShowNum = self.second_wechat_customer_service_data["qrCodeShowNum"] - \
                        self.once_wechat_customer_service_data["qrCodeShowNum"]
        # 二维码长按识别数
        identifyQrCodeNum = self.second_wechat_customer_service_data["identifyQrCodeNum"] - \
                            self.once_wechat_customer_service_data["identifyQrCodeNum"]
        # 落地页链路成功加企业微信数
        landAddWorkWechatNum = self.second_wechat_customer_service_data["landAddWorkWechatNum"] - \
                               self.once_wechat_customer_service_data["landAddWorkWechatNum"]
        log.warning(f'微信客服列表断言判断：二维码展示数{qrCodeShowNum} 二维码长按识别数{identifyQrCodeNum} 落地页链路成功加企业微信数{landAddWorkWechatNum}')
        return True if qrCodeShowNum == 1 and identifyQrCodeNum == 1 and landAddWorkWechatNum == 1 else False


if __name__ == '__main__':
    c = CustomerService()
    c.once_wechat_customer_service("王新婷")
    c.second_wechat_customer_service("王新婷")

    print(c.assert_wechat_customer_service_list())
