import random

from ui.mobile_phone import *

logger = Log(__file__)

phone = MobilePhone()

class H5Action(MobilePhone):
    @staticmethod
    def _wait(v, timeout, intervalfunc=None):
        try:
            logger.info(f"开始图片识别{v}")
            address = wait(v, timeout, intervalfunc)
        except:
            logger.error(f"等待{timeout}秒后没有找到图片{v}")
            address = ()
        return address

    def get_now_activity(self):
        return self.phone.shell("dumpsys window | grep mCurrentFocus")

    @staticmethod
    def image_name(image_name):
        return "./image/{}.png".format(image_name)

    @staticmethod
    def get_click_id():
        """
        # 在配置文件中保存了1000多条有用的click_id,这个方法是读取配置文件中的click里面的click_id
        """
        with open("../config/click_id", "r") as f:
            click_id = random.choice(f.readlines())
        return click_id

    def random_click_id(self):
        """ 对拿到的配置文件里面的click_id随机生成一个可以正常上报的click_id用来上报"""
        st = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        s = random.choice(st)
        click_id = self.get_click_id().replace("\n", "")
        _click_id = list(click_id)
        # 修改巨量平台上的可用的click_id末尾的三个字符都可以正常使用的click_id,已验证
        _click_id.pop(random.randint(len(click_id) - 4, len(click_id) - 1))
        _click_id.append(s)
        return "&clickid=" + "".join(
            _click_id) + "&test=api_test&adid=1750461105858564&creativeid=1750461105859595&creativetype=5"

    def open_land_page(self, landing_page_url):
        """
        am start -a android.intent.action.VIEW -d url
        通过adb命令打开落地页，如果手机上只安装了今日头条，会默认使用今日头条打开h5连接
        如果手机上有默认浏览器，会以浏览器打开h5页面

        """
        open_url = landing_page_url + self.random_click_id()
        logger.info("使用adb命令打开的页面的地址{}".format(open_url))
        # 使用adb命令打开落地页
        self.phone.shell(
            "am start -a android.intent.action.VIEW -d '{}'".format(open_url))
        # 先停止今日头条app的运行
        stop_app("com.ss.android.article.news")
        # 查看当前是不是在今日头条打开落地页
        now_activity = self.get_now_activity()
        if "com.ss.android.article.news" not in now_activity:
            today_news_image = self.image_name("today_news")
            # 查看页面是否出现今日头条的图片
            coordinate = self._wait(
                Template(today_news_image, record_pos=(-0.34, 0.423), resolution=(1440, 3200), threshold=0.4),
                timeout=10)
            # 判断页面是否出现使用今日头条打开落地页
            if coordinate:
                loggers.info("选择今日头条打开落地页")
                touch(coordinate)
            else:
                loggers.error("没有找到今日头条，无法从今日头条打开落地页")
        else:
            loggers.info("已经在今日头条打开落地页")
        sleep(3)
        address = self._wait(
            Template(r"{}".format(self.image_name("to_applets")), record_pos=(0.0, -0.704), resolution=(1080, 2400),
                     threshold=0.6),
            timeout=10)
        logger.info(f"返回图片to_applets坐标{address}")
        # 如果返回图片地址和当前页面是在今日头条中打开就点击图片
        if address and "com.ss.android.article.news" in self.get_now_activity():
            if address:
                logger.info("点击图片to_applets")
                touch(address)
            else:
                loggers.error("检查落地页打开的环境，或者没有识别到数据")

    def mian(self):
        self.open_land_page("http://bbb.dbq.yiye.ai/dbq/slLPIPXr?_cl=ffcf")


if __name__ == '__main__':
    h = H5Action()
    h.mian()
