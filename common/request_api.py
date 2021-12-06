# coding=utf-8
import requests

import config
from common.connectdb import ConnectDb
from common.get_config_data import GetConfig
from common.log import *

log = Log(__name__)
logger = log.Logger

# logger = setlogging(__name__)

GC = GetConfig()
gateway = GC.get_config_data("USER")["HOST"]
header = {"authorization": dict(config.TOKEN)["token"]}
CD = ConnectDb()


class RequestApi(object):
    # def __init__(self):
    #     # super(RequestApi, self).__init__()
    #     self.
    #
    #     self.gateway = GC.get_config_data("USER")["HOST"]
    @staticmethod
    def deal_with_data(request_data):
        _data = {}
        _id = request_data["id"]
        data = request_data["data"]
        uri = request_data["uri"]
        method = request_data["method"].lower()
        if "advertiserGroupId" in data.keys():
            advertiser_group_id = CD.get_pmp_id()
            data["advertiserGroupId"] = advertiser_group_id
        if "http" in uri:
            url = uri
        else:
            url = gateway + uri

        _data["url"] = url
        _data["method"] = method
        _data["data"] = data
        _data["id"] = _id
        return _data

    def request(self, request_data):
        """
        data ={'id':1,'uri': '/api/v1/landing-page/landing-pages/pmp', 'method': 'post', 'data': {'aa': 'bb'}, 'assert': {'aa': 'bb'}, 'describe': '这是模板'}

        respond = self.request(data)
        """

        _data = self.deal_with_data(request_data)

        if _data["method"] in ["post", "put"]:
            if type(_data) == dict:

                try:
                    res = requests.request(_data["method"], url=_data["url"],
                                           headers=header, json=_data["data"],
                                           timeout=30)
                    logger.info(
                        "请求方式：{}  请求地址：{}  请求参数：{}  返回参数：{}".format(_data["method"], _data["url"], request_data,
                                                                    res.text))
                except Exception as e:
                    logger.warn(e)

                CD.update_data(
                    """UPDATE asp_saas_zjd.api_test SET respond = '{}' WHERE id = {}""".format(res.text,
                                                                                               request_data["id"]))
                return res
        elif _data["method"] in ["get", "delete"]:
            try:
                res = requests.request(_data["method"], url=_data["url"],
                                       headers=header, params=_data["data"], timeout=30)
                logger.info(
                    "请求方式：{}  请求地址：{}  请求参数：{}  返回参数：{}".format(_data["method"], _data["url"], request_data, res.text))

            except Exception as e:
                logger.warn(e)

            # insert_data = res.text

            CD.update_data(
                """UPDATE asp_saas_zjd.api_test SET respond = '{}' WHERE id = {}""".format(res.text,
                                                                                           request_data["id"]))
            return res


if __name__ == '__main__':
    r = RequestApi()

    a = {"id": 9999, 'uri': "/api/v1/landing-page/landing-pages/pmp", 'method': 'get',
         'data': {"name": "api_test", "advertiserGroupId": 1233}, 'assert': {'aa': 'bb'}, 'describe': '这是模板', }
    r.request(a)
