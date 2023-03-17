import nonebot
from nonebot.adapters.onebot.v11 import Adapter

from . import config


def asgi():
    return nonebot.get_asgi()


def driver():
    return nonebot.get_driver()


def init():

    nonebot.init(**{
        "host": config.HOST,
        "port": config.PORT,
        "nickname": config.NICKNAME,
        "superusers": config.SUPERUSERS,
        "command_start": config.COMMAND_START,
        "command_sep": config.COMMAND_SEP,
        "driver": config.DRIVER,
        "session_expire_timeout": config.SESSION_EXPIRE_TIMEOUT,
    })
    driver().register_adapter(Adapter)
    # nonebot.load_plugins("skadi/plugins")
    nonebot.load_plugin("skadi.plugins.test-plugin")
    # nonebot.load_plugin("skadi.plugins.pic-search")
    nonebot.load_plugin("skadi.plugins.picsearch")

def run():
    nonebot.run()

