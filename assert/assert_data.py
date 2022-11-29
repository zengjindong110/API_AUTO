# -*- coding: utf-8 -*-
import json

"""
用来编写断言方式的模块
"""


class Assert(object):
    def __init__(self):
        self.key_list = list()
        self.key_value_type = {}

    def __del__(self):
        self.key_list.clear()

    # 断言json格式
    @staticmethod
    def assert_json(respond):
        try:
            respond = json.loads(respond)
            if respond:
                return True
        except TypeError:
            return False

    # 断言状态码
    @staticmethod
    def assert_code(respond):
        try:
            respond = json.loads(respond)
            if respond["code"] == '200':
                return True
            else:
                return False
        except TypeError:
            return False

    # 从返回的结果里面获取所有的key
    def get_key(self, respond: str) -> list:
        """
        :param respond:
        :return: 返回的格式是以列表的形式展示
        列如：[[a,b,c],[q,w,r],[s,d,f,h,j]]
        字典的key同意层级，会在同一个列表里面

        """
        try:

            respond = respond.replace('"[', "[").replace(']"', "]")
        except AttributeError as e:
            pass
        try:
            respond = json.loads(respond)
        except:
            pass

        if type(respond) == dict:
            self.key_list.append(list(respond.keys()))

        for key in respond.keys():
            # 当类型为字典而且返回的字典不为空
            if type(respond[key]) == dict and respond[key]:

                self.get_key(respond[key])

            elif type(respond[key]) == list and respond[key]:
                if type(respond[key][0]) != str:
                    self.get_key(respond[key][0])
            else:
                pass
        [_list.sort() for _list in self.key_list]

        return self.key_list

    # 断言key
    def assert_key(self, expect, respond):
        """

        :param expect: 预期结果
        :param respond: 实际结果
        :return:
        """
        expect_key = eval(expect)  # 预期结果所有的key
        [_except.sort() for _except in expect_key]
        keys = self.get_key(json.loads(respond))  # 获取返回结果所有的key
        expect_key.sort()
        keys.sort()
        # print("响应结果:{}\n响应结果所有的key:{}\n预期所有结果的key:{}".format(respond, keys, expect_key))

        if expect_key == keys:
            keys.clear()
            return True
        else:
            keys.clear()
            return False

    def get_value_type(self, respond):
        """
            :param respond:
            :return: 返回的格式是以列表的形式展示
            列如：[[a,b,c],[q,w,r],[s,d,f,h,j]]
            字典的key同意层级，会在同一个列表里面
            """
        try:

            respond = respond.replace('"[', "[").replace(']"', "]")
        except AttributeError as e:
            pass
        try:
            respond = json.loads(respond)
        except:
            pass

        if type(respond) == dict:
            keys = list(respond.keys())
            for key in keys:
                self.key_value_type[key] = type(respond[key])
            # map(lambda first_key: key_value_type.setdefault(first_key, type(respond[first_key])), key)

        for key in respond.keys():

            if type(respond[key]) == dict and respond[key]:

                self.get_value_type(respond[key])

            elif type(respond[key]) == list and respond[key]:

                if type(respond[key][0]) != str:
                    self.get_value_type(respond[key][0])
                else:
                    pass
            else:
                pass
        # [_list.sort() for _list in key_list]

        return self.key_value_type


if __name__ == '__main__':
    data = '{"records":[{"id":265,"name":"105版本验收项目","count":859,"pv":1676365,"click":35312,"clickRate":0.0211,"spend":"8863.88","submitDataCount":3,"submitDataCost":"2954.63","orderCompleteCount":0,"orderCompleteCost":"0"},{"id":263,"name":"102-01","count":3,"pv":1676365,"click":35312,"clickRate":0.0211,"spend":"8863.88","submitDataCount":0,"submitDataCost":"0","orderCompleteCount":0,"orderCompleteCost":"0"},{"id":255,"name":"105投放面板","count":5,"pv":1676365,"click":35312,"clickRate":0.0211,"spend":"8863.88","submitDataCount":0,"submitDataCost":"0","orderCompleteCount":0,"orderCompleteCost":"0"},{"id":267,"name":"45245245","count":0,"pv":0,"click":0,"clickRate":0,"spend":"0","submitDataCount":0,"submitDataCost":"0","orderCompleteCount":0,"orderCompleteCost":"0"},{"id":262,"name":"十人105测试","count":6,"pv":0,"click":0,"clickRate":0,"spend":"0","submitDataCount":0,"submitDataCost":"0","orderCompleteCount":0,"orderCompleteCost":"0"},{"id":261,"name":"105-203","count":1,"pv":0,"click":0,"clickRate":0,"spend":"0","submitDataCount":0,"submitDataCost":"0","orderCompleteCount":0,"orderCompleteCost":"0"},{"id":260,"name":"105-202","count":1,"pv":0,"click":0,"clickRate":0,"spend":"0","submitDataCount":0,"submitDataCost":"0","orderCompleteCount":0,"orderCompleteCost":"0"},{"id":259,"name":"105-201","count":1,"pv":0,"click":0,"clickRate":0,"spend":"0","submitDataCount":0,"submitDataCost":"0","orderCompleteCount":0,"orderCompleteCost":"0"},{"id":258,"name":"105-103","count":1,"pv":0,"click":0,"clickRate":0,"spend":"0","submitDataCount":0,"submitDataCost":"0","orderCompleteCount":0,"orderCompleteCost":"0"},{"id":257,"name":"105-102","count":1,"pv":0,"click":0,"clickRate":0,"spend":"0","submitDataCount":0,"submitDataCost":"0","orderCompleteCount":0,"orderCompleteCost":"0"},{"id":256,"name":"105-101","count":5,"pv":0,"click":0,"clickRate":0,"spend":"0","submitDataCount":0,"submitDataCost":"0","orderCompleteCount":0,"orderCompleteCost":"0"},{"id":254,"name":"王文修验收0730","count":1,"pv":0,"click":0,"clickRate":0,"spend":"0","submitDataCount":0,"submitDataCost":"0","orderCompleteCount":0,"orderCompleteCost":"0"},{"id":253,"name":"测试song111","count":0,"pv":0,"click":0,"clickRate":0,"spend":"0","submitDataCount":0,"submitDataCost":"0","orderCompleteCount":0,"orderCompleteCost":"0"},{"id":252,"name":"102添加投放账号","count":0,"pv":0,"click":0,"clickRate":0,"spend":"0","submitDataCount":0,"submitDataCost":"0","orderCompleteCount":0,"orderCompleteCost":"0"},{"id":251,"name":"1.101.0","count":1,"pv":0,"click":0,"clickRate":0,"spend":"0","submitDataCount":0,"submitDataCost":"0","orderCompleteCount":0,"orderCompleteCost":"0"},{"id":250,"name":"测试071501","count":0,"pv":0,"click":0,"clickRate":0,"spend":"0","submitDataCount":0,"submitDataCost":"0","orderCompleteCount":0,"orderCompleteCost":"0"},{"id":249,"name":"仰映昱测试","count":98,"pv":0,"click":0,"clickRate":0,"spend":"0","submitDataCount":0,"submitDataCost":"0","orderCompleteCount":0,"orderCompleteCost":"0"},{"id":248,"name":"测试SAAS","count":0,"pv":0,"click":0,"clickRate":0,"spend":"0","submitDataCount":0,"submitDataCost":"0","orderCompleteCount":0,"orderCompleteCost":"0"},{"id":246,"name":"94测试验收","count":5,"pv":0,"click":0,"clickRate":0,"spend":"0","submitDataCount":0,"submitDataCost":"0","orderCompleteCount":0,"orderCompleteCost":"0"},{"id":245,"name":"333","count":1,"pv":0,"click":0,"clickRate":0,"spend":"0","submitDataCount":0,"submitDataCost":"0","orderCompleteCount":0,"orderCompleteCost":"0"}],"total":151,"size":20,"current":1,"orders":[],"optimizeCountSql":true,"hitCount":false,"searchCount":true,"pages":8}'

    ase = Assert()

    a = ase.get_value_type(data)
    print(a)
