import pymysql
import threading
from common.get_config_data import GetConfig


class Connect_Db(object):
    def __init__(self):
        self.gc = GetConfig()
        self.config = self.gc.get_config_data("MYSQL")
        self.connect = pymysql.connect(host=self.config["HOST"],
                                       port=3306,
                                       user=self.config["USER"],
                                       passwd=self.config["PASSWORD"],
                                       db=self.config["DB"],
                                       charset='utf8')
        self.cursor = self.connect.cursor()
        self.lock = threading.Lock()

    def __del__(self):

        self.connect.close()
        self.cursor.close()

    def execute_sql(self, sql):
        """
        执行sql
        :param sql:
        :return:
        """
        self.cursor.execute(sql)

        return self.cursor.execute(sql)

    def insert_data(self, sql):

        """
        执行insert语句插入数据到数据库
        :param sql:
        :return:
        """
        try:
            result = self.execute_sql(sql)
            self.connect.commit()
            return result
        # 错误回滚
        except Exception as E:
            print('\033[1;31;31m err-sql  "{}" {} \033[0m!'.format(sql, E))
            self.connect.rollback()

    def select_data(self, sql):
        """
        执行select语句查询输入,返回所有数据
        :param sql:
        :return:
        """

        try:

            self.execute_sql(sql)
            all_data = self.cursor.fetchall()
            return all_data
        except Exception as E:
            print('\033[1;31;31m err-sql  "{}" {} \033[0m!'.format(sql, E))
            self.connect.rollback()


if __name__ == '__main__':
    c = Connect_Db()
    x = c.insert_data(

        """INSERT INTO `my_data`.`api_auto_test` (`data`,`assert`, `uri`, `method`, `create_time`, `update_time`, `describe`) VALUES ('{\"aa\":\"vv\"}', 'aasdfasd', 'dfasdfasdf', 'fsdafasdf', '2021-08-14 08:37:31', '2021-08-14 08:37:31', NULL);""")
    print(x)
