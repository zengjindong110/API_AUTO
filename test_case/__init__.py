import unittest

from Assert.customer_assert import *
from Assert.customer_service import CustomerService
from Assert.landing_page_table import AssertLandingPageTable
from common.get_request_data import *
from common.log import Log
from common.open_landing_page import *
from common.request_api import RequestApi
from ui.api import CommonApi
from ui.applet_add_friends import *

__all__ = ['RequestApi', 'unittest', 'select_respond', 'get_request_data', "replace_data", "open_url",
           "order_submit", "table_submit", "AddFriend", "CommonApi", "Customer", "Log", "CustomerService",
           "AssertLandingPageTable","wechat_customer_service"]


# 更新整个data请求参数
def replace_data(old, new):
    """
    replace_data(old,{'advertiserAccountGroupId': '4'})
    """
    return [i["data"].update(new) for i in old]


wechat_customer_service = "王新婷"
