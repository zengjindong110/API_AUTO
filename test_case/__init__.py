import time
import unittest
from common.log import Log
from Assert.customer_assert import *
from common.get_request_data import *
from common.open_landing_page import *
from common.request_api import RequestApi
from ui.applet_add_friends import *
from ui.api import CommonApi

__all__ = ['RequestApi', 'unittest', 'select_respond', 'get_request_data', "replace_data", "open_url", "now_date",
           "start_time", "end_time", "order_submit", "table_submit","AddFriend","CommonApi","Customer","Log"]


# 更新整个data请求参数
def replace_data(old, new):
    """
    replace_data(old,{'advertiserAccountGroupId': '4'})
    """
    return [i["data"].update(new) for i in old]


# 当前时间 格式化成2016-03-20 11:45:39形式
def now_date():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def start_time():
    """2022-07-09T16:00:00.000Z"""
    now_data = time.strftime("%Y-%m-%dT16:00:00.000Z", time.localtime())
    a = int(now_data[8:10]) - 1
    if a < 10:
        a = "0" + str(a)
    else:
        a = str(a)

    yesterday = now_data[:8] + a + now_data[10:]

    return yesterday


def end_time():
    """2022-07-09T16:00:00.000Z"""
    return time.strftime("%Y-%m-%dT15:59:59.000Z", time.localtime())
