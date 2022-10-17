from test_case import *

# import unittest
# from common.request_api import RequestApi
# from common.get_request_data import get_request_data

request = RequestApi()

order_template_id = None
form_template_id = None


class Template(unittest.TestCase, RequestApi):

    def test_01_create_order_template(self):
        """创建订单模板名称"""
        create_order_data = get_request_data("/api/v1/landing-page/widget-templates/PMP/ORDER_TYPE")
        # 订单模板名称更改，相同的订单模板名称不能创建成功
        order_tem_name = now_date()
        replace_data(create_order_data, {'name': order_tem_name})
        create_order_name_respond = self.request(create_order_data[0])
        print(create_order_name_respond)
        # 设置断言如果返回的字段name里面有订单模板名称表示通过
        self.assertEqual(create_order_name_respond["name"], order_tem_name, msg="通过返回值里面的name字段进行断言")
        global order_template_id
        order_template_id = create_order_name_respond["id"]

    def test_02_create_order_template(self):
        """将订单模板里面添加内容"""
        create_order_data = get_request_data("/api/v1/landing-page/widget-templates/pmp/FORM_TYPE/{}")
        create_order_url = "/api/v1/landing-page/widget-templates/pmp/FORM_TYPE/{}".format(str(order_template_id))
        create_order_data[0].update({"uri": create_order_url})
        create_order_respond = self.request(create_order_data[0])
        print(create_order_respond)
        self.assertTrue(create_order_respond['name'],msg="通过返回的name断言")

    def test_03_create_form_template(self):
        """创建表单模板名称"""
        create_form_data = get_request_data("/api/v1/landing-page/widget-templates/pmp/FORM_TYPE")
        # 订单模板名称更改，相同的订单模板名称不能创建成功
        form_tem_name = now_date()
        replace_data(create_form_data, {'name': form_tem_name})
        create_order_name_respond = self.request(create_form_data[0])
        # 设置断言如果返回的字段name里面有订单模板名称表示通过
        self.assertEqual(create_order_name_respond["name"], form_tem_name, msg="通过返回值里面的name字段进行断言")
        global form_template_id
        form_template_id = create_order_name_respond["id"]

    def test_04_create_form_template(self):
        """将表单模板里面添加内容"""
        create_form_data = get_request_data("/api/v1/landing-page/widget-templates/pmp/FORM_TYPE/{}")
        print(create_form_data)
        create_form_url = "/api/v1/landing-page/widget-templates/pmp/FORM_TYPE/{}".format(str(form_template_id))
        create_form_data[0].update({"uri": create_form_url})
        create_form_respond = self.request(create_form_data[0])
        self.assertTrue(create_form_respond['name'],msg="通过返回的name断言")

