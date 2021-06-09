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

            print("����ʽ��{}  �����ַ��{}  ���������{}  ���ز�����{}".format(method, request_url, request_data.replace("\n", ""),
                                                              res.text))
            logger.info(
                "����ʽ��{}  �����ַ��{}  ���������{}  ���ز�����{}".format(method, request_url, request_data.replace("\n", ""),
                                                            res.text))
            return res
        elif method.lower() in ["get", "delete"]:
            res = requests.request(method, url=request_url,
                                   headers=header, params=request_data, timeout=config.timeout)
            logger.info("����ʽ��{}�����ַ��{}���������{}".format(method, request_url, request_data))
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
                print("����ʽ��{} �����ַ��{} ���������{}  ���ؽ����{}".format(method, worker_url, request_data.replace("\n", ""),
                                                                res.text))
            logger.info("����ʽ��{}�����ַ��{}���������{}".format(method, worker_url, request_data.replace("\n", "")))
            return res
        elif method.lower() in ["get", "delete"]:
            res = requests.request(method, url=worker_url,
                                   headers=header, params=request_data, timeout=config.timeout)
            logger.info("����ʽ��{}�����ַ��{}���������{}".format(method, worker_url, res))
            return res


if __name__ == '__main__':
    r = RequestApi()
    # d = '{"baseFeeList":null,"startMileage":"20","updateOrderInfo":null,"replenishFlag":false,"baseServeFee":60,"orderBaseFee":0,"noteList":[],"goodsTemplate":[{"templateName":"�Ҿ�ģ��","goodsSpec":"1*5","goodsId":null,"goodsName":"�Զ�����Ʒ���","imageUrl":"upload/template/20200907/DAD7A6A8C3E93DD4CE5F3611681B18CE_p167373.jpg","goodsCategoryId":"140","goodsCategoryName":"�Ҿ���","remark":"1231","contactName":null,"contactPhone":null,"goodsThirdId":"5032","goodsThirdName":"����","goodsTypeId":"5003","goodsTypeName":"����","orderType":"1","azvideo":"1231","goodsSpecId":null,"wybnum":0,"wybprice":5,"wybMaxnum":30,"wybMaxpaymultiple":30,"wybMaxpayamount":4500,"unit":"��","goodslabel":"","goodsLabelList":[],"packageNum":null,"rewardMoney":""},{"templateName":"�Ҿ�ģ��001","goodsSpec":"44","goodsId":null,"goodsName":"�Զ�����Ʒ���","imageUrl":"upload/template/20200907/B80C97A5E52F6232B8AB5A2E6704E0D8_p167373.jpg","goodsCategoryId":"140","goodsCategoryName":"�Ҿ���","remark":"","contactName":null,"contactPhone":null,"goodsThirdId":"5024","goodsThirdName":"���մ�","goodsTypeId":"5002","goodsTypeName":"����","orderType":"1","azvideo":"","goodsSpecId":null,"wybnum":0,"wybprice":5,"wybMaxnum":30,"wybMaxpaymultiple":30,"wybMaxpayamount":4500,"unit":"��","goodslabel":"","goodsLabelList":[],"packageNum":null,"rewardMoney":""},{"templateName":"�Ҿ�ģ��003","goodsSpec":"1m�ܳ��ȡ�1.5��","goodsId":null,"goodsName":"�����","imageUrl":"upload/order/20200907/xcx958620DC77B6EEF39DFD97B747C605F3_p167373.jpg","goodsCategoryId":"140","goodsCategoryName":"�Ҿ���","remark":"","contactName":null,"contactPhone":null,"goodsThirdId":"5021","goodsThirdName":"�����","goodsTypeId":"5001","goodsTypeName":"����","orderType":"1","azvideo":"","goodsSpecId":null,"wybnum":0,"wybprice":5,"wybMaxnum":30,"wybMaxpaymultiple":30,"wybMaxpayamount":4500,"unit":null,"goodslabel":"","goodsLabelList":[],"packageNum":null,"rewardMoney":""},{"templateName":"�Ҿ�ģ��003","goodsSpec":"1m�ܳ��ȡ�1.5��","goodsId":null,"goodsName":"�����","imageUrl":"upload/order/20200907/xcx958620DC77B6EEF39DFD97B747C605F3_p167373.jpg","goodsCategoryId":"140","goodsCategoryName":"�Ҿ���","remark":"","contactName":null,"contactPhone":null,"goodsThirdId":"5021","goodsThirdName":"�����","goodsTypeId":"5001","goodsTypeName":"����","orderType":"1","azvideo":"","goodsSpecId":null,"wybnum":0,"wybprice":5,"wybMaxnum":30,"wybMaxpaymultiple":30,"wybMaxpayamount":4500,"unit":null,"goodslabel":"","goodsLabelList":[],"packageNum":null,"rewardMoney":""},{"templateName":"�Ҿ�ģ��003","goodsSpec":"1m�ܳ��ȡ�1.5��","goodsId":null,"goodsName":"�����","imageUrl":"upload/order/20200907/xcx958620DC77B6EEF39DFD97B747C605F3_p167373.jpg","goodsCategoryId":"140","goodsCategoryName":"�Ҿ���","remark":"","contactName":null,"contactPhone":null,"goodsThirdId":"5021","goodsThirdName":"�����","goodsTypeId":"5001","goodsTypeName":"����","orderType":"1","azvideo":"","goodsSpecId":null,"wybnum":0,"wybprice":5,"wybMaxnum":30,"wybMaxpaymultiple":30,"wybMaxpayamount":4500,"unit":null,"goodslabel":"","goodsLabelList":[],"packageNum":null,"rewardMoney":""},{"templateName":"ģ��004","goodsSpec":"101","goodsId":null,"goodsName":"�Զ�����Ʒ���","imageUrl":"upload/order/20200907/xcx8B3B06D47FBE34A14E9EB87DC651A6B0_p167373.jpg","goodsCategoryId":"140","goodsCategoryName":"�Ҿ���","remark":"","contactName":null,"contactPhone":null,"goodsThirdId":"5021","goodsThirdName":"�����","goodsTypeId":"5001","goodsTypeName":"����","orderType":"1","azvideo":"","goodsSpecId":null,"wybnum":0,"wybprice":5,"wybMaxnum":30,"wybMaxpaymultiple":30,"wybMaxpayamount":4500,"unit":null,"goodslabel":"","goodsLabelList":[],"packageNum":null,"rewardMoney":""}],"imgsTemplate":[],"cId":"140","serviceType":"anz","serviceTypeId":"0","psType":"","shopId":"","orderType":"1","orderPlatform":1,"customerName":"����","customerPhone":"17786451825","provinceCode":52993,"cityCode":52994,"districtCode":52996,"provinceCodeText":"�۰�","cityCodeText":"����ر�������","districtCodeText":"������","customerAddress":"ǰ��һ·ǰ������ǰ��С��","contactName":"����֧��","contactTel":"15666666666","customerDesc":"","isBatchOrder":0,"expectedTime":"","expectedOffer":"99","tmOrderId":"","tmVerify":0,"technicalContact":"","technicalContactPhone":"","orderGoodsDtos":[{"itemKey":1,"errorMsg":{"cateleavl2":"","cateleavl3":"","parentGoodId":"","goodsId":"","specName":"","quantity":"","lockAttr":"","lockType":"","therehook":""},"cateleavl2":"5003","cateleavl3":"5034","parentGoodId":"3201","parentGoodIdText":"\n            �綯�齫��\n          ","goodsId":"3202","goodsIdText":"1��","goodsName":"�齫��","specName":"�綯�齫��/1��","uploadImgList":["upload/order/20201027/C652E472D8558AC9D99084F26EE3BCEE_p167373.png"],"img":"upload/order/20201027/C652E472D8558AC9D99084F26EE3BCEE_p167373.png","templateImgList":["upload/order/20201027/C652E472D8558AC9D99084F26EE3BCEE_p167373.png"],"imageTemplateId":"","installRequire":"","installRequireList":[],"quantity":1,"remark":"","lockAttr":"","lockType":"","wxType":"","addFeeDtos":[],"autofill":null,"fillImgData":null,"azvideo":"","floor":"","wybnum":0,"unit":"��","content":"","goodsLabelList":[],"goodsLabel":"","isSpecSelectMode":true,"isCurtainsLcType":"","therehook":""}],"vGoodsDtos":[],"isMakeGood":0,"ifurgent":0,"urgentFee":"","makeGoodMoney":"","whetherusepraisemoney":0,"lubanCardAccountId":"","isUseLubanCard":0,"lubanCardDiscount":0,"lubanCoin":0,"sdepositBalance":0,"sdepositdiscount":1,"isUseServiceDeposit":0,"sdepositexpirationTime":"","customerPayment":"","customerAliww":"","rewardMoney":"","expressCompany":"","expressNo":"","lastamont":"","sourceOrderId":"","lockList":{},"wxTypeList":[],"isRepeat":false,"isShowBatch":false,"isShowAddressWin":false,"mapSelectShowWin":false,"ignoreAddressWin":true,"ignoreMapSelect":true,"mapSelectOk":false,"azyjFee":null,"addressLists":[],"azArrivalGoods":"1","socketClient":null,"packageNum":"","associatedOrderId":"","isCurtainsLcType":""}'
    # x = r.request("post","/lbdj/web/saveOrder",d)
    for i in range(900):
        m = r.worker_requests("post","/lbdj/app/DecemberWorkerDrawHandleApiRequest",request_data={})
        print(m.text)
