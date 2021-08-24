# coding=utf8

import json
from common.connect_db import Connect_Db


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

        data = eval(i[2])
        asserts = eval(i[3])

        li.append({"uri": i[0], "method": i[1], "data": data, "assert": asserts, "describe": i[4]})

    return li


if __name__ == '__main__':
    a = get_request_data("/api/v1/marketing/advertiser-account-groups/collect/list")
    b = json.dumps(a[0])
    print(a)
