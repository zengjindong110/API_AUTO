import logging
import sys

from airtest.core.api import *
from common.log import Log as init_log

loggers = init_log(__file__)

# 调整airtet的日志等级
logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)

# 初始化airtet
auto_setup(__file__)

try:
    phone = connect_device("Android:///")
    wake()
except IndexError as e:
    phone = None

"""
初始化的时候检查设备的状态
"""

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
        loggers.error("手机以上锁,先解锁 +False")
    try:
        browser = phone.path_app("com.android.browser")
    except:
        browser = False
    if browser:
        loggers.error(
            "检查手机上是否存在默认的浏览器，如果执行--  adb shell pm uninstall -k --user 0 com.android.browser 进行删除 +False ")
        phone_statue.append(False)
    else:
        loggers.info("手机默认的浏览器已经卸载 +True")
        phone_statue.append(True)

    if False in phone_statue:
        phone = None
        sys.exit()


else:
    loggers.error("手机未连接或者未开启USB调试")
    sys.exit()

# dev.shell("am start -a android.intent.action.VIEW -d http://bbb.dbq.yiye.ai/dbq/slLPIPXr?_cl=ffcf")
# sleep(3)
#
# touch(Template(r"./image/to_applets.png", record_pos=(-0.007, -0.474), resolution=(1080, 2400)))
