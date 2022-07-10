# coding=utf-8
import json

import requests

from common.connectdb import ConnectDb
from common.log import Log
from config.get_config_data import GetConfig

logger = Log(__file__)
GC = GetConfig()
gateway = GC.get_config_data("USER")["HOST"]
header = GC.get_header()
execution_sql = ConnectDb()


# 把参入参数中的filetering参数中的None改成null
def deal_with_filtering(data):
    if "filtering" in data.keys():
        filter_data = """{}""".format(str(data["filtering"]))
        data["filtering"] = filter_data.replace("None", "null")
    else:

        filter_data = """{}""".format(str(data))
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
        _id = 99

    data = request_data["data"]
    uri = request_data["uri"]
    method = request_data["method"].lower()
    # url = uri
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

        # logger.info("未处理之前的参数所有请求参数：{}".format(str(request_data)))

        _data = deal_with_data(request_data)
        logger.info(
            "请求地址：{} 请求方式：{} 请求参数：{}  请求头：{} \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t".format(
                _data["uri"], _data["method"], _data["data"], header))
        res = ""
        try:
            if _data["method"] in ["post", "put"]:

                res = requests.request(method=_data["method"], url=_data["uri"],
                                       headers=header, json=_data["data"],
                                       timeout=30)  # 如果要抓包就添加  ,proxies=proxies,verify=False
                logger.info("响应结果:{}".format(res.text))

            elif _data["method"] in ["get", "delete"]:
                res = requests.request(method=_data["method"], url=_data["uri"],
                                       headers=header, params=_data["data"], timeout=30)
                logger.info("响应结果:{}".format(res.text))

        except Exception:
            logger.error("请求的时候出错了出错了:{}".format(_data["method"]))

        try:
            json.loads(res.text)
            execution_sql.update_data(
                """UPDATE api_test SET respond = '{}' WHERE id = {}""".format(res.text, request_data["id"]))
        except ValueError:
            return res
        return res.json()



if __name__ == '__main__':
    r = RequestApi()
    b = {
        "content": "[{\"uuid\":\"64801ca7\",\"name\":\"OrderSpecification\",\"model\":{\"specs\":{\"defs\":[],\"prices\":[]}},\"version\":\"\"},{\"uuid\":\"a0b6816c\",\"name\":\"OrderAmount\",\"model\":{\"price\":\"1\",\"originalPrice\":\"1\",\"showPrice\":true,\"showOriginalPrice\":true,\"displayText\":\"\"},\"version\":\"\"},{\"uuid\":\"e7012bbf\",\"name\":\"OrderPurchaseQuantity\",\"model\":{\"show\":false},\"version\":\"\"},{\"uuid\":\"ec202599\",\"name\":\"OrderFormSetting\",\"model\":{\"show\":true,\"forms\":[{\"uuid\":\"e9945\",\"name\":\"InputName\",\"label\":\"姓名\",\"value\":\"姓名\",\"key\":\"name\",\"required\":true,\"titlePosition\":\"outside\"},{\"uuid\":\"j7798\",\"name\":\"InputPhone\",\"label\":\"手机号\",\"value\":\"手机号\",\"key\":\"phone\",\"required\":true,\"smsValue\":\"\",\"enableSmsValidation\":true,\"signatureId\":1,\"titlePosition\":\"outside\"},{\"uuid\":\"j9501\",\"name\":\"AreaSelect\",\"label\":\"地区\",\"value\":\"地区\",\"key\":\"areaSelect\",\"required\":true,\"enableGeoDetection\":false,\"titlePosition\":\"outside\"}],\"undefined\":\"地区\"},\"version\":\"\"},{\"uuid\":\"38833c70\",\"name\":\"OrderRemark\",\"model\":{\"show\":false,\"titlePosition\":\"outside\"},\"version\":\"\"},{\"uuid\":\"7423374c\",\"name\":\"OrderPaymentMethod\",\"model\":{\"show\":true,\"mode\":[{\"name\":\"货到付款\",\"checked\":true},{\"name\":\"微信支付\",\"checked\":false,\"disabled\":true},{\"name\":\"在线支付\",\"checked\":false}]},\"version\":\"\"},{\"uuid\":\"593df07a\",\"name\":\"OrderPurchaseButtonSetting\",\"model\":{\"text\":\"立即购买\"},\"version\":\"\"},{\"uuid\":\"fc5d9d84\",\"name\":\"OrderPurchaseRecord\",\"model\":{\"show\":false,\"orderRecordName\":\"\",\"orderRecordContent\":\"张***在 17:32 订购了订单模板一\",\"showRealRecords\":false,\"orderRecordTemplate\":\"\"},\"version\":\"\"}]",
        "ext": {"limitFilling": "null"}, "limitFilling": "null", "paymentType": "PING_PAY", "goodId": "null",
        "applicationId": "null", "version": 0}

    a = {'id': 102, 'uri': 'https://lpedit-asptest.yiye.ai/api/v1/landing-page/widget-templates/pmp/ORDER_TYPE/379',
         'method': 'put', 'data': {
            'content': '[{"uuid":"64801ca7","name":"OrderSpecification","model":{"specs":{"defs":[],"prices":[]}},"version":""},{"uuid":"a0b6816c","name":"OrderAmount","model":{"price":"1","originalPrice":"1","showPrice":true,"showOriginalPrice":true,"displayText":""},"version":""},{"uuid":"e7012bbf","name":"OrderPurchaseQuantity","model":{"show":false},"version":""},{"uuid":"ec202599","name":"OrderFormSetting","model":{"show":true,"forms":[{"uuid":"e9945","name":"InputName","label":"姓名","value":"姓名","key":"name","required":true,"titlePosition":"outside"},{"uuid":"j7798","name":"InputPhone","label":"手机号","value":"手机号","key":"phone","required":true,"smsValue":"","enableSmsValidation":true,"signatureId":1,"titlePosition":"outside"},{"uuid":"j9501","name":"AreaSelect","label":"地区","value":"地区","key":"areaSelect","required":true,"enableGeoDetection":false,"titlePosition":"outside"}],"undefined":"地区"},"version":""},{"uuid":"38833c70","name":"OrderRemark","model":{"show":false,"titlePosition":"outside"},"version":""},{"uuid":"7423374c","name":"OrderPaymentMethod","model":{"show":true,"mode":[{"name":"货到付款","checked":true},{"name":"微信支付","checked":false,"disabled":true},{"name":"在线支付","checked":false}]},"version":""},{"uuid":"593df07a","name":"OrderPurchaseButtonSetting","model":{"text":"立即购买"},"version":""},{"uuid":"fc5d9d84","name":"OrderPurchaseRecord","model":{"show":false,"orderRecordName":"","orderRecordContent":"张***在 17:32 订购了订单模板一","showRealRecords":false,"orderRecordTemplate":""},"version":""}]',
            'ext': {'limitFilling': 'null'}, 'limitFilling': 'null', 'paymentType': 'PING_PAY', 'goodId': 'null',
            'applicationId': 'null', 'version': 0}, 'assert': 1, 'describe': '将订单模板里面添加内容'}
    a["data"] = b
    r.request(a)
