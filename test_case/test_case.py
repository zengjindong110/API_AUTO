# coding=gbk
from common.get_request_data import get_request_data
import unittest
import warnings


class TestUserLogin(unittest.TestCase):

    def tearDown(self):  # ÿ����������֮�����е�
        pass

    @classmethod
    def tearDownClass(cls):  # ������������ִ����֮�����е�
        warnings.simplefilter('ignore', ResourceWarning)

    def test_saveOrder(self):  # ������Ҫ��test��ͷ�����򲻻ᱻִ��
        """ƽ̨���û��˺������½"""
        login_data = get_request_data("dfasdfasdf")[0]
        print(login_data)


if __name__ == '__main__':
    unittest.main()
