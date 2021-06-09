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
    aargs = get_request_data("/lbdj/app/order/AppMyOrderListApiRequest")  # ʦ���鿴�ҵĴ�ԤԼ����

    def tearDown(self):  # ÿ����������֮�����е�
        key_list.clear()

    @classmethod
    def tearDownClass(cls):  # ������������ִ����֮�����е�
        warnings.simplefilter('ignore', ResourceWarning)

    @data(*aargs)
    def test_my_order(self, value):  # ������Ҫ��test��ͷ�����򲻻ᱻִ��
        """
        hahahah
        :param value:
        :return:
        """
        print("��������{}".format(value["describe"]))
        req_data = json.loads(value["data"])
        req_data["token"] = config.worker_environment["test"]["token"]
        respond = RequestApi.worker_requests(value["method"], value["uri"], value["data"])
        if respond.json()["data"] == []:
            self.assertEqual(respond.text,'{"isSuccess":true,"code":"200","msg":"success","data":[]}',respond.text)
        else:
            self.assertEqual(respond.json()["msg"], "success", msg=respond.text)
            self.assertTrue(assert_key(value["assert"], respond.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")  # key����


if __name__ == '__main__':
    unittest.main()
