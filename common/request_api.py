# coding=utf-8
import requests
import config
from common.log import *
from common.get_config_data import GetConfig
from common.connectdb import ConnectDb

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

    def request(self, request_data):
        """
        data ={'uri': '/api/v1/landing-page/landing-pages/pmp', 'method': 'post', 'data': {'aa': 'bb'}, 'assert': {'aa': 'bb'}, 'describe': '这是模板'}

        respond = self.request(data)
        """
        res = ""
        uri = request_data["uri"]
        method = request_data["method"]

        if "data" in request_data.keys():

            data = request_data["data"]
            print(111, data)
            if "advertiserGroupId" in data.keys():
                advertiserGroupId = CD.get_pmp_id()
                print(advertiserGroupId)
                data["advertiserGroupId"] = advertiserGroupId

        else:
            request_data = ""
        if "http" in uri:
            request_url = uri
        else:
            request_url = gateway + uri
        if method.lower() in ["post", "put"]:
            if type(request_data) == dict:

                try:
                    res = requests.request(method, url=request_url,
                                           headers=header, json=data,
                                           timeout=30)
                    logger.info(
                        "请求方式：{}  请求地址：{}  请求参数：{}  返回参数：{}".format(method, request_url, request_data,
                                                                    res.text))
                except Exception as e:
                    logger.warn(e)

                # print("请求方式：{}  请求地址：{}  请求参数：{}  返回参数：{}".format(method, request_url, request_data.replace("\n", ""),
                #                                                   res.text))
                CD.update_data(
                    """UPDATE asp_saas_zjd.api_test SET respond = '{}' WHERE id = {}""".format(res.text,
                                                                                               request_data["id"]))
                return res
        elif method.lower() in ["get", "delete"]:
            try:
                res = requests.request(method, url=request_url,
                                       headers=header, params=data, timeout=30)
                logger.info("请求方式：{}  请求地址：{}  请求参数：{}  返回参数：{}".format(method, request_url, request_data, res.text))
            except Exception as e:
                logger.warn(e)
            CD.update_data(
                """UPDATE asp_saas_zjd.api_test SET respond = '{}' WHERE id = {}""".format(res.text,
                                                                                           request_data["id"]))
            return res


if __name__ == '__main__':
    r = RequestApi()

    a = {"id": 9999, 'uri': "/api/v1/landing-page/landing-pages/pmp", 'method': 'get',
         'data': {"name": "api_test", "advertiserGroupId": 1233}, 'assert': {'aa': 'bb'}, 'describe': '这是模板', }
    r.request(a)
