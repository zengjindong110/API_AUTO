from common.request_api import RequestApi


class AssertLandingPageTable(RequestApi):
    """通过落地页名称查落地页列表上面的数据
        拿到数据后将数据做比较，判断不同链路上面的数据变化，
        根据数据的变化进行断言
    """

    def get_data(self):
        data = {
            "page": 1,
            "size": 20,
            "order": "desc",
            "sortField": "updatedAt",
            "name": "一跳-小程序-加粉",
            "startTime": "2022-11-30T16:00:00.000Z",
            "endTime": "2022-12-01T15:59:59.000Z",
            "deleteStatus": "NORMAL",
            "landingPageGroupId": -1,
            "advertiserAccountGroupId": 126,
            "recoveryAt": 0
        }
        print(data)
        # self.request()


if __name__ == '__main__':
    a = AssertLandingPageTable()
    a.get_data()
