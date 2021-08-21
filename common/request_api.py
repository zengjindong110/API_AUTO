# coding=gbk
import requests
import config
import json
from common.log import *
from common.get_config_data import *

log = Log(__name__)
logger = log.Logger


# logger = setlogging(__name__)


class RequestApi(object):
    def __init__(self):

        self.header = {"authorization": None}

    def request(self, method, uri, request_data):

        # request_url = config.environment["test"]["gateway"] + uri
        request_url = get_config_data("user")["host"] + uri
        if method.lower() in ["post", "put"]:
            if type(request_data) == dict:
                request_data = json.dumps(request_data)
            try:
                res = requests.request(method, url=request_url,
                                       headers=self.header, json=json.loads(request_data.replace("\n", "")),
                                       timeout=config.timeout)

            except KeyError as e:
                raise KeyError() from e

            print("����ʽ��{}  �����ַ��{}  ���������{}  ���ز�����{}".format(method, request_url, request_data.replace("\n", ""),
                                                              res.text))
            logger.info(
                "����ʽ��{}  �����ַ��{}  ���������{}  ���ز�����{}".format(method, request_url, request_data.replace("\n", ""),
                                                            res.text))
            return res
        elif method.lower() in ["get", "delete"]:
            res = requests.request(method, url=request_url,
                                   headers=self.header, params=request_data, timeout=config.timeout)
            logger.info("����ʽ��{}�����ַ��{}���������{}".format(method, request_url, request_data))
            return res


if __name__ == '__main__':
    r =  RequestApi()
    r.request(post  )
