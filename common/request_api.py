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

    a = {'uri': '/api/v1/landing-page/landing-pages/pmp', 'method': 'POST', 'data': {'name': '1111111111111', 'landingPageGroupId': 0, 'advertiserAccountGroupId': '2'}, 'assert': {'id': 22, 'name': '1111111111111', 'title': None, 'content': None, 'bgColor': None, 'token': 'iviv0IQo', 'wechatDate': None, 'wechatLinkContent': None, 'wechatLinkAddress': None, 'advertiserAccountId': None, 'unreadCount': None, 'createdAt': '2021-11-15T17:45:35.441Z', 'updatedAt': '2021-11-15T17:45:35.441Z', 'creatorId': 1, 'version': 1, 'landingPageWidth': None, 'landingPageHeight': None, 'landingPageSize': None, 'bsId': None, 'recoveryAt': None, 'recoveryId': None, 'recoveryName': None, 'landingPageTop': None, 'landingPageGroupTop': None, 'wechatShareDesc': None, 'wechatShareImagePath': None, 'support': None, 'bgPic': None, 'limitFilling': None, 'wechatAppId': None, 'showOpenId': None, 'status': None, 'landingPageGroupName': None, 'landingPageGroupId': 0, 'access': None, 'convertCustomer': None, 'convertUrl': None, 'convertType': None, 'top': None, 'isGroupTop': None, 'fillNumNow': None, 'fillAllNums': None, 'fillNums': None, 'fillRate': None, 'pv': None, 'pvDay': None, 'pvNow': None, 'showFillData': None, 'identifyQrCodeNum': None, 'identifyQrCodeRate': None, 'addWorkWechatNum': None, 'addWorkWechatRate': None, 'remainTime': None, 'errors': None, 'rename': False, 'advertiserAccountGroupId': 2, 'platformId': None, 'promotionType': None, 'accountId': None, 'accountName': None, 'uploadConfigCopy': False, 'customCode': None, 'landingPageHosts': None, 'landingPageStrategys': [], 'templateIds': None, 'popupId': None, 'isJumpWechatApplet': None, 'wechatAppletLandingPageId': None, 'wechatAppletChannelId': None, 'wechatAppletChannelUrl': None}, 'describe': '创建落地页'}
    r.request(a)
