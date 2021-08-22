# coding=utf8

import csv
import os
from typing import List
from common.connect_db import Connect_Db

# 以csv的形式读取数据
def read_csv() -> List[dict]:
    li = list()
    parent_directory = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    path = parent_directory + "/test_case/test_api.csv"
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for i in list(reader)[1:]:
            li.append({"method": i[1], "uri": i[2], "data": i[3], "assert": i[4]})
    return li


# 连接数据库获取参数
def get_request_data(uri=None, describe=None):
    conn = Connect_Db()

    li = list()
    if not describe:
        sql = "SELECT `uri`,`method`, `data`,`assert`,`describe` FROM `api_auto_test` WHERE `uri`='{uri}'".format(
            uri=uri)
    elif not uri:
        sql = "SELECT `uri`,`method`, `data`,`assert`,`describe` FROM `api_auto_test` WHERE `describe`='{describe}' ".format(
            describe=describe)
    else:
        sql = "SELECT `uri`,`method`, `data`,`assert`,`describe` FROM `api_auto_test` WHERE `uri`='{uri}' and `describe`='{describe}'".format(
            uri=uri, describe=describe)

    for i in conn.select_data(sql):
        li.append({"uri": i[0], "method": i[1], "data": i[2], "assert": i[3], "describe": i[4]})
    return li


if __name__ == '__main__':
    a = get_request_data("dfasdfasdf")
    print(a)
