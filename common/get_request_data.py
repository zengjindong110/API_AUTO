# coding=utf8

import json
from common.connectdb import ConnectDb

conn = ConnectDb()


def select_respond(uri=None, describe=None):
    if not describe:
        sql = "SELECT  respond  FROM api_auto_test WHERE uri='{uri}' and is_delete='0'".format(
            uri=uri)
    elif not uri:
        sql = "SELECT respond FROM api_auto_test WHERE describe='{describe}' and is_delete='0'".format(
            describe=describe)
    else:
        sql = "SELECT respond FROM api_auto_test WHERE uri='{uri}' and describe='{describe}' and is_delete='0'".format(
            uri=uri, describe=describe)

    respond = conn.select_data(sql)

    return json.loads(respond[0][0])


# 连接数据库获取参数
def get_request_data(uri=None, describe=None):
    li = list()

    if not describe:
        sql = "SELECT  uri,method, data,assert,describe,id  FROM api_auto_test WHERE uri='{uri}' and is_delete='0'".format(
            uri=uri)
    elif not uri:
        sql = "SELECT uri,method, data,assert,describe,id FROM api_auto_test WHERE describe='{describe}' and is_delete='0'".format(
            describe=describe)
    else:
        sql = "SELECT uri,method, data,assert,describe,id FROM api_auto_test WHERE uri='{uri}' and describe='{describe}' and is_delete='0'".format(
            uri=uri, describe=describe)

    search_data = conn.select_data(sql)

    for i in search_data:

        data = i[2]

        asserts = i[3]



        li.append({"id": i[5], "uri": i[0], "method": i[1], "data": data, "assert": asserts, "describe": i[4]})
    if li:
        return li
    else:
        print(sql)


if __name__ == '__main__':
    a = get_request_data("/api/v1/marketing/advertiser-account-groups/collect/list")
    print(a)
