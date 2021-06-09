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

    def tearDown(self):  # 每个用例运行之后运行的
        key_list.clear()

    @classmethod
    def tearDownClass(cls):  # 在所有用例都执行完之后运行的
        warnings.simplefilter('ignore', ResourceWarning)

    @data(*args)
    def test_saveOrder(self, value):  # 函数名要以test开头，否则不会被执行
        """
        hahahah
        :param value:
        :return:
        """
        print("用例描述{}".format(value["describe"]))
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

        self.assertTrue(assert_json(respond.text), msg="响应结果不知json格式")  # 断言json
        self.assertTrue(assert_code(respond.text), msg="响应状态码不是200")  # code断言
        self.assertTrue(assert_key(value["assert"], respond.text), msg=get_order.json())  # key断言


class TestGetOrderData(unittest.TestCase):

    def test_selectTemplate(self):
        """获取订单模板"""
        selectTemplateData = get_request_data("/lbdj/web/selectTemplate")[0]
        selectTemplateRsp = RequestApi.request(selectTemplateData["method"], selectTemplateData["uri"],
                                               selectTemplateData["data"])
        self.assertTrue(assert_key(selectTemplateData["assert"], selectTemplateRsp.text),
                        msg=selectTemplateRsp.json())  # key断言

    def test_getCategory(self):
        """获取商品类别名称"""
        getCategoryDat = get_request_data("/lbdj/web/getCategory", "获取商品类别名称")[0]
        getCategoryRsp = RequestApi.request(getCategoryDat["method"], getCategoryDat["uri"],
                                            getCategoryDat["data"])
        self.assertTrue(assert_key(getCategoryDat["assert"], getCategoryRsp.text),
                        msg=getCategoryRsp.json())  # key断言

    def test_getGoodsSpection(self):
        """获取商品规格"""
        GoodsSpectionData = get_request_data("/lbdj/web/getGoodsSpection", "获取商品规格")[0]

        GoodsSpectionRsp = RequestApi.request(GoodsSpectionData["method"], GoodsSpectionData["uri"],
                                              GoodsSpectionData["data"])

        self.assertTrue(assert_key(GoodsSpectionData["assert"], GoodsSpectionRsp.text),
                        msg=GoodsSpectionRsp.text)  # key断言

    def test_orderBaseData(self):
        """获取基础订单类型"""
        orderBaseData = get_request_data("/lbdj/web/orderBaseData")[0]

        orderBaseDataRsp = RequestApi.request(orderBaseData["method"], orderBaseData["uri"],
                                              orderBaseData["data"])
        self.assertTrue(assert_key(orderBaseData["assert"], orderBaseDataRsp.text),
                        msg=orderBaseDataRsp.text)  # key断言


if __name__ == '__main__':
    unittest.main()
