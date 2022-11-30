# -*- coding: utf-8 -*-
from common.get_config_data import GetConfig

from common.request_api import RequestApi
import datetime

GC = GetConfig()


class Customer(RequestApi):

    def get_customer(self):
        """
        获取客资
        """
        get_data_params = {
            "uri": "/api/v1/customer/customers/pmp",
            "method": "get",
            "data": {"page": 1,
                     "size": 20,
                     "order": "desc",
                     "sort": "createdAt",
                     "advertiserAccountId": GC.get_config_data("PMP")["PMP_ID"],
                     "filtering": [{"field": "advertiser_account_group_id", "operator": "EQ",
                                    "values": [GC.get_config_data("PMP")["PMP_ID"]]}],
                     "startTime": str(datetime.date.today()),
                     "endTime": str(datetime.date.today())
                     },
            "id": 18
        }
        print()
        aa = self.request(get_data_params)
        print(aa)

    def compare_customer(self, first_customer, second_customer):
        """
        比较客资
        """
        pass


if __name__ == '__main__':
    aaa = Customer()
    aaa.get_customer()
