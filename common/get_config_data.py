import os
import configparser
import inspect


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

    def __init__(self, file_name="config"):
        # 获取当前文件的路径
        current_file_name = inspect.getfile(inspect.currentframe())
        # 获取当前文件的父级目录
        current_path = os.path.dirname(current_file_name)
        current_path = os.path.dirname(current_path) + "/config"
        self.file_name = file_name
        self.file_path = current_path

    # 获取ini的配置文件,返回一个字典
    def get_config_data(self, section):
        cfg = MyConf()
        cfg.read(r"{}\config.ini".format(self.file_path, self.file_name), encoding="utf-8")
        return dict(cfg.items(section))


if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    print(path)
    gc = GetConfig()
    a = gc.get_config_data("EMAIL")
    print(a)

