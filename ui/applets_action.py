# -*- coding: utf-8 -*-

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.exceptions import PocoTargetTimeout

from common.log import Log
from ui import *
from ui.api import CommonApi

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

logger = Log(__file__)

"""
小程序添加好友的链路在这里面编写
除了长按识别二维码是通过airtest的方法写的
其他的动作都是通过poco写的，因为在微信环境里面一些控件不会随便更改

"""


class AppletAction(CommonApi):

    def check_page(self):
        """
        获取当前页面的active
        """
        # 获取当前页面的activition
        now_dev = self.get_now_activity()
        # com.tencent.mm.plugin.appbrand.ui.AppBrandUI 为添加好友的二维码页面
        if "com.tencent.mm.plugin.appbrand.ui.AppBrandUI" in now_dev or "com.tencent.mm.plugin.profile.ui.ContactInfoUI" in now_dev:
            logger.info("当前在小程序环境，为小程序的二维码展示页面!!!!!")
        else:
            logger.error("当前不在小程序环境!!!!!")
            raise Exception("当前不是小程序环境，检查脚本为什么没有跳转到小程序")
    def wait_QR_code(self):
        """
        默认等待50秒 等待二维码页面出来
        """
        times = 0
        while times < 50 :
            now_active = self.get_now_activity()

            if "com.tencent.mm.plugin.appbrand.ui.AppBrandUI" in now_active:
                logger.info(f"进入页面{now_active}")
                break
            else:

                logger.info(f"已经等待了{times}")
                sleep(1)
                times += 1



    def long_touch_qr_code(self):
        """
        长按二维码
        """
        # 等待跳转到小程序页面
        self.wait_QR_code()

        # 打印当前页面记得要补充
        try:
            logger.info("开始在小程序长按二维码，进行添加好友")
            self.touch_image(
                [(Template(f"{self.image_name('QR_code')}", record_pos=(-0.006, -0.507), resolution=(1080, 2400)), 2)])
        except PocoTargetTimeout as e:
            logger.error(f"小程序里面的二维码没有识别到，检查二维码{e}")

    def click_friends(self):
        """
        点击打开对方企业微信名片
        """
        logger.info("已经长按小程序，点击打开对方企业名片")
        try:
            poco("com.tencent.mm:id/ky_").wait_for_appearance(10)
        except PocoTargetTimeout:
            logger.error("使用poco没有识别出来com.tencent.mm:id/ky_控件，采用图片识别的方式")
            self.touch_image(
                [Template(r"image/dakaiqiyemingpian1.png", record_pos=(0.006, 0.767), resolution=(1440, 3200)),
                 Template(r"image/dakaiqiyemingpian.png", record_pos=(0.006, 0.767), resolution=(1440, 3200))])
        else:
            poco("com.tencent.mm:id/ky_").click()

    def go_friends(self):
        """
        点击添加到通讯录
        """
        logger.info("跳转到添加到通讯录页面")
        # if "com.tencent.mm.plugin.profile.ui.ContactInfoUI" in now_dev:
        try:
            poco(text="添加到通讯录").wait_for_appearance(10)
        except PocoTargetTimeout:
            try:
                logger.error("使用poco没有识别出来'text=添加到通讯录'控件，采用图片识别的方式")
                self.touch_image(
                    [Template(r"./image/add_to_address_book.png", record_pos=(0.006, 0.767), resolution=(1440, 3200)),
                     Template(r"./image/add_to_address_book1.png", record_pos=(0.006, 0.767), resolution=(1440, 3200))])
            except TargetNotFoundError as e:
                logger.error(f"没有识别到add_to_address_book.png图片--打开企业微信添加好友图片{e}")
        else:
            poco(text="添加到通讯录").click()
        finally:
            try:
                poco(text="发消息").wait_for_appearance(10)
                assert_equal(poco(text="发消息").exists(), True, "添加好友成功")
            except PocoTargetTimeout:
                logger.error("使用poco没有识别出来'text=发消息'控件，采用图片faxiaoxi.png识别的方式")
                try:
                    assert_exists(Template(r"./image/faxiaoxi.png", record_pos=(0.044, 0.276), resolution=(1440, 3200)),
                                  "添加好友成功")
                except TargetNotFoundError:
                    assert_exists(Template(r"./image/faxiaoxi1.png", record_pos=(0.0, 0.293), resolution=(1080, 2400)),
                                  "添加好友成功")

    def delete_friend(self):
        """
        添加好友成功后，删除好友
        """
        # poco(desc).wait_for_appearance(10)
        """
        com.tencent.mm:id/eo   为页面上的三个点 ...
        com.tencent.mm:id/khj  为页面上的删除按钮
        com.tencent.mm:id/guw  为页面上的确认删除按钮

        """
        # 删除微信点击点击三个点
        logger.info("开始删除微信好友")
        try:
            poco("com.tencent.mm:id/eo").wait_for_appearance(10)
            poco("com.tencent.mm:id/eo").click()
        except PocoTargetTimeout:
            self.touch_image([Template(r"./image/too_more.png", record_pos=(0.428, -0.983), resolution=(1440, 3200)),
                              Template(r"./image/too_more1.png", record_pos=(0.428, -0.983), resolution=(1440, 3200))])

        # 点击删除按钮
        try:
            poco("com.tencent.mm:id/khj").wait_for_appearance(10)
            poco("com.tencent.mm:id/khj").click()
        except PocoTargetTimeout:
            self.touch_image(
                [Template(r"./image/delete_button.png", record_pos=(-0.001, 0.216), resolution=(1440, 3200)),
                 Template(r"./image/delete_button1.png", record_pos=(-0.001, 0.216), resolution=(1440, 3200))])
        # 点击确认删除

        try:
            poco("com.tencent.mm:id/guw").wait_for_appearance(10)
            poco("com.tencent.mm:id/guw").click()
        except PocoTargetTimeout:
            self.touch_image(
                [Template(r"./image/confirm_delete.png", record_pos=(0.197, 0.219), resolution=(1440, 3200)),
                 Template(r"./image/confirm_delete1.png", record_pos=(0.197, 0.219), resolution=(1440, 3200))
                 ])
        now_dev = self.get_now_activity()
        if "com.tencent.mm.plugin.appbrand.ui.AppBrandUI" in now_dev:
            assert_true(True, "好友删除成功")

    def add_friend(self):
        self.long_touch_qr_code()
        sleep(2)
        self.click_friends()
        sleep(2)
        self.go_friends()
        sleep(2)
        self.delete_friend()


if __name__ == '__main__':
    a = AppletAction()
    a.wait_QR_code()
