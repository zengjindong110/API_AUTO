# -*- coding: utf-8 -*-

import configparser
import inspect
import os
import random


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

    def get_click_id(self):
        """
        读取配置好的click_id ，然后随机抽取一个
        """
        with open(f"{self.file_path}/click_id", "r") as f:
            click_id = random.choice(f.readlines())
        return click_id

    def random_click_id(self):
        """ 对拿到的配置文件里面的click_id随机生成一个可以正常上报的click_id用来上报"""
        st = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        s = random.choice(st)
        click_id = self.get_click_id().replace("\n", "")
        _click_id = list(click_id)
        # 修改巨量平台上的可用的click_id末尾的两个字符都可以正常使用的click_id,已验证
        _click_id.pop(random.randint(len(click_id) - 3, len(click_id) - 1))
        _click_id.append(s)
        return "&clickid=" + "".join(
            _click_id) + "&test=api_test&adid=1750461105858564&creativeid=1750461105859595&creativetype=5"

    # 获取ini的配置文件,返回一个字典
    def get_config_data(self, section):
        cfg = MyConf()
        cfg.read(f"{self.file_path}/config.ini", encoding="utf-8")
        return dict(cfg.items(section))

    # 配置请求头
    def get_header(self):
        gateway = self.get_config_data("USER")["HOST"]
        header = {
            "host": gateway[8:],
            "Authorization": self.get_config_data("USER")["TOKEN"],
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
        return self.get_config_data("PMP")["PMP_ID"]


if __name__ == '__main__':
    gc = GetConfig()
    # a = gc.get_config_data("EMAIL")
    a = gc.get_config_data("EMAIL")
    print(a)
