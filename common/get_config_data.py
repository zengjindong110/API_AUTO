import os
import configparser


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

    def __init__(self, file_path, file_name="config"):
        self.file_name = file_name
        self.file_path = file_path

    # 获取ini的配置文件,返回一个字典
    def get_config_data(self, section):
        cfg = MyConf()
        cfg.read(r"{}\config.ini".format(self.file_path, self.file_name), encoding="utf-8")
        return dict(cfg.items(section))


if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    print(path)
    gc = GetConfig(path, "config")
    a = gc.get_config_data("GATEWAY")
    print(a)
    print(a["AGENT_HOST"])
