from test_case import *


# import unittest
# from common.request_api import RequestApi
# from common.get_request_data import get_request_data

request = RequestApi()
class OrderTemplate(unittest.TestCase):


    def test_create_order_template(self):
        create_order_data = get_request_data("/api/v1/landing-page/widget-templates/PMP/ORDER_TYPE")
        print(create_order_data)
        create_order_respond = request.request(create_order_data[0])
        self.assertEqual(1, 1)
