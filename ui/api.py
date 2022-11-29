from common.log import Log
from airtest.core.api import *
from ui import phone

logger = Log(__file__)


class CommonApi(object):

    @staticmethod
    def touch_image(tem_list):
        """
        封装atirtest，支持传入多张图片,识别到其中一个就进行点击,传入的值是Template
        Template(r"./image/too_more.png", record_pos=(0.428, -0.983), resolution=(1440, 3200))
        """

        for i in tem_list:
            timeout = 20
            duration = 0.3
            if isinstance(i, tuple):
                for params in i[1:]:
                    if params > 5:
                        timeout = params
                    else:
                        duration = params
            try:
                if isinstance(i, tuple):
                    logger.info(f"开始识别图片{i}")
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

    @staticmethod
    def get_now_activity():
        new_activity = phone.shell("dumpsys window | grep mCurrentFocus")
        logger.info(f"获取当前页面的activity为{new_activity}")
        return new_activity


if __name__ == '__main__':
    a = CommonApi()
    a.get_now_activity()
