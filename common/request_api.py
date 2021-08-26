# coding=utf-8
import requests
import config
import json
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
        request_data = data["data"]
        request_url = self.gateway + uri
        if method.lower() in ["post", "put"]:
            if type(request_data) == dict:

                try:
                    res = requests.request(method, url=request_url,
                                           headers=self.header, json=json.loads(request_data.replace("\n", "")),
                                           timeout=30)
                    logger.info(
                        "请求方式：{}  请求地址：{}  请求参数：{}  返回参数：{}".format(method, request_url, request_data.replace("\n", ""),
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
                logger.info("请求方式：{}请求地址：{}请求参数：{}".format(method, request_url, request_data))
            except Exception as e:
                logger.warn(e)

            return res


if __name__ == '__main__':
    r = RequestApi()

    a = {'page': '1', 'size': '20', 'sort': 'pv', 'order': 'desc', 'name': ''}
    r.request(a)
