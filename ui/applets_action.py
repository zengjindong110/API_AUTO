from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.exceptions import PocoTargetTimeout

from common.log import Log
from ui import *

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

logger = Log(__file__)

"""
小程序添加好友的链路在这里面编写
除了长按识别二维码是通过airtest的方法写的
其他的动作都是通过poco写的，因为在微信环境里面一些控件不会随便更改

"""


class AppletAction(object):
    def touch_image(self, tem_list):
        """
        封装atirtest，支持传入多张图片,识别到其中一个就进行点击,传入的值是Template
        Template(r"./image/too_more.png", record_pos=(0.428, -0.983), resolution=(1440, 3200))
        """

        for i in tem_list:
            timeout = 20
            duration = 0.3
            if type(i) == "tuple":
                for params in i[1:]:
                    if params > 5:
                        timeout = params
                    else:
                        duration = params
            try:

                if type(i) == "tuple":
                    loggers.info(f"开始识别图片{i}")
                    address = wait(i[0], timeout=timeout)
                else:
                    address = wait(i)

                if address:
                    logger.info(f"识别出来图片{i}的坐标{address}")

            except TargetNotFoundError:
                logger.error(f"图片没有识别出来{i}")
            else:
                logger.info(f"点击图片{i}，位置为{address},点击图片的时间为{duration}")
                touch(address, duration=duration)

    #
    def check_page(self):
        # 获取当前页面的activition
        now_dev = phone.shell("dumpsys window | grep mCurrentFocus")
        # com.tencent.mm.plugin.appbrand.ui.AppBrandUI 为添加好友的二维码页面
        if "com.tencent.mm.plugin.appbrand.ui.AppBrandUI" in now_dev or "com.tencent.mm.plugin.profile.ui.ContactInfoUI" in now_dev:
            logger.info("当前在小程序环境，为小程序的二维码展示页面!!!!!")
        else:
            logger.error("当前不在小程序环境!!!!!")
            raise Exception("当前不是小程序环境，检查脚本为什么没有跳转到小程序")

    def long_touch_qr_code(self):
        sleep(10)
        # 打印当前页面记得要补充
        qr_code = "./image/QR_code.png"
        try:
            logger.info("开始在小程序长按二维码，进行添加好友")
            # qr_code_address = wait(
            #     Template(r"{}".format(qr_code), record_pos=(-0.006, -0.507), resolution=(1080, 2400)), timeout=30)
            self.touch_image(
                [(Template(r"{}".format(qr_code), record_pos=(-0.006, -0.507), resolution=(1080, 2400)), 3)])
        except PocoTargetTimeout as e:
            logger.error(f"小程序里面的二维码没有识别到，检查二维码{e}")

    def click_friends(self):
        sleep(3)
        logger.info("已经长按小程序，点击打开对方企业名片")
        try:
            poco("com.tencent.mm:id/ky_").wait_for_appearance(10)
        except PocoTargetTimeout:
            logger.error("使用poco没有识别出来com.tencent.mm:id/ky_控件，采用图片识别的方式")
            # touch(Template(r"image/dakaiqiyemingpian1.png", record_pos=(0.006, 0.767), resolution=(1440, 3200)))
            self.touch_image(
                [Template(r"image/dakaiqiyemingpian1.png", record_pos=(0.006, 0.767), resolution=(1440, 3200))])
        else:
            poco("com.tencent.mm:id/ky_").click()

    def go_friends(self):
        logger.info("跳转到添加到通讯录页面")
        # if "com.tencent.mm.plugin.profile.ui.ContactInfoUI" in now_dev:
        try:
            poco(text="添加到通讯录").wait_for_appearance(10)

        except PocoTargetTimeout:
            try:
                logger.error("使用poco没有识别出来'text=添加到通讯录'控件，采用图片识别的方式")
                # touch(Template(r"./image/add_to_address_book.png", record_pos=(0.006, 0.767), resolution=(1440, 3200)))
                self.touch_image(
                    [Template(r"./image/add_to_address_book.png", record_pos=(0.006, 0.767), resolution=(1440, 3200))])
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
                assert_exists(Template(r"./image/faxiaoxi.png", record_pos=(0.044, 0.276), resolution=(1440, 3200)),
                              "请填写测试点")

    def delete_friend(self):
        # poco(desc).wait_for_appearance(10)
        """
        com.tencent.mm:id/eo   为页面上的三个点 ...
        com.tencent.mm:id/khj  为页面上的删除按钮
        com.tencent.mm:id/guw  为页面上的确认删除按钮

        """
        # 删除微信点击点击三个点
        sleep(3)
        try:
            poco("com.tencent.mm:id/eo").wait_for_appearance(10)
            poco("com.tencent.mm:id/eo").click()
        except PocoTargetTimeout:
            # try:
            #     too_more = wait(Template(r"./image/too_more.png", record_pos=(0.428, -0.983), resolution=(1440, 3200)))
            # except TargetNotFoundError:
            #     logger.error("没有识别到...的图片")
            # else:
            #     touch(too_more)
            self.touch_image([Template(r"./image/too_more.png", record_pos=(0.428, -0.983), resolution=(1440, 3200))])

        # 点击删除按钮
        try:
            poco("com.tencent.mm:id/khj").wait_for_appearance(10)

            poco("com.tencent.mm:id/khj").click()
        except PocoTargetTimeout:
            # try:
            #     delete_button = wait(
            #         Template(r"./image/delete_button.png", record_pos=(-0.001, 0.216), resolution=(1440, 3200)))
            # except TargetNotFoundError:
            #     logger.error("通过图片识别没有识别到delete_button的图片")
            # else:
            #     touch(delete_button)
            self.touch_image(
                [Template(r"./image/delete_button.png", record_pos=(-0.001, 0.216), resolution=(1440, 3200))])
        # 点击确认删除
        sleep(3)
        try:
            poco("com.tencent.mm:id/guw").wait_for_appearance(10)
            poco("com.tencent.mm:id/guw").click()
        except PocoTargetTimeout:
            # try:
            #     confirm_delete = wait(
            #         Template(r"./image/confirm_delete.png", record_pos=(0.197, 0.219), resolution=(1440, 3200)))
            # except TargetNotFoundError:
            #     logger.error("通过图片识别没有识别到confirm_delete的图片")
            # else:
            #     touch(confirm_delete)
            self.touch_image(
                [Template(r"./image/confirm_delete.png", record_pos=(0.197, 0.219), resolution=(1440, 3200))])
        sleep(3)
        now_dev = phone.shell("dumpsys window | grep mCurrentFocus")
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
    a.add_friend()
