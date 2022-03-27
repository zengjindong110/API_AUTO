import configparser
import inspect
import os

import config


# 重写获取配置文件的方法,让读取出来的内容变为大写的
class MyConf(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr


class GetConfig(object):
    """
    取配置文件的内容
    返回字典
    """

    def __init__(self):
        # 获取当前文件的路径
        current_file_name = inspect.getfile(inspect.currentframe())
        # 获取当前文件的父级目录
        current_path = os.path.dirname(current_file_name)
        current_path = os.path.dirname(current_path) + "/config"
        self.file_name = "config"
        self.file_path = current_path

    # 获取ini的配置文件,返回一个字典
    def get_config_data(self, section):
        cfg = MyConf()
        cfg.read(r"{}\config.ini".format(self.file_path, self.file_name), encoding="utf-8")
        return dict(cfg.items(section))

    # 配置请求头
    def get_header(self):
        gateway = self.get_config_data("USER")["HOST"]
        header = {
            "host": gateway[8:],
            "Authorization": config.TOKEN["token"],
            "accept": "application/json, text/plain, */*",
            "useR-agent": "mozilla/5.0 (windOWs NT 10.0; Win64; x64) aPplEwebKit/537.36 (KHTml, lIke gecKo) chrome/99.0.4844.51 safari/537.36",
            "type": "",
            "X-Y-version": "1.130.0",
            "sec-ch-ua-platform": "windows",
            "origin": gateway,
            "seC-fetcH-site": "same-origin",
            "seC-fetcH-mode": "cors",
            "seC-fetcH-dest": "empty",
            "referer": gateway,
            "accepT-language": "Zh-cN,zh;q=0.9,En-US;q=0.8,en;q=0.7,Zh-TW;q=0.6",
        }
        return header

    def get_pmp_id(self):
        return config.PMP_ID


if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    print(path)
    gc = GetConfig()
    # a = gc.get_config_data("EMAIL")
    a = gc.get_header()

    print(a)
