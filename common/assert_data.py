# coding=utf-8
import json
import pymysql
import config

"""
用来编写断言方式的模块
"""

key_list = list()


# 断言json格式
def assert_json(respond):
    try:
        respond = json.loads(respond)
        if respond:
            return True
    except TypeError:
        return False


# 断言状态码
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
def get_key(respond: str) -> list:
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
        key_list.append(list(respond.keys()))

    for key in respond.keys():

        if type(respond[key]) == dict and respond[key]:

            get_key(respond[key])

        elif type(respond[key]) == list and respond[key]:
            if type(respond[key][0]) != str:
                get_key(respond[key][0])
        else:
            pass
    [_list.sort() for _list in key_list]

    return key_list


# 断言key
def assert_key(expect, respond):
    """

    :param expect: 预期结果
    :param respond: 实际结果
    :return:
    """
    expect_key = eval(expect)  # 预期结果所有的key
    [_except.sort() for _except in expect_key]
    keys = get_key(json.loads(respond))  # 获取返回结果所有的key
    expect_key.sort()
    keys.sort()
    # print("响应结果:{}\n响应结果所有的key:{}\n预期所有结果的key:{}".format(respond, keys, expect_key))

    if expect_key == keys:
        keys.clear()
        return True
    else:
        keys.clear()
        return False


def select_data(sql):
    conn = pymysql.connect(host=config.environment["test"]["mysql"]["mysql_host"],
                           port=config.environment["test"]["mysql"]["mysql_port"],
                           user=config.environment["test"]["mysql"]["mysql_user"],
                           passwd=config.environment["test"]["mysql"]["mysql_passworld"],
                           db=config.environment["test"]["mysql"]["mysql_db"],
                           charset='utf8')
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def get_order_info(ordersn):
    query = "SELECT * FROM `lbdj`.`lbdjorder` where ordersn ='{}'".format(ordersn)

    order_info = select_data(query)
    return order_info


def assert_order_info(ordersn):
    if get_order_info(ordersn):
        return True
    else:
        return False


