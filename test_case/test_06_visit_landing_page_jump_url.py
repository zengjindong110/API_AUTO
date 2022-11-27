# coding=utf8
import json

from test_case import *
from ui import *

class VisitLandingPageJumpUrl(unittest.TestCase, RequestApi,AddFriend):

    def tearDown(self):  # 每个用例运行之后运行的
        pass

    @classmethod
    def tearDownClass(cls):  # 在所有用例都执行完之后运行的
        # warnings.simplefilter('ignore', ResourceWarning)
        pass

    def test_applets_add_friend(self):
        land_page_url = "http://bbb.dbq.yiye.ai/dbq/slLPIPXr?_cl=ffcf"
        self.open_land_page(land_page_url)
        self.add_friend()

if __name__ == '__main__':
    unittest.main()