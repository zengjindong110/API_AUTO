# coding=gbk
import unittest
from BeautifulReport import BeautifulReport
import os
# from common.send_email import send_email
import sys


source_route = os.getcwd() + "/report"

"""
�ⲿ���β�����Ĭ��Ϊtest����
���Σ�
test Ϊ���Ի���
pre  ΪԤ������
prod Ϊ���ϻ���    
"""



if __name__ == '__main__':
    # try:
    #     envi = sys.argv[1]
    # except Exception:
    #     envi = "test"
    # environment["test"] = eval("user_" + envi)
    # worker_environment["test"] = eval("worker_" + envi)
    test_suite = unittest.defaultTestLoader.discover('./test_case', pattern='test_*.py')
    result = BeautifulReport(test_suite)
    result.report(filename='test_report', description='api_test_report', report_dir=source_route)
    # send_email()
