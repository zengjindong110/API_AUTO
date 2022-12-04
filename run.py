# -*- coding: utf-8 -*-
import os
import unittest

from BeautifulReport import BeautifulReport

source_route = os.getcwd() + "/report"

"""
外部传参不传参默认为test环境
传参：
test 为测试环境
pre  为预发环境
prod 为线上环境    
"""

if __name__ == '__main__':
    test_suite = unittest.defaultTestLoader.discover('test_case', pattern='test_06_visit_landing_page_jump_url2.py')

    result = BeautifulReport(test_suite)

    result.report(filename='test_report', description='api_test_report', report_dir=source_route)

    # send_email()
