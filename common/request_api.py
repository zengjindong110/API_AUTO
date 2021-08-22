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

        self.header = {"authorization": None}

    def request(self, method, uri, request_data):

        # request_url = config.environment["test"]["gateway"] + uri
        parent_directory = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

        GC = GetConfig(parent_directory)
        request_url = GC.get_config_data("USER")["HOST"] + uri
        if method.lower() in ["post", "put"]:
            if type(request_data) == dict:
                request_data = json.dumps(request_data)
            try:
                res = requests.request(method, url=request_url,
                                       headers=self.header, json=json.loads(request_data.replace("\n", "")),
                                       timeout=config.timeout)

            except KeyError as e:
                raise KeyError() from e

            print("请求方式：{}  请求地址：{}  请求参数：{}  返回参数：{}".format(method, request_url, request_data.replace("\n", ""),
                                                              res.text))
            logger.info(
                "请求方式：{}  请求地址：{}  请求参数：{}  返回参数：{}".format(method, request_url, request_data.replace("\n", ""),
                                                            res.text))
            return res
        elif method.lower() in ["get", "delete"]:
            res = requests.request(method, url=request_url,
                                   headers=self.header, params=request_data, timeout=config.timeout)
            logger.info("请求方式：{}请求地址：{}请求参数：{}".format(method, request_url, request_data))
            return res


if __name__ == '__main__':
    r =  RequestApi()
    r.request("POST","http://www.baidu.com",{"a":"b"})
