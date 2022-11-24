from ui import *


class H5Action(MobilePhone):
    def open_land_page(self):
        self.phone.shell("am start -a android.intent.action.VIEW -d http://bbb.dbq.yiye.ai/dbq/slLPIPXr?_cl=ffcf")


if __name__ == '__main__':
    h = H5Action()
    h.open_land_page()