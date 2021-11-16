# coding=utf8

import json
from common.connectdb import ConnectDb


# 连接数据库获取参数
def get_request_data(uri=None, describe=None):
    conn = ConnectDb()

    li = list()
    if not describe:
        sql = "SELECT uri,method, data,assert,describe FROM asp_saas_zjd.test WHERE uri='{uri}'".format(
            uri=uri)
    elif not uri:
        sql = "SELECT uri,method, data,assert,describe FROM asp_saas_zjd.test WHERE describe='{describe}' ".format(
            describe=describe)
    else:
        sql = "SELECT uri,method, data,assert,describe FROM asp_saas_zjd.test WHERE uri='{uri}' and describe='{describe}'".format(
            uri=uri, describe=describe)

    for i in conn.select_data(sql):
        try:

            data = json.loads(i[2])
            asserts = json.loads(i[3])
        except Exception as e:

            data = eval(i[2])
            asserts = eval(i[3])
        finally:
            pass
        li.append({"uri": i[0], "method": i[1], "data": data, "assert": asserts, "describe": i[4]})

    return li


if __name__ == '__main__':
    a = get_request_data("/api/v1/landing-page/landing-pages/pmp")
    print(a)
