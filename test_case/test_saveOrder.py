# coding=gbk


import unittest
from ddt import ddt, data
from common.get_request_data import *
from common.assert_data import *
from common.request_api import RequestApi
import warnings
import config


@ddt()
class TestSaveOrder(unittest.TestCase):
    args = get_request_data("/lbdj/web/saveOrder")

    def tearDown(self):  # ÿ����������֮�����е�
        key_list.clear()

    @classmethod
    def tearDownClass(cls):  # ������������ִ����֮�����е�
        warnings.simplefilter('ignore', ResourceWarning)

    @data(*args)
    def test_saveOrder(self, value):  # ������Ҫ��test��ͷ�����򲻻ᱻִ��
        """
        hahahah
        :param value:
        :return:
        """
        print("��������{}".format(value["describe"]))
        respond = RequestApi.request(value["method"], value["uri"], value["data"])
        try:
            ordersn, orderid = respond.json()["t"]["orderSn"], respond.json()["t"]["orderId"]
        except KeyError as e:
            raise RuntimeError(respond.json()) from e
        if ordersn.startswith('S1') or ordersn.startswith('S3'):
            pay_data = {"cashCouponId": "", "orderId": str(orderid), "payChannel": 0,
                        "walletPwd": config.environment["test"]["pay_password"]}

            pay_status = RequestApi.request("post", "/lbdj/web/pay/orderPay", pay_data).json()
            self.assertEqual(orderid, pay_status['t']["orderId"], msg="{}".format(pay_status['t']["msg"]))
        get_order_data = {"orderId": orderid}
        get_order = RequestApi.request("post", "/lbdj/web/getOrderDetail", get_order_data)
        self.assertEqual(get_order.json()["msg"], None, msg="get_order.json()")

        self.assertTrue(assert_json(respond.text), msg="��Ӧ�����֪json��ʽ")  # ����json
        self.assertTrue(assert_code(respond.text), msg="��Ӧ״̬�벻��200")  # code����
        self.assertTrue(assert_key(value["assert"], respond.text), msg=get_order.json())  # key����


class TestGetOrderData(unittest.TestCase):

    def test_selectTemplate(self):
        """��ȡ����ģ��"""
        selectTemplateData = get_request_data("/lbdj/web/selectTemplate")[0]
        selectTemplateRsp = RequestApi.request(selectTemplateData["method"], selectTemplateData["uri"],
                                               selectTemplateData["data"])
        self.assertTrue(assert_key(selectTemplateData["assert"], selectTemplateRsp.text),
                        msg=selectTemplateRsp.json())  # key����

    def test_getCategory(self):
        """��ȡ��Ʒ�������"""
        getCategoryDat = get_request_data("/lbdj/web/getCategory", "��ȡ��Ʒ�������")[0]
        getCategoryRsp = RequestApi.request(getCategoryDat["method"], getCategoryDat["uri"],
                                            getCategoryDat["data"])
        self.assertTrue(assert_key(getCategoryDat["assert"], getCategoryRsp.text),
                        msg=getCategoryRsp.json())  # key����

    def test_getGoodsSpection(self):
        """��ȡ��Ʒ���"""
        GoodsSpectionData = get_request_data("/lbdj/web/getGoodsSpection", "��ȡ��Ʒ���")[0]

        GoodsSpectionRsp = RequestApi.request(GoodsSpectionData["method"], GoodsSpectionData["uri"],
                                              GoodsSpectionData["data"])

        self.assertTrue(assert_key(GoodsSpectionData["assert"], GoodsSpectionRsp.text),
                        msg=GoodsSpectionRsp.text)  # key����

    def test_orderBaseData(self):
        """��ȡ������������"""
        orderBaseData = get_request_data("/lbdj/web/orderBaseData")[0]

        orderBaseDataRsp = RequestApi.request(orderBaseData["method"], orderBaseData["uri"],
                                              orderBaseData["data"])
        self.assertTrue(assert_key(orderBaseData["assert"], orderBaseDataRsp.text),
                        msg=orderBaseDataRsp.text)  # key����


if __name__ == '__main__':
    unittest.main()
