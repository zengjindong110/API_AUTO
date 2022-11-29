# coding=utf8

from test_case import *


class VisitLandingPageJumpUrl(unittest.TestCase, RequestApi, AddFriend):

    def tearDown(self):  # 每个用例运行之后运行的
        pass

    @classmethod
    def tearDownClass(cls):  # 在所有用例都执行完之后运行的
        # warnings.simplefilter('ignore', ResourceWarning)
        pass

    def test_applets_add_friend(self):
        """
        H5跳转到企业小程序添加好友
        """
        land_page_url = "http://bbb.dbq.yiye.ai/dbq/slLPIPXr?_cl=ffcf"
        self.h5_applet_add(land_page_url)


if __name__ == '__main__':
    unittest.main()
