# coding=utf8

import json
from common.connectdb import ConnectDb

conn = ConnectDb()


def select_respond(uri=None, describe=None):
    if not describe:
        sql = "SELECT  respond  FROM asp_saas_zjd.api_test WHERE uri='{uri}'".format(
            uri=uri)
    elif not uri:
        sql = "SELECT respond FROM asp_saas_zjd.api_test WHERE describe='{describe}' ".format(
            describe=describe)
    else:
        sql = "SELECT respond FROM asp_saas_zjd.api_test WHERE uri='{uri}' and describe='{describe}'".format(
            uri=uri, describe=describe)

    respond = conn.select_data(sql)

    return json.loads(respond[0][0])


# 连接数据库获取参数
def get_request_data(uri=None, describe=None):
    li = list()
    if not describe:
        sql = "SELECT  uri,method, data,assert,describe,id  FROM asp_saas_zjd.api_test WHERE uri='{uri}'".format(
            uri=uri)
    elif not uri:
        sql = "SELECT uri,method, data,assert,describe,id FROM asp_saas_zjd.api_test WHERE describe='{describe}' ".format(
            describe=describe)
    else:
        sql = "SELECT uri,method, data,assert,describe,id FROM asp_saas_zjd.api_test WHERE uri='{uri}' and describe='{describe}'".format(
            uri=uri, describe=describe)

    search_data = conn.select_data(sql)
    for i in search_data:
        try:

            data = json.loads(i[2])
            asserts = json.loads(i[3])

        except Exception as e:

            data = eval(i[2])
            asserts = eval(i[3])
        finally:
            pass

        li.append({"id": i[5], "uri": i[0], "method": i[1], "data": data, "assert": asserts, "describe": i[4]})

    return li


if __name__ == '__main__':
    a = select_respond("/api/v1/landing-page/widget-templates/PMP/ORDER_TYPE")
    print(a)
