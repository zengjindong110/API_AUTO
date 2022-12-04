from common.request_api import RequestApi
from common.log import Log
from common.get_config_data import GetConfig

gc = GetConfig()
log = Log(__file__)


class AssertLandingPageTable(RequestApi):
    """通过落地页名称查落地页列表上面的数据
        拿到数据后将数据做比较，判断不同链路上面的数据变化，
        根据数据的变化进行断言
    """

    def __init__(self):
        super().__init__()
        self.once_jump_page_data_one = ""
        self.once_jump_page_data_second = ""
        self.second_jump_page_data_one = ""
        self.second_jump_page_data_second = ""

    def get_data(self, landing_page_name):
        """
        查询落地页列表数据
        """
        search_data = {
            "method": "get",
            "uri": "/api/v1/landing-page/landing-pages/pmp/collect/filtering/new",
            "data": {
                "page": 1,
                "size": 20,
                "order": "desc",
                "sortField": "updatedAt",
                "name": landing_page_name,
                "startTime": gc.start_time()[0],
                "endTime": gc.end_time()[0],
                "deleteStatus": "NORMAL",
                "landingPageGroupId": -1,
                "advertiserAccountGroupId": gc.get_pmp_id(),
                "recoveryAt": 0
            },
            "id": 19,
        }
        respond = self.request(search_data)
        try:
            respond = respond["records"][0]
        except KeyError:
            log.error(f"接口返回参数有问题{respond}")
        else:
            return respond

    def applet_add_friend_before(self, once_jump_page_name, second_jump_page_name):
        """
        获取一跳落地页和二跳落地页添加好友前的数据
        """
        self.once_jump_page_data_one = self.get_data(once_jump_page_name)
        self.second_jump_page_data_one = self.get_data(second_jump_page_name)

    def applet_add_friend_after(self, once_jump_page_name, second_jump_page_name):
        """
        获取一跳落地页和二跳落地页添加好友后的数据
        """
        self.once_jump_page_data_second = self.get_data(once_jump_page_name)
        self.second_jump_page_data_second = self.get_data(second_jump_page_name)

    def assert_once_page_data(self):
        """
        一跳页断言落地页只会增加pv数+1
        """

        # 浏览数(PV)
        pageViewNum = self.once_jump_page_data_second["pageViewNum"] - \
                      self.once_jump_page_data_one["pageViewNum"]
        log.info(f'断言一跳页数据一跳页浏览数(PV) {pageViewNum} ')
        return True if pageViewNum == 1 else False

    def assert_second_page_data(self):
        """
        断言二跳页添加好友的数据
        加企业微信数 +1
        pageViewNum +1
        长按二维码识别数(微信 / 企业微信) +1
        平均停留时长(秒)  不为 0
        """
        # 加企业微信数
        addWorkWechatNum = self.second_jump_page_data_second["addWorkWechatNum"] - \
                           self.second_jump_page_data_one["addWorkWechatNum"]

        # 浏览数(PV)
        pageViewNum = self.second_jump_page_data_second["pageViewNum"] - \
                      self.second_jump_page_data_one["pageViewNum"]
        # 长按二维码识别数(微信 / 企业微信)
        identifyQrCodeNum = self.second_jump_page_data_second["pageViewNum"] - \
                            self.second_jump_page_data_one["pageViewNum"]
        # 长按二维码识别率(微信 / 企业微信)

        # 加企业微信率

        # 平均停留时长(秒)
        averageLengthOfStay = self.second_jump_page_data_second["averageLengthOfStay"]

        log.info(
            f"断言二跳页数据 加企业微信数+{addWorkWechatNum} 浏览数(PV)+{pageViewNum} 长按二维码识别数(微信 / 企业微信)+{identifyQrCodeNum} 平均停留时长(秒){averageLengthOfStay}")
        return True if addWorkWechatNum == 1 and pageViewNum == 1 and identifyQrCodeNum == 1 and \
                       float(averageLengthOfStay) > 0 else False


if __name__ == '__main__':
    a = AssertLandingPageTable()
    a.applet_add_friend_before("一跳-小程序-加粉", "二跳-H5-二维码")
    a.applet_add_friend_after("一跳-小程序-加粉", "二跳-H5-二维码")
    a.assert_once_page_data()
    a.assert_second_page_data()
