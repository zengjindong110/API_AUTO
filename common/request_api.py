# coding=utf-8
import requests
import config
from common.log import *
from common.get_config_data import GetConfig

log = Log(__name__)
logger = log.Logger


# logger = setlogging(__name__)


class RequestApi(GetConfig):
    def __init__(self,file_name):
        self.header = {"authorization": dict(config.TOKEN)["token"]}
        super(RequestApi, self).__init__(file_name)
        self.gateway = self.get_config_data("USER")["HOST"]

    def request(self, data):
        """
        data ={'uri': '/api/v1/landing-page/landing-pages/pmp', 'method': 'post', 'data': {'aa': 'bb'}, 'assert': {'aa': 'bb'}, 'describe': '这是模板'}

        respond = self.request(data)
        """
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

                return res.text
        elif method.lower() in ["get", "delete"]:
            try:
                res = requests.request(method, url=request_url,
                                       headers=self.header, params=request_data, timeout=30)
                logger.info("请求方式：{}  请求地址：{}  请求参数：{}  返回参数：{}".format(method, request_url, request_data, res.text))
            except Exception as e:
                logger.warn(e)

            return res.text


if __name__ == '__main__':
    r = RequestApi("config.ini")

    a = {'uri': "/api/v1/marketing/advertiser-account-groups/collect/list", 'method': 'GET',
                'data': {"name": "api_test"}, 'assert': {'aa': 'bb'}, 'describe': '这是模板'}
    r.request(a)
