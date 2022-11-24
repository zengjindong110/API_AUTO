from ui import *


class H5Action(MobilePhone):
    def open_land_page(self,landing_page_url):
        ones_jump_page = "./image/to_applets.png"
        self.phone.shell("am start -a android.intent.action.VIEW -d {}".format(landing_page_url))
        sleep(3)
        assert_exists(Template(r"{}".format(ones_jump_page), record_pos=(0.0, -0.704), resolution=(1080, 2400)), "判断一跳一落地页是否打开")
        touch(Template(r"{}".format(ones_jump_page), record_pos=(0.004, -0.702), resolution=(1080, 2400)))

    def mian(self):
        self.open_land_page("http://bbb.dbq.yiye.ai/dbq/slLPIPXr?_cl=ffcf")

if __name__ == '__main__':
    h = H5Action()
    h.mian()