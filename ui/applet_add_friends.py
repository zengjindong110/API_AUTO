# -*- coding: utf-8 -*-

from ui.applets_action import AppletAction
from ui.h5_action import H5Action


class AddFriend(AppletAction, H5Action):

    def h5_applet_add(self, once_jump_page_url):
        """
        一跳落地页为H5落地页跳转到自己的小程序后添加好友
        """
        self.open_land_page(once_jump_page_url)
        print(1111111)
        self.add_friend()


if __name__ == '__main__':
    a = AddFriend()
    a.h5_applet_add("http://bbb.dbq.yiye.ai/dbq/slLPIPXr?_cl=ffcf")
