from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from ui import *

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

phone = MobilePhone()

logger = Log(__file__)


class AppletAction(object):
    def __init__(self):
        # 获取当前页面的activition
        now_dev = phone.mobile().shell("dumpsys window | grep mCurrentFocus")
        # com.tencent.mm.plugin.appbrand.ui.AppBrandUI 为添加好友的二维码页面
        if "com.tencent.mm.plugin.appbrand.ui.AppBrandUI" in now_dev or "com.tencent.mm.plugin.profile.ui.ContactInfoUI" in now_dev:
            loggers.info("当前在小程序环境，为小程序的二维码展示页面!!!!!")
        else:
            loggers.error("当前不在小程序环境!!!!!")
            raise "当前不是小程序环境，检查脚本为什么没有跳转到小程序"

    @staticmethod
    def long_touch_qr_code():
        sleep(5)
        loggers.info("开始识别二维码")
        qr_code = "./image/QR_code.png"
        try:
            qr_code_address = wait(
                Template(r"{}".format(qr_code), record_pos=(-0.006, -0.507), resolution=(1080, 2400)), timeout=30)
        except TargetNotFoundError as e:
            qr_code_address = ()
            loggers.error(f"小程序里面的二维码没有识别到，检查二维码{e}")
        touch(qr_code_address, duration=2)

    @staticmethod
    def click_friends():
        loggers.info("通过小程序长按后，点击好友名字")
        poco(text="打开对方的企业微信名片").wait_for_appearance(10)
        poco(text="打开对方的企业微信名片").click()

    @staticmethod
    def go_friends():
        loggers.info("跳转到添加好友按钮的页面")
        # if "com.tencent.mm.plugin.profile.ui.ContactInfoUI" in now_dev:
        poco(text="添加到通讯录").wait_for_appearance(10)
        poco(text="添加到通讯录").click()
        poco(text="发消息").wait_for_appearance(10)
        assert_equal(poco(text="发消息").exists(), True, "添加好友成功")

    @staticmethod
    def delete_friend():
        # poco(desc).wait_for_appearance(10)
        poco("com.tencent.mm:id/eo").wait_for_appearance(10)
        poco("com.tencent.mm:id/eo").click()
        poco("com.tencent.mm:id/khj").wait_for_appearance(10)
        poco("com.tencent.mm:id/khj").click()
        poco("com.tencent.mm:id/guw").wait_for_appearance(10)
        poco("com.tencent.mm:id/guw").click()
        sleep(3)
        now_dev = phone.mobile().shell("dumpsys window | grep mCurrentFocus")
        if "com.tencent.mm.plugin.appbrand.ui.AppBrandUI" in now_dev:
            assert_true(True, "好友删除成功")

    def add_friend(self):
        self.long_touch_qr_code()
        self.click_friends()
        self.go_friends()
        self.add_friend()


if __name__ == '__main__':
    a = AppletAction()
    a.add_friend()
