from common.request_api import RequestApi


class Customer(RequestApi):

    def get_customer(self):
        """
        获取客资
        """
        get_data_params = {
            "method":"get",
            "data":{}
        }
        self.request()

    def compare_customer(self, first_customer, second_customer):
        """
        比较客资
        """
        pass
