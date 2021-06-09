# coding=gbk
import requests
import config
import json
from common.log import *

log = Log(__name__)
logger = log.Logger


# logger = setlogging(__name__)


class RequestApi(object):

    @staticmethod
    def request(method, uri, request_data):
        header = {
            "token": config.environment["test"]["token"]
        }
        request_url = config.environment["test"]["gateway"] + uri
        if method.lower() in ["post", "put"]:
            if type(request_data) == dict:
                request_data = json.dumps(request_data)
            try:
                res = requests.request(method, url=request_url,
                                       headers=header, json=json.loads(request_data.replace("\n", "")),
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
                                   headers=header, params=request_data, timeout=config.timeout)
            logger.info("请求方式：{}请求地址：{}请求参数：{}".format(method, request_url, request_data))
            return res

    @staticmethod
    def worker_requests(method, uri, request_data):
        header = {
            "deviceType": "Android",
            "versionCode": str(config.worker_environment["test"]["versionCode"]),
            "appProduct": "share",
            "Content-Type": "application/json",


            "token": config.worker_environment["test"]["token"]
        }
        worker_url = config.worker_environment["test"]["gateway"] + uri
        if method.lower() in ["post", "put"]:

            if type(request_data) == dict:
                request_data = json.dumps(request_data)

            res = requests.request(method, url=worker_url,
                                   headers=header, json=json.loads(request_data.replace("\n", "")),
                                   timeout=config.timeout)
            if uri not in ["/lbdj/app/order/AppGrabOrderHallApiRequest", "/lbdj/app/order/AppReservationApiRequest",
                           "/lbdj/app/order/AppMyOrderInfoApiRequest"]:
                print("请求方式：{} 请求地址：{} 请求参数：{}  返回结果：{}".format(method, worker_url, request_data.replace("\n", ""),
                                                                res.text))
            logger.info("请求方式：{}请求地址：{}请求参数：{}".format(method, worker_url, request_data.replace("\n", "")))
            return res
        elif method.lower() in ["get", "delete"]:
            res = requests.request(method, url=worker_url,
                                   headers=header, params=request_data, timeout=config.timeout)
            logger.info("请求方式：{}请求地址：{}请求参数：{}".format(method, worker_url, res))
            return res


if __name__ == '__main__':
    r = RequestApi()
    # d = '{"baseFeeList":null,"startMileage":"20","updateOrderInfo":null,"replenishFlag":false,"baseServeFee":60,"orderBaseFee":0,"noteList":[],"goodsTemplate":[{"templateName":"家具模板","goodsSpec":"1*5","goodsId":null,"goodsName":"自定义商品规格","imageUrl":"upload/template/20200907/DAD7A6A8C3E93DD4CE5F3611681B18CE_p167373.jpg","goodsCategoryId":"140","goodsCategoryName":"家具类","remark":"1231","contactName":null,"contactPhone":null,"goodsThirdId":"5032","goodsThirdName":"餐桌","goodsTypeId":"5003","goodsTypeName":"桌类","orderType":"1","azvideo":"1231","goodsSpecId":null,"wybnum":0,"wybprice":5,"wybMaxnum":30,"wybMaxpaymultiple":30,"wybMaxpayamount":4500,"unit":"个","goodslabel":"","goodsLabelList":[],"packageNum":null,"rewardMoney":""},{"templateName":"家具模板001","goodsSpec":"44","goodsId":null,"goodsName":"自定义商品规格","imageUrl":"upload/template/20200907/B80C97A5E52F6232B8AB5A2E6704E0D8_p167373.jpg","goodsCategoryId":"140","goodsCategoryName":"家具类","remark":"","contactName":null,"contactPhone":null,"goodsThirdId":"5024","goodsThirdName":"布艺床","goodsTypeId":"5002","goodsTypeName":"床类","orderType":"1","azvideo":"","goodsSpecId":null,"wybnum":0,"wybprice":5,"wybMaxnum":30,"wybMaxpaymultiple":30,"wybMaxpayamount":4500,"unit":"个","goodslabel":"","goodsLabelList":[],"packageNum":null,"rewardMoney":""},{"templateName":"家具模板003","goodsSpec":"1m≤长度≤1.5米","goodsId":null,"goodsName":"储物柜","imageUrl":"upload/order/20200907/xcx958620DC77B6EEF39DFD97B747C605F3_p167373.jpg","goodsCategoryId":"140","goodsCategoryName":"家具类","remark":"","contactName":null,"contactPhone":null,"goodsThirdId":"5021","goodsThirdName":"储物柜","goodsTypeId":"5001","goodsTypeName":"柜类","orderType":"1","azvideo":"","goodsSpecId":null,"wybnum":0,"wybprice":5,"wybMaxnum":30,"wybMaxpaymultiple":30,"wybMaxpayamount":4500,"unit":null,"goodslabel":"","goodsLabelList":[],"packageNum":null,"rewardMoney":""},{"templateName":"家具模板003","goodsSpec":"1m≤长度≤1.5米","goodsId":null,"goodsName":"储物柜","imageUrl":"upload/order/20200907/xcx958620DC77B6EEF39DFD97B747C605F3_p167373.jpg","goodsCategoryId":"140","goodsCategoryName":"家具类","remark":"","contactName":null,"contactPhone":null,"goodsThirdId":"5021","goodsThirdName":"储物柜","goodsTypeId":"5001","goodsTypeName":"柜类","orderType":"1","azvideo":"","goodsSpecId":null,"wybnum":0,"wybprice":5,"wybMaxnum":30,"wybMaxpaymultiple":30,"wybMaxpayamount":4500,"unit":null,"goodslabel":"","goodsLabelList":[],"packageNum":null,"rewardMoney":""},{"templateName":"家具模板003","goodsSpec":"1m≤长度≤1.5米","goodsId":null,"goodsName":"储物柜","imageUrl":"upload/order/20200907/xcx958620DC77B6EEF39DFD97B747C605F3_p167373.jpg","goodsCategoryId":"140","goodsCategoryName":"家具类","remark":"","contactName":null,"contactPhone":null,"goodsThirdId":"5021","goodsThirdName":"储物柜","goodsTypeId":"5001","goodsTypeName":"柜类","orderType":"1","azvideo":"","goodsSpecId":null,"wybnum":0,"wybprice":5,"wybMaxnum":30,"wybMaxpaymultiple":30,"wybMaxpayamount":4500,"unit":null,"goodslabel":"","goodsLabelList":[],"packageNum":null,"rewardMoney":""},{"templateName":"模板004","goodsSpec":"101","goodsId":null,"goodsName":"自定义商品规格","imageUrl":"upload/order/20200907/xcx8B3B06D47FBE34A14E9EB87DC651A6B0_p167373.jpg","goodsCategoryId":"140","goodsCategoryName":"家具类","remark":"","contactName":null,"contactPhone":null,"goodsThirdId":"5021","goodsThirdName":"储物柜","goodsTypeId":"5001","goodsTypeName":"柜类","orderType":"1","azvideo":"","goodsSpecId":null,"wybnum":0,"wybprice":5,"wybMaxnum":30,"wybMaxpaymultiple":30,"wybMaxpayamount":4500,"unit":null,"goodslabel":"","goodsLabelList":[],"packageNum":null,"rewardMoney":""}],"imgsTemplate":[],"cId":"140","serviceType":"anz","serviceTypeId":"0","psType":"","shopId":"","orderType":"1","orderPlatform":1,"customerName":"张三","customerPhone":"17786451825","provinceCode":52993,"cityCode":52994,"districtCode":52996,"provinceCodeText":"港澳","cityCodeText":"香港特别行政区","districtCodeText":"中西区","customerAddress":"前进一路前进二村前进小区","contactName":"技术支持","contactTel":"15666666666","customerDesc":"","isBatchOrder":0,"expectedTime":"","expectedOffer":"99","tmOrderId":"","tmVerify":0,"technicalContact":"","technicalContactPhone":"","orderGoodsDtos":[{"itemKey":1,"errorMsg":{"cateleavl2":"","cateleavl3":"","parentGoodId":"","goodsId":"","specName":"","quantity":"","lockAttr":"","lockType":"","therehook":""},"cateleavl2":"5003","cateleavl3":"5034","parentGoodId":"3201","parentGoodIdText":"\n            电动麻将桌\n          ","goodsId":"3202","goodsIdText":"1张","goodsName":"麻将桌","specName":"电动麻将桌/1张","uploadImgList":["upload/order/20201027/C652E472D8558AC9D99084F26EE3BCEE_p167373.png"],"img":"upload/order/20201027/C652E472D8558AC9D99084F26EE3BCEE_p167373.png","templateImgList":["upload/order/20201027/C652E472D8558AC9D99084F26EE3BCEE_p167373.png"],"imageTemplateId":"","installRequire":"","installRequireList":[],"quantity":1,"remark":"","lockAttr":"","lockType":"","wxType":"","addFeeDtos":[],"autofill":null,"fillImgData":null,"azvideo":"","floor":"","wybnum":0,"unit":"个","content":"","goodsLabelList":[],"goodsLabel":"","isSpecSelectMode":true,"isCurtainsLcType":"","therehook":""}],"vGoodsDtos":[],"isMakeGood":0,"ifurgent":0,"urgentFee":"","makeGoodMoney":"","whetherusepraisemoney":0,"lubanCardAccountId":"","isUseLubanCard":0,"lubanCardDiscount":0,"lubanCoin":0,"sdepositBalance":0,"sdepositdiscount":1,"isUseServiceDeposit":0,"sdepositexpirationTime":"","customerPayment":"","customerAliww":"","rewardMoney":"","expressCompany":"","expressNo":"","lastamont":"","sourceOrderId":"","lockList":{},"wxTypeList":[],"isRepeat":false,"isShowBatch":false,"isShowAddressWin":false,"mapSelectShowWin":false,"ignoreAddressWin":true,"ignoreMapSelect":true,"mapSelectOk":false,"azyjFee":null,"addressLists":[],"azArrivalGoods":"1","socketClient":null,"packageNum":"","associatedOrderId":"","isCurtainsLcType":""}'
    # x = r.request("post","/lbdj/web/saveOrder",d)
    for i in range(900):
        m = r.worker_requests("post","/lbdj/app/DecemberWorkerDrawHandleApiRequest",request_data={})
        print(m.text)
