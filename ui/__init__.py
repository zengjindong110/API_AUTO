import logging

from airtest.core.api import *

# 调整Airtest的日志等级
loggers = logging.getLogger("airtest")
loggers.setLevel(logging.ERROR)

# 初始化airtet
auto_setup(__file__)

