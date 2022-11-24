__author__ = "Airtest"

import logging

from airtest.core.api import *

from common.log import Log

loggers = Log(__file__)
# 调整airtet的日志等级
logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)

# 初始化airtet
auto_setup(__file__)


class MobilePhone(object):

    def __init__(self):

        try:
            phone = connect_device("Android:///")
        except IndexError as e:
            phone = None
        phone_statue = []
        if phone:
            # 查看手机里面是否安装今日头条
            app_package = phone.check_app("com.ss.android.article.news")
            if app_package:
                phone_statue.append(True)
                loggers.info("今日头条app已经安装+True")
            else:
                phone_statue.append(False)
                loggers.error("请安装今日头条app+False")

            # 查看屏幕是不是亮的
            phone_screen = phone.is_screenon()
            if phone_screen:
                phone_statue.append(True)
                loggers.info("手机屏幕已经是亮的+True")
            else:

                loggers.error("手机屏幕没有亮,请点亮屏幕")
                shell("input keyevent 26")
                phone_statue.append(True)
                loggers.info("唤醒手机屏幕+True")

            is_locked = phone.is_locked()

            if not is_locked:
                phone_statue.append(True)
                loggers.info("手机未锁定+True")
            else:
                phone_statue.append(False)
                loggers.info("手机以上锁,先解锁 +False")

            if False in phone_statue:
                self.phone = None
            else:
                self.phone = phone
            print(phone_statue)

        else:
            loggers.error("手机没有链接上,连接手机后再试")

    def mobile(self):
        return self.phone



# dev.shell("am start -a android.intent.action.VIEW -d http://bbb.dbq.yiye.ai/dbq/slLPIPXr?_cl=ffcf")
# sleep(3)
#
# touch(Template(r"./image/to_applets.png", record_pos=(-0.007, -0.474), resolution=(1080, 2400)))
