import sys

from airtest.core.api import *
from airtest.core.error import AirtestError

from common.log import Log

logger = Log(__file__)

try:
    phone = connect_device("Android:///")
    wake()
except IndexError:
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
        logger.info("今日头条app已经安装+True")
    else:
        phone_statue.append(False)
        logger.error("请安装今日头条app+False")

    # 查看屏幕是不是亮的
    phone_screen = phone.is_screenon()
    if phone_screen:
        phone_statue.append(True)
        logger.info("手机屏幕已经是亮的+True")
    else:

        logger.error("手机屏幕没有亮,请点亮屏幕")
        shell("input keyevent 26")
        phone_statue.append(True)
        logger.info("唤醒手机屏幕+True")

    is_locked = phone.is_locked()

    if not is_locked:
        phone_statue.append(True)
        logger.info("手机未锁定+True")
    else:
        phone_statue.append(False)
        logger.error("手机以上锁,先解锁 +False")
    try:
        browser = phone.path_app("com.android.browser")
    except AirtestError:
        browser = False
    if browser:
        logger.error(
            "检查手机上是否存在默认的浏览器，如果执行--  adb shell pm uninstall -k --user 0 com.android.browser 进行删除 +False ")
        phone_statue.append(False)
    else:
        logger.info("手机默认的浏览器已经卸载 +True")
        phone_statue.append(True)

    if False in phone_statue:
        phone = None
        sys.exit()


else:
    logger.error("手机未连接或者未开启USB调试")
    sys.exit()


class CommonApi(object):

    @staticmethod
    def touch_image(tem_list: list):
        """
        封装atirtest，支持传入多张图片,识别到其中一个就进行点击,传入的值是Template 或者是一个列表里面用元组包含多个参数
        支持传入timeout 和 duration 输入的数值小于5默认为duration，大于5的为timeout
        eg：
        self.touch_image[Template(r"./image/too_more.png", record_pos=(0.428, -0.983), resolution=(1440, 3200)),
        Template(r"./image/too_more.png", record_pos=(0.428, -0.983), resolution=(1440, 3200))]
        or
        self.touch_image[(Template(r"./image/too_more.png", record_pos=(0.428, -0.983), resolution=(1440, 3200)),5,20),
        (Template(r"./image/too_more.png", record_pos=(0.428, -0.983), resolution=(1440, 3200)),5,20)]
        """
        timeout = 20
        duration = 0.3
        for i in tem_list:
            if isinstance(i, tuple):
                for params in i[1:]:
                    if params > 5:
                        timeout = params
                    else:
                        duration = params
        address = ()
        i = ""
        for i in tem_list:
            i = i
            try:
                if isinstance(i, tuple):
                    logger.info(f"开始识别图片{i}")
                    address = wait(i[0], timeout=timeout)
                    break
                else:
                    address = wait(i)
                    break
            except TargetNotFoundError:
                logger.error(f"没有识别出来{i}")
        logger.info(f"点击图片{i}，位置为{address},点击图片的时间为{duration}")
        touch(address, duration=duration)

    @staticmethod
    def get_now_activity():
        """
        获取当前页面的activity
        """
        new_activity = phone.shell("dumpsys window | grep mCurrentFocus")
        logger.info(f"获取当前页面的activity为{new_activity}")
        return new_activity

    @staticmethod
    def adb_shell(adb_shell):
        """执行adb命令"""
        logger.info(f"执行adb命令{adb_shell}")
        phone.shell(adb_shell)

    @staticmethod
    def image_name(image_name):
        """封装的图片地址，直接传入图片名称就可以"""
        return "./image/{}.png".format(image_name)


if __name__ == '__main__':
    a = CommonApi()
    a.get_now_activity()

    a.adb_shell("am start -a android.intent.action.VIEW -d 'http://www.baidu.com'")
