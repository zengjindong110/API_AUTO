from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from ui.mobile_phone import *

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

logger = Log(__file__)

"""
小程序添加好友的链路在这里面编写
除了长按识别二维码是通过airtest的方法写的
其他的动作都是通过poco写的，因为在微信环境里面一些控件不会随便更改

"""


class AppletAction(MobilePhone):

    def check_page(self):
        # 获取当前页面的activition
        now_dev = self.phone.shell("dumpsys window | grep mCurrentFocus")
        # com.tencent.mm.plugin.appbrand.ui.AppBrandUI 为添加好友的二维码页面
        if "com.tencent.mm.plugin.appbrand.ui.AppBrandUI" in now_dev or "com.tencent.mm.plugin.profile.ui.ContactInfoUI" in now_dev:
            loggers.info("当前在小程序环境，为小程序的二维码展示页面!!!!!")
        else:
            loggers.error("当前不在小程序环境!!!!!")
            raise "当前不是小程序环境，检查脚本为什么没有跳转到小程序"

    def long_touch_qr_code(self):
        sleep(10)
        loggers.info("开始识别二维码")
        qr_code = "./image/QR_code.png"
        try:
            qr_code_address = wait(
                Template(r"{}".format(qr_code), record_pos=(-0.006, -0.507), resolution=(1080, 2400)), timeout=30)
        except TargetNotFoundError as e:
            qr_code_address = ()
            loggers.error(f"小程序里面的二维码没有识别到，检查二维码{e}")
        touch(qr_code_address, duration=3)

    def click_friends(slef):
        sleep(3)
        loggers.info("通过小程序长按后，点击好友名字")
        poco("com.tencent.mm:id/ky_").wait_for_appearance(10)
        poco("com.tencent.mm:id/ky_").click()

    def go_friends(self):
        loggers.info("跳转到添加好友按钮的页面")
        # if "com.tencent.mm.plugin.profile.ui.ContactInfoUI" in now_dev:
        a = poco(text="添加到通讯录").wait_for_appearance(100)
        print(a)
        poco(text="添加到通讯录").click()
        poco(text="发消息").wait_for_appearance(10)
        assert_equal(poco(text="发消息").exists(), True, "添加好友成功")

    def delete_friend(self):
        # poco(desc).wait_for_appearance(10)
        """
        com.tencent.mm:id/eo   为页面上的三个点 ...
        com.tencent.mm:id/khj  为页面上的删除按钮
        com.tencent.mm:id/guw  为页面上的确认删除按钮

        """
        sleep(3)
        poco("com.tencent.mm:id/eo").wait_for_appearance(10)

        poco("com.tencent.mm:id/eo").click()
        sleep(3)
        poco("com.tencent.mm:id/khj").wait_for_appearance(10)
        poco("com.tencent.mm:id/khj").click()
        sleep(3)
        poco("com.tencent.mm:id/guw").wait_for_appearance(10)
        poco("com.tencent.mm:id/guw").click()
        sleep(3)
        now_dev = self.phone.shell("dumpsys window | grep mCurrentFocus")
        if "com.tencent.mm.plugin.appbrand.ui.AppBrandUI" in now_dev:
            assert_true(True, "好友删除成功")

    def add_friend(self):
        sleep(5)
        self.long_touch_qr_code()
        sleep(2)
        self.click_friends()
        sleep(2)
        self.go_friends()
        sleep(2)
        self.delete_friend()


if __name__ == '__main__':
    a = AppletAction()
    a.add_friend()
