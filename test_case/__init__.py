import unittest

from common.get_request_data import *
from common.request_api import RequestApi
from common.seleniums import ChromeDriver

__all__ = ['RequestApi', 'unittest', 'select_respond', 'get_request_data', "replace_data","ChromeDriver"]


def replace_data(old, new):
    return [i["data"].update(new) for i in old]
