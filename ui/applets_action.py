from ui import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

class AppletAction(MobilePhone):

    def long_touch_qr_code(self):
        sleep(1)
        qr_code = "./image/QR_code.jpg"
        touch(Template(r"{}".format(qr_code), record_pos=(-0.006, -0.507), resolution=(1080, 2400)),duration=2)

    def click_friends(self):
        click_friends_image = "./image/click_friends.jpg"
        touch(Template(r"{}".format(click_friends_image), record_pos=(0.011, 0.83), resolution=(1080, 2400)))

    def add_friends(self):
        poco(text="添加到通讯录").click()

    def main(self):
        # self.long_touch_qr_code()
        # self.click_friends()
        self.add_friends()
if __name__ == '__main__':
    a = AppletAction()
    a.main()