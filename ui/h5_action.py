# -*- coding: utf-8 -*-

from common.get_config_data import GetConfig
from common.log import Log
from ui import *
from ui.api import CommonApi

logger = Log(__file__)
GC = GetConfig()


class H5Action(CommonApi):

    def open_land_page(self, landing_page_url):
        """
        am start -a android.intent.action.VIEW -d url
        通过adb命令打开落地页，如果手机上只安装了今日头条，会默认使用今日头条打开h5连接
        如果手机上有默认浏览器，会以浏览器打开h5页面

        """

        open_url = landing_page_url + GC.random_click_id()
        logger.info("使用adb命令打开的页面的地址{}".format(open_url))
        # 先停止今日头条app的运行
        stop_app("com.ss.android.article.news")

        # 使用adb命令打开落地页
        self.adb_shell(
            "am start -a android.intent.action.VIEW -d '{}'".format(open_url))

        # 查看当前是不是在今日头条打开落地页
        now_activity = self.get_now_activity()
        if "com.ss.android.article.news" not in now_activity:
            today_news_image = self.image_name("today_news")
            logger.info("当前页面不在今日头条，选择今日头条进入落地页")
            self.touch_image(
                [Template(today_news_image, record_pos=(-0.34, 0.423), resolution=(1440, 3200), threshold=0.4)])
        else:
            logger.info("已经在今日头条打开落地页")
        sleep(3)
        logger.info("开始点击图片跳转到小程序")
        self.touch_image(
            [Template(r"{}".format(self.image_name("to_applets")), record_pos=(0.0, -0.704), resolution=(1080, 2400),
                      threshold=0.6)])

    def mian(self):
        self.open_land_page("http://bbb.dbq.yiye.ai/dbq/slLPIPXr?_cl=ffcf")


if __name__ == '__main__':
    h = H5Action()
    h.mian()
