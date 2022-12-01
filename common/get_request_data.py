# -*- coding: utf-8 -*-

import json
from common.connectdb import ConnectDb

conn = ConnectDb()


def select_respond(uri=None, describe=None):
    if not describe:
        sql = f"SELECT  respond  FROM api_auto_test WHERE uri='{uri}' and is_delete='0'"
    elif not uri:
        sql = f"SELECT respond FROM api_auto_test WHERE describe='{describe}' and is_delete='0'"
    else:
        sql = f"SELECT respond FROM api_auto_test WHERE uri='{uri}' and describe='{describe}' and is_delete='0'"

    respond = conn.select_data(sql)

    return json.loads(respond[0][0])


# 连接数据库获取参数
def get_request_data(uri=None, describe=None):
    li = list()

    if not describe:
        sql = f"SELECT  uri,method, data,Assert,describe,id  FROM api_auto_test WHERE uri='{uri}' and is_delete='0'"
    elif not uri:
        sql = f"SELECT uri,method, data,Assert,describe,id FROM api_auto_test WHERE describe='{describe}' and is_delete='0'"
    else:
        sql = f"SELECT uri,method, data,Assert,describe,id FROM api_auto_test WHERE uri='{uri}' and describe='{describe}' and is_delete='0'"

    search_data = conn.select_data(sql)

    for i in search_data:

        data = i[2]

        asserts = i[3]



        li.append({"id": i[5], "uri": i[0], "method": i[1], "data": data, "Assert": asserts, "describe": i[4]})
    if li:
        return li
    else:
        print(sql)


if __name__ == '__main__':
    a = get_request_data("/api/v1/marketing/advertiser-account-groups/collect/list")
    print(a)
