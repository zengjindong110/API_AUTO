# coding=gbk


import unittest
from ddt import ddt,data
from common.get_request_data import *
from common.assert_data import *
from common.request_api import RequestApi
import warnings
import config


@ddt()
class TestMyOrder(unittest.TestCase):
    aargs = get_request_data("/lbdj/app/order/AppMyOrderListApiRequest")  # 师傅查看我的待预约订单

    def tearDown(self):  # 每个用例运行之后运行的
        key_list.clear()

    @classmethod
    def tearDownClass(cls):  # 在所有用例都执行完之后运行的
        warnings.simplefilter('ignore', ResourceWarning)

    @data(*aargs)
    def test_my_order(self, value):  # 函数名要以test开头，否则不会被执行
        """
        hahahah
        :param value:
        :return:
        """
        print("用例描述{}".format(value["describe"]))
        req_data = json.loads(value["data"])
        req_data["token"] = config.worker_environment["test"]["token"]
        respond = RequestApi.worker_requests(value["method"], value["uri"], value["data"])
        if respond.json()["data"] == []:
            self.assertEqual(respond.text,'{"isSuccess":true,"code":"200","msg":"success","data":[]}',respond.text)
        else:
            self.assertEqual(respond.json()["msg"], "success", msg=respond.text)
            self.assertTrue(assert_key(value["assert"], respond.text), msg="预期的key与实际的key不一样")  # key断言


if __name__ == '__main__':
    unittest.main()
