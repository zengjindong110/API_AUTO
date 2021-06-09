# coding=gbk
import csv
import os
from typing import List
import pymysql
import config


# ��csv����ʽ��ȡ����
def read_csv() -> List[dict]:
    li = list()
    path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "/test_case/test_api.csv"
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for i in list(reader)[1:]:
            li.append({"method": i[1], "uri": i[2], "data": i[3], "assert": i[4]})
    return li


def select_data(sql):

    conn = pymysql.connect(host=config.mysql_host, port=config.mysql_port, user=config.mysql_user,
                           passwd=config.mysql_passworld, db=config.mysql_db, charset='utf8')
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


# �������ݿ��ȡ����
def get_request_data(uri=None, describe=None):
    li = list()
    if not describe:
        sql = "SELECT `uri`,`method`, `data`,`assert`,`describe` FROM `lbdj`.`api_auto_test` WHERE `uri`='{uri}'".format(
            uri=uri)
    elif not uri:
        sql = "SELECT `uri`,`method`, `data`,`assert`,`describe` FROM `lbdj`.`api_auto_test` WHERE `describe`='{describe}' ".format(
            describe=describe)
    else:
        sql = "SELECT `uri`,`method`, `data`,`assert`,`describe` FROM `lbdj`.`api_auto_test` WHERE `uri`='{uri}' and `describe`='{describe}'".format(
            uri=uri, describe=describe)

    for i in select_data(sql):
        li.append({"uri": i[0], "method": i[1], "data": i[2], "assert": i[3], "describe": i[4]})
    return li


if __name__ == '__main__':
    import json
    getCategoryData = json.loads(get_request_data("/lbdj/app/order/AppGrabOrderHallApiRequest", "�鿴ʦ�����۶���")[0]["data"])
    print(getCategoryData)
    getCategoryData["token"] = config.worker_environment["test"]["token"]
    print(getCategoryData)
