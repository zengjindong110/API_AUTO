# coding=utf-8
import json

import requests

from common.connectdb import ConnectDb
from common.log import Log
from common.get_config_data import GetConfig

logger = Log(__file__)
GC = GetConfig()
gateway = GC.get_config_data("USER")["HOST"]
header = GC.get_header()

execution_sql = ConnectDb()


# 把参入参数中的filetering参数中的None改成null
def deal_with_filtering(data):
    if "filtering" in data.keys():
        filter_data = f"""{str(data["filtering"])}"""
        data["filtering"] = filter_data.replace("None", "null")
    else:

        filter_data = f"""{str(data)}"""
        data = filter_data.replace("None", "null")


# 把接口中含有pmpid的字段都改成固定的pmpid
def deal_with_advertiser_group_id(data):
    if "advertiserAccountGroupId" in data.keys():
        advertiser_group_id = GC.get_pmp_id()
        data["advertiserAccountGroupId"] = advertiser_group_id


def deal_with_data(request_data):
    _data = {}
    if "id" in request_data.keys():
        _id = request_data["id"]
    else:
        _id = 9999

    data = request_data["data"]
    uri = request_data["uri"]
    method = request_data["method"].lower()
    if "http" in uri:
        url = uri
    else:
        url = gateway + uri
    # 查看请求参数的类型
    request_data_type = type(data)
    # 如果请求参数是dict类型参数
    if request_data_type == dict:
        # 改变项目id
        deal_with_advertiser_group_id(data)
        deal_with_filtering(data)

    # 如果请求的body为列表，处理列表的数据
    elif request_data_type == list:
        for request_dict in request_data["data"]:
            deal_with_advertiser_group_id(request_dict)
            deal_with_filtering(request_dict)

    _data["uri"] = url
    _data["method"] = method
    _data["data"] = data
    _data["id"] = _id
    return _data


proxies = {'http': 'http://localhost:8888', 'https': 'http://localhost:8888'}


class RequestApi(object):
    def __init__(self):
        # 为了抓包使用了代理

        # self.proxies = None
        pass

    def request(self, request_data):
        """
        data ={'id':1,'uri': '/api/v1/landing-page/landing-pages/pmp', 'method': 'post', 'data': {'aa': 'bb'}, 'assert': {'aa': 'bb'}, 'describe': '这是模板'}

        respond = self.request(data)
        """
        if type(request_data) == list:
            request_data = request_data[0]
        _data = deal_with_data(request_data)
        logger.info(
            f'请求地址：{_data["uri"]} 请求方式：{_data["method"]} 请求参数：{_data["data"]}  请求头：{header}')
        res = ""
        try:
            if _data["method"] in ["post", "put"]:

                res = requests.request(method=_data["method"], url=_data["uri"],
                                       headers=header, json=_data["data"],
                                       timeout=30)  # 如果要抓包就添加  ,proxies=proxies,verify=False
                logger.info(f"响应结果:{res.text}")

            elif _data["method"] in ["get", "delete"]:
                res = requests.request(method=_data["method"], url=_data["uri"],
                                       headers=header, params=_data["data"], timeout=30)

                logger.info(f"响应结果:{res.text}")

        except Exception:
            logger.error(f"请求的时候出错了出错了:{_data}")

        try:
            json.loads(res.text)
            execution_sql.update_data(
                f"""UPDATE api_auto_test SET respond = '{res.text}' WHERE id = { request_data["id"]}""")
        except ValueError:
            return res
        return res.json()



if __name__ == '__main__':
    r = RequestApi()
    a = {'id': 1, 'uri': '/api/v1/marketing/advertiser-account-groups/collect/list', 'method': 'get', 'data': {'page': 1, 'size': 20, 'sort': 'pv', 'order': 'desc', 'name': 'api_test', 'startTime': '2022-10-16', 'endTime': '2022-10-16'}, 'assert': {'name': 'test1111', 'advertiserAccountIndustryId': 2, 'managerList': [], 'leaderId': None, 'advertiserAccountIds': [], 'target': []}, 'describe': '搜索pmp账号接口有没有“api_test”的账号'}
    r.request(a)
