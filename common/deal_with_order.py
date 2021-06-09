# coding=gbk


from common.get_request_data import *
from common.request_api import RequestApi
import json

def get_code(orderId):
    data = {"orderId": orderId}
    return RequestApi.request("post", "/lbdj/web/getConfirmationCode", data).json()["t"]


def my_order_info(order_id, orderSn):
    snCodeListReq = {"orderId": order_id, "orderSn": orderSn}
    order_list_res = RequestApi.worker_requests("post", "/lbdj/app/order/AppMyOrderInfoApiRequest", snCodeListReq)

    return order_list_res.json()["data"]["goodsList"][0]


def appointment_time():
    import datetime
    return str(datetime.datetime.now())[:10] + ",21:00+-+23:00"


def snCodeList(order_id, orderSn):
    order_list = my_order_info(order_id, orderSn)
    # {"orderId":"1318175099890696262","goodsName":"��ͯѧϰ����װ","productDetailId":null,"snCode":""}
    return {"orderId": order_list['orderGoodsId'], "goodsName": order_list["goodsName"], "productDetailId": "",
            "snCode": ""}


def reserve_HomeCheck(order):
    """
    ������ԤԼʱ�䣬���Ŵ� һ��д����һ����������
    :param order:
    :return:
    """
    GrabOrderData = get_request_data("/lbdj/app/order/AppGrabOrderApiRequest")[0]  # ��ѯʦ���������ݿ����

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


def ServiceDone(order):
    ServiceDoneData = get_request_data("/lbdj/app/order/AppServiceDoneApiRequest")[0]  # ��ȡ�깤����
    ServiceDoneReq = json.loads(ServiceDoneData["data"])
    ServiceDoneReq["orderId"] = order["id"]
    ServiceDoneReq["wcCode"] = get_code(order["id"])
    ServiceDoneReq["orderSn"] = order["orderNum"]
    respond = RequestApi.worker_requests(ServiceDoneData["method"], ServiceDoneData["uri"],
                                         ServiceDoneReq).json()  # ������֤��ȷ���깤
    return respond


def wangong(order):
    # order = {'discountServiceFlag': 0, 'address': 'ǰ��һ·ǰ������ǰ��С��', 'catName': '����', 'city': '����ر�������', 'closeReason': None, 'customer': '����', 'customerPhone': '17786451825', 'district': '������', 'exceptionReason': None, 'isPause': None, 'id': '1307964854425878536', 'orderGetTime': '2020-09-22 08:00-10:00', 'sortTime': '2020-09-22 08:00:00', 'orderNum': 'S31307964854404907079', 'busofferno': None, 'orderaddfee': 0.0, 'pauseReason': None, 'pauseTime': None, 'payment': 162.24, 'province': '�۰�', 'status': 5, 'isAssigned': 0, 'isSign': 0, 'arrivalGoods': None, 'arrivalGoodsMsg': None, 'urgentFee': 0.0, 'statusTime': None, 'tName': '����-����', 'busserName': 'ƽ̨--�̼�', 'busserId': 106552, 'isTmallTag': 0, 'properStatus': 0, 'arrivalTime': '2020-09-24 14:32:18', 'latestReservationTime': None, 'remainReservationTime': None, 'islvmilockorder': 0, 'hasAllowance': 0, 'allowanceMoney': 0.0, 'isPS': 0, 'isTaobaoOrder': 0, 'hx_status': 0, 'nextSubscribeTime': '', 'exceptionOprationTime': None, 'timeOutSubscribe': None, 'timeOutNotDropIn': None, 'excepSubscribeTime': None, 'excepSbuscribeReason': None, 'excepSbuscribeNote': None, 'installNote': '', 'needOntimeInstall': 0, 'orderChannel': 0, 'clockFinish': 1, 'customerDesc': '', 'originId': None, 'orderType': 3, 'isVip': 1, 'createTime': '2020-09-21 16:48:17', 'tryOrderTag': 0, 'tryOrderFrozenTag': 0, 'tryOrderFrozenTime': None, 'vipDiscountTag': 0, 'vipDiscountMoney': 0.0, 'statusName': '������', 'displayText': '������', 'wxOrSecondText': None, 'extendedTags': [], 'appointExceptionPrompt': None, 'servicetype': 'lc', 'thirdservicetype': None, 'planTime': '2020-09-22 08:00:00', 'workerPayment': None, 'pauseNote': None, 'cid': 136, 'planEndTime': '2020-09-22 10:00:00', 'countdownTip': None, 'fullAddress': '�۰�����ر�������������ǰ��һ·ǰ������ǰ��С��', 'showTime': 'ԤԼʱ��:2020-09-22 08:00-10:00', 'promptTime': None, 'orderStatus': 5, 'pauseDetail': 0, 'orderQty': '1', 'goodsImg': 'https://lbdj.oss-cn-beijing.aliyuncs.com//upload/test/20200916/0DE48D1D270F38032796A33B9DE41BE0.png', 'psType': None, 'adjustFee': 0.0, 'adjustprice': 0, 'orderTags': [], 'middleVoList': None, 'tbOrderId': None, 'relationBusinessId': None, 'httNew': 0, 'workerId': '147989', 'workerName': None, 'workerPhone': None, 'teamId': None}
    order_id = order["id"]
    order_sn = order["orderNum"]
    InstallCheckData = get_request_data("/lbdj/app/order/AddOrderInstallCheckApiRequest")[0]  # ��ȡװǰ�����������

    InstallCheckReq = json.loads(InstallCheckData["data"])
    InstallCheckReq["orderId"] = order_id
    InstallCheckRes = RequestApi.worker_requests(InstallCheckData["method"], InstallCheckData["uri"],
                                                 InstallCheckReq)  # װǰ���

    UploadDoneImageData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest")[0]  # ��ȡ�깤�������
    UploadDoneImageReq = json.loads(UploadDoneImageData["data"])
    UploadDoneImageReq["orderId"] = order_id
    UploadDoneImageReq["finishImages"][0]["goodName"] = my_order_info(order_id, order_sn)["goodsName"]
    UploadDoneImageRes = RequestApi.worker_requests(UploadDoneImageData["method"], UploadDoneImageData["uri"],
                                                    UploadDoneImageReq)  # �ϴ��깤ͼ

    DoneImageReq = {"orderId": order_id, "type": 3,
                    "images": "[\"writing/20201029/0D3D8E2DC02B4AF3D15FF7E1A009413B.png\"]", "videoAddress": ""}
    RequestApi.worker_requests("post", "/lbdj/app/order/AppUploadDoneImageApiRequest",
                               DoneImageReq)  # ����ǩ�յ�ȷ��
    """type: ͼƬ���ͣ�1.�깤ͼ/�깤��Ƶ 2.��������ͼ 3.ǩ��ͼ"""
    respond = ServiceDone(order)
    print(respond)


def get_my_order():
    data = {"token": config.worker_environment["test"]["token"], "pageNum": "1", "pageSize": "10", "type": "1",
            "currentOrderNum": "52", "status": "3"}

    respond = RequestApi.worker_requests("post", "/lbdj/app/order/AppMyOrderListApiRequest", data)
    print(respond)
    return respond.json()["data"]


def over_yuyue():
    """���ԤԼ�Ķ���"""
    all_order = []
    data = {"token": config.worker_environment["test"]["token"], "pageNum": "1", "pageSize": "10", "type": "1",
            "currentOrderNum": "52", "status": "1"}

    respond = RequestApi.worker_requests("post", "/lbdj/app/order/AppMyOrderListApiRequest", data)
    print(respond)
    all_order.extend(respond.json()["data"])
    data["status"] = "15"
    respond = RequestApi.worker_requests("post", "/lbdj/app/order/AppMyOrderListApiRequest", data)
    all_order.extend(respond.json()["data"])
    for order in all_order:
        reserve_HomeCheck(order)
        wangong(order)


def run_over():
    """
    ��ɷ����еĶ���
    :return:
    """
    all_order = get_my_order()
    [wangong(order) for order in all_order]


if __name__ == '__main__':
    # d = {'discountServiceFlag': 0, 'address': '���Ե�ַ11111', 'catName': '�ƾ���', 'city': '����ر�������', 'closeReason': None, 'customer': '����', 'customerPhone': '18565745317', 'district': '������', 'exceptionReason': None, 'isPause': None, 'id': '310707824097628160', 'orderGetTime': '2020-11-05 19:49:15', 'sortTime': '2020-11-05 19:49:15', 'orderNum': 'S1310707824085045248', 'busofferno': None, 'orderaddfee': 0.0, 'pauseReason': None, 'pauseTime': None, 'payment': 50.0, 'province': '�۰�', 'status': 3, 'isAssigned': 2, 'isSign': 0, 'arrivalGoods': None, 'arrivalGoodsMsg': '������ѯ�ʵ������', 'urgentFee': 0.0, 'statusTime': None, 'tName': '�ƾ���-��װ', 'busserName': 'U_105227', 'busserId': 105395, 'isTmallTag': 0, 'properStatus': 0, 'arrivalTime': '2020-11-05 19:49:14', 'latestReservationTime': None, 'remainReservationTime': None, 'islvmilockorder': 0, 'hasAllowance': 0, 'allowanceMoney': 0.0, 'isPS': 0, 'isTaobaoOrder': 0, 'hx_status': 0, 'nextSubscribeTime': '2020-11-06 07:49:15', 'exceptionOprationTime': None, 'timeOutSubscribe': None, 'timeOutNotDropIn': None, 'excepSubscribeTime': None, 'excepSbuscribeReason': None, 'excepSbuscribeNote': None, 'installNote': '', 'needOntimeInstall': 0, 'orderChannel': 0, 'clockFinish': 0, 'customerDesc': '', 'originId': None, 'orderType': 0, 'isVip': 1, 'createTime': '2019-05-08 09:21:58', 'tryOrderTag': 0, 'tryOrderFrozenTag': 0, 'tryOrderFrozenTime': None, 'vipDiscountTag': 0, 'vipDiscountMoney': 0.0, 'statusName': 'ԤԼ�ͻ�', 'displayText': None, 'wxOrSecondText': None, 'extendedTags': ['ָ��'], 'appointExceptionPrompt': None, 'servicetype': 'anz', 'thirdservicetype': None, 'planTime': None, 'workerPayment': None, 'pauseNote': None, 'cid': 138, 'planEndTime': None, 'countdownTip': None, 'fullAddress': '�۰�����ر����������������Ե�ַ11111', 'showTime': '����ʱ��:2020-11-05 19:49:15', 'promptTime': None, 'orderStatus': 3, 'pauseDetail': 0, 'orderQty': '1', 'goodsImg': 'https://lbdj.oss-cn-beijing.aliyuncs.com/upload/template/20190425/DD584973F9B3FEB34B83FEA2C733430F.png', 'psType': None, 'adjustFee': 0.0, 'adjustprice': 0, 'orderTags': [], 'middleVoList': None, 'tbOrderId': None, 'relationBusinessId': None, 'httNew': 0, 'workerId': '147989', 'workerName': None, 'workerPhone': None, 'teamId': None}
    #
    # reserve_HomeCheck(d)
    over_yuyue()
