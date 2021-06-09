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
        if order["orderNum"].startswith("S1") or order["orderNum"].startswith("S3") and order["grabStatus"][0] == "������":
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
    �鿴������������
    :param order_type: ��ѯ���ͣ�0.һ�ڼ�(����Ҳ��һ�ڼ�) 1.���� 2.ָ�� 4.��֤��ר��
    :param catIdList: {"������"��"136","�ƾ���":"138","���¼���":"139","�Ҿ���":"140",
                    "�ذ���":"141","ǽֽ��":"142","����":"143","������":"144","�ҵ���":"148",
                    "��ˮ��":"137","����":"149","��ԡ��":"202","���ƼҾ�":"135"}
    :param serviceTypeList: �����������ͣ�anz:��װ,wx:ά��,ps:����,cz:����+��װ,lc:���ߣ�
     :return: �������ж���---���˵��Ѿ����˵Ķ���
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
                        return {'id': 'û�и�Ʒ�ඩ��', 'orderNum': '{}'.format(order_res.text)}

        else:
            return {'id': 'û�и�Ʒ�ඩ��', 'orderNum': '{}'.format(order_res.text)}

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
    ������ԤԼʱ�䣬���Ŵ� һ��д����һ����������
    :param order:
    :return:
    """
    time.sleep(12)
    GrabOrderData = get_request_data("/lbdj/app/order/AppGrabOrderApiRequest")[0]  # ��ѯ���ݿ����

    order_id = order["id"]
    request_data = json.loads(GrabOrderData["data"])

    request_data["orderId"] = order_id  # ����������������"orderId"

    RequestApi.worker_requests(GrabOrderData["method"], GrabOrderData["uri"], request_data)  # ����

    appointmentData = get_request_data("/lbdj/app/order/AppReservationApiRequest")[0]  # ��ȡԤԼ���ŵ��������
    appointmentReq = json.loads(appointmentData["data"])
    appointmentReq["planTime"] = appointment_time()
    appointmentReq["orderId"] = order_id

    RequestApi.worker_requests(appointmentData["method"], appointmentData["uri"],
                               appointmentReq)  # �绰ԤԼ����ʱ��

    HomeCheckData = get_request_data("/lbdj/app/order/AppHomeCheckApiRequest")[0]  # ��ȡ���Ŵ򿨵��������
    HomeCheckReq = json.loads(HomeCheckData["data"])
    HomeCheckReq["orderId"] = order_id
    HomeCheckReq["snCodeList"] = [snCodeList(order_id, order["orderNum"])]

    RequestApi.worker_requests(HomeCheckData["method"], HomeCheckData["uri"], HomeCheckReq)  # ���Ŵ�


def my_order_info(order_id, orderSn):
    snCodeListReq = {"orderId": order_id, "orderSn": orderSn}
    order_list_res = RequestApi.worker_requests("post", "/lbdj/app/order/AppMyOrderInfoApiRequest", snCodeListReq)

    return order_list_res.json()["data"]["goodsList"][0]


def snCodeList(order_id, orderSn):
    order_list = my_order_info(order_id, orderSn)
    # {"orderId":"1318175099890696262","goodsName":"��ͯѧϰ����װ","productDetailId":null,"snCode":""}
    return {"orderId": order_list['orderGoodsId'], "goodsName": order_list["goodsName"], "productDetailId": "",
            "snCode": ""}


def ServiceDone(order):
    ServiceDoneData = get_request_data("/lbdj/app/order/AppServiceDoneApiRequest")[0]  # ��ȡ�깤����
    ServiceDoneReq = json.loads(ServiceDoneData["data"])
    ServiceDoneReq["orderId"] = order["id"]
    ServiceDoneReq["wcCode"] = get_code(order["id"])
    ServiceDoneReq["orderSn"] = order["orderNum"]
    respond = RequestApi.worker_requests(ServiceDoneData["method"], ServiceDoneData["uri"],
                                         ServiceDoneReq).json()  # ������֤��ȷ���깤
    return respond


if __name__ == '__main__':
    d = get_order("149", "anz")
    print(d)
