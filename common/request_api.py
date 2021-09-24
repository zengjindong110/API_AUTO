# coding=utf-8
import requests
import config
from common.log import *
from common.get_config_data import GetConfig

log = Log(__name__)
logger = log.Logger


# logger = setlogging(__name__)


class RequestApi(GetConfig):
    def __init__(self):
        self.header = {"authorization": dict(config.TOKEN)["token"]}
        super(RequestApi, self).__init__(None)
        self.gateway = self.get_config_data("USER")["HOST"]

    def request(self, data):

        res = ""
        uri = data["uri"]
        method = data["method"]
        if "data" in data.keys():
            request_data = data["data"]
        else:
            request_data = ""
        if "http" in uri:
            request_url = uri
        else:
            request_url = self.gateway + uri
        if method.lower() in ["post", "put"]:
            if type(request_data) == dict:

                try:
                    res = requests.request(method, url=request_url,
                                           headers=self.header, json=request_data,
                                           timeout=30)
                    logger.info(
                        "请求方式：{}  请求地址：{}  请求参数：{}  返回参数：{}".format(method, request_url, request_data,
                                                                    res.text))
                except Exception as e:
                    logger.warn(e)

                # print("请求方式：{}  请求地址：{}  请求参数：{}  返回参数：{}".format(method, request_url, request_data.replace("\n", ""),
                #                                                   res.text))

                return res
        elif method.lower() in ["get", "delete"]:
            try:
                res = requests.request(method, url=request_url,
                                       headers=self.header, params=request_data, timeout=30)
                logger.info("请求方式：{}  请求地址：{}  请求参数：{}  返回参数：{}".format(method, request_url, request_data, res.text))
            except Exception as e:
                logger.warn(e)

            return res


if __name__ == '__main__':
    r = RequestApi()

    a = {'uri': '/api/v1/landing-page/widget-templates/PMP/ORDER_TYPE', 'method': 'post',
         'data': {'advertiserAccountGroupId': '8', 'name': '323', 'wtType': 'ORDER_TYPE'},
         'assert': {'id': 57, 'name': '323', 'content': None, 'advertiserAccountId': None,
                    'advertiserAccountGroupId': 8, 'usedColumns': None, 'usedColumnDescs': None, 'creatorId': 1,
                    'status': None, 'version': None, 'wtType': 'ORDER_TYPE', 'goodId': None, 'paymentType': None,
                    'applicationId': None, 'ext': None, 'createdAt': '2021-08-27T07:58:41.615Z',
                    'updatedAt': '2021-08-27T07:58:41.615Z', 'pingAppId': None, 'applicationName': None,
                    'accountId': None, 'accountName': None, 'orderQueryType': None, 'updateGood': False,
                    'limitFilling': False, 'productId': None, 'merchantId': None, 'merchantName': None,
                    'officialId': None, 'draft': True, 'errors': None, 'order': None, 'sort': None,
                    'landingPageId': None, 'advertiserAccountGroupIds': None, 'domain': None}, 'describe': '创建订单模板名称'}
    r.request(a)
