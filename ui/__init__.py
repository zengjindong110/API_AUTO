__author__ = "Airtest"
import logging
from airtest.core.api import *


# 调整airtet的日志等级
logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)

# 初始化airtet
auto_setup(__file__)


dev = connect_device("Android:///")




dev.shell("am start -a android.intent.action.VIEW -d http://bbb.dbq.yiye.ai/dbq/slLPIPXr?_cl=ffcf")
sleep(3)

touch(Template(r"./image/to_applets.png", record_pos=(-0.007, -0.474), resolution=(1080, 2400)))
