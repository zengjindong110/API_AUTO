# coding=gbk
import json
import config
import time
from common.request_api import RequestApi
from common.get_request_data import *


def get_code(orderId):
    data = {"orderId": orderId}
    return RequestApi.request("post", "/lbdj/web/getConfirmationCode", data).json()["t"]


def is_grabStatus(order_list):
    for order in order_list:
        if order["orderNum"].startswith("S1") or order["orderNum"].startswith("S3") and order["grabStatus"][0] == "待抢单":
            return order
        else:
            return False


def appointment_time():
    import datetime
    return str(datetime.datetime.now())[:10] + ",21:00+-+23:00"


def get_vip_order(catIdList, serviceTypeList):
    page = 1
    order_data = {"token": config.worker_environment["test"]["token"], "type": '4', "size": "20",
                  "page": str(page),
                  "catIdList": [catIdList], "regionIdList": [], "serviceTypeList": [serviceTypeList]}

    while True:
        order_data["page"] = page
        order_res = RequestApi.worker_requests("post", "/lbdj/app/order/AppGrabOrderHallApiRequest", order_data)
        order_list = order_res.json()["data"]
        print(order_list)

        if type(order_list) == list and order_list:

            order = is_grabStatus(order_list)

            if order:
                return order
            else:
                page += 1

        else:

            break


def get_order(catIdList="", serviceTypeList="", order_type='0'):
    """
    查看订单大厅订单
    :param order_type: 查询类型：0.一口价(悬赏也是一口价) 1.报价 2.指派 4.保证金专区
    :param catIdList: {"窗帘类"："136","灯具类":"138","晾衣架类":"139","家具类":"140",
                    "地板类":"141","墙纸类":"142","门类":"143","吊顶类":"144","家电类":"148",
                    "净水器":"137","锁类":"149","卫浴类":"202","定制家具":"135"}
    :param serviceTypeList: 订单服务类型（anz:安装,wx:维修,ps:配送,cz:配送+安装,lc:量尺）
     :return: 返回所有订单---过滤掉已经抢了的订单
    """

    page = 1
    if catIdList == "":
        catIdList = []

        serviceTypeList = []
    else:
        catIdList, serviceTypeList = [catIdList], [serviceTypeList]
    order_data = {"token": config.worker_environment["test"]["token"], "type": order_type, "size": "20",
                  "page": str(page),
                  "catIdList": catIdList, "regionIdList": [], "serviceTypeList": serviceTypeList}

    while True:
        order_data["page"] = page
        order_res = RequestApi.worker_requests("post", "/lbdj/app/order/AppGrabOrderHallApiRequest", order_data)

        order_list = order_res.json()["data"]

        if type(order_list) == list:

            order = is_grabStatus(order_list)

            if order:
                return order
            else:
                page += 1
                if page == 3:
                    order = get_vip_order(catIdList[0], serviceTypeList[0])
                    if order:
                        return order
                    else:
                        return {'id': '没有该品类订单', 'orderNum': '{}'.format(order_res.text)}

        else:
            return {'id': '没有该品类订单', 'orderNum': '{}'.format(order_res.text)}

        # else:
        #
        #     order = get_vip_order(catIdList, serviceTypeList)
        #
        #     if order:
        #         return order
        #     else:
        #         return {'id': 'error', 'orderNum': '{}'.format(order_res.text)}


def reserve_HomeCheck(order):
    """
    抢单，预约时间，上门打卡 一起写的在一个方法里面
    :param order:
    :return:
    """
    time.sleep(12)
    GrabOrderData = get_request_data("/lbdj/app/order/AppGrabOrderApiRequest")[0]  # 查询数据库参数

    order_id = order["id"]
    request_data = json.loads(GrabOrderData["data"])

    request_data["orderId"] = order_id  # 更换请求参数里面的"orderId"

    RequestApi.worker_requests(GrabOrderData["method"], GrabOrderData["uri"], request_data)  # 抢单

    appointmentData = get_request_data("/lbdj/app/order/AppReservationApiRequest")[0]  # 获取预约上门的请求参数
    appointmentReq = json.loads(appointmentData["data"])
    appointmentReq["planTime"] = appointment_time()
    appointmentReq["orderId"] = order_id

    RequestApi.worker_requests(appointmentData["method"], appointmentData["uri"],
                               appointmentReq)  # 电话预约上门时间

    HomeCheckData = get_request_data("/lbdj/app/order/AppHomeCheckApiRequest")[0]  # 获取上门打卡的请求参数
    HomeCheckReq = json.loads(HomeCheckData["data"])
    HomeCheckReq["orderId"] = order_id
    HomeCheckReq["snCodeList"] = [snCodeList(order_id, order["orderNum"])]

    RequestApi.worker_requests(HomeCheckData["method"], HomeCheckData["uri"], HomeCheckReq)  # 上门打卡


def my_order_info(order_id, orderSn):
    snCodeListReq = {"orderId": order_id, "orderSn": orderSn}
    order_list_res = RequestApi.worker_requests("post", "/lbdj/app/order/AppMyOrderInfoApiRequest", snCodeListReq)

    return order_list_res.json()["data"]["goodsList"][0]


def snCodeList(order_id, orderSn):
    order_list = my_order_info(order_id, orderSn)
    # {"orderId":"1318175099890696262","goodsName":"儿童学习桌套装","productDetailId":null,"snCode":""}
    return {"orderId": order_list['orderGoodsId'], "goodsName": order_list["goodsName"], "productDetailId": "",
            "snCode": ""}


def ServiceDone(order):
    ServiceDoneData = get_request_data("/lbdj/app/order/AppServiceDoneApiRequest")[0]  # 获取完工参数
    ServiceDoneReq = json.loads(ServiceDoneData["data"])
    ServiceDoneReq["orderId"] = order["id"]
    ServiceDoneReq["wcCode"] = get_code(order["id"])
    ServiceDoneReq["orderSn"] = order["orderNum"]
    respond = RequestApi.worker_requests(ServiceDoneData["method"], ServiceDoneData["uri"],
                                         ServiceDoneReq).json()  # 输入验证码确认完工
    return respond


if __name__ == '__main__':
    d = get_order("149", "anz")
    print(d)
