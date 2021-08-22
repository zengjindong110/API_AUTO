# coding=utf-8
import logging
import os
import time

current_path = os.path.dirname(__file__)
parent_path = os.path.dirname(current_path)


class Log(object):
    def __init__(self, name=__name__,
                 path=parent_path + '/log/{}.log'.format(time.strftime("%Y-%m-%d", time.localtime())), level='DEBUG'):
        self.__name = name
        self.__path = path
        self.__level = level
        self.__logger = logging.getLogger()
        self.__logger.setLevel(level=logging.INFO)

    # def __ini_handler(self):
    #     """初始化handler"""
    #     stream_handler = logging.StreamHandler()
    #     file_handler = logging.FileHandler(self.__path, encoding='utf-8')
    #     return stream_handler, file_handler
    def __ini_handler(self):
        """初始化handler"""
        self.__logger.handlers.clear()
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(self.__path, encoding='utf-8')
        return stream_handler, file_handler

    def __set_handler(self, stream_handler, file_handler, level='DEBUG'):
        """设置handler级别并添加到logger收集器"""
        stream_handler.setLevel(level)
        file_handler.setLevel(level)
        self.__logger.addHandler(stream_handler)
        self.__logger.addHandler(file_handler)

    def __set_formatter(self, stream_handler, file_handler):
        """设置日志输出格式"""
        formatter = logging.Formatter('%(asctime)s-%(name)s-%(filename)s-[line:%(lineno)d]'
                                      '-%(levelname)s-[日志信息]: %(message)s',
                                      datefmt='%a, %d %b %Y %H:%M:%S')
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

    def __close_handler(self, stream_handler, file_handler):
        """关闭handler"""
        stream_handler.close()
        file_handler.close()

    @property
    def Logger(self):
        """构造收集器，返回looger"""
        stream_handler, file_handler = self.__ini_handler()
        self.__set_handler(stream_handler, file_handler)
        self.__set_formatter(stream_handler, file_handler)
        self.__close_handler(stream_handler, file_handler)
        return self.__logger
