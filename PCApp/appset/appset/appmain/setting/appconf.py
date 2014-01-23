#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-10 23:17

>>> import os
>>> import tempfile
>>> filename = os.path.join(tempfile.gettempdir(), "appset.conf")
>>> appConf = AppConf(filename)
>>> appConf.loadConf()
>>> appConf.isHideInTray()
False
>>> appConf.setHideInTray(True)
>>> appConf.saveConf()
>>> appConf.setHideInTray(False)
>>> appConf.loadConf()
>>> appConf.isHideInTray()
True
"""

from abstract.commconfile import CommonConf


class AppConf(CommonConf):
    # default config values
    _DEF_CONF = {
        "hide_in_tray": True,
        "ask_hide_in_tray": True,
        "data_dir": "./data",
        "default_mod": "LunarMod"
    }

    # default config file
    _CONFIG_FILE_NAME = "./config/appset.conf"

    def __init__(self, filename=None):
        super().__init__(filename)
        self._mergeDefConf()

    def isHideInTray(self):
        return self._conf["hide_in_tray"]

    def setHideInTray(self, value=_DEF_CONF["hide_in_tray"]):
        self._conf["hide_in_tray"] = value

    def isAskQuit(self):
        return self._conf["ask_hide_in_tray"]

    def setAskQuit(self, value=_DEF_CONF["ask_hide_in_tray"]):
        self._conf["ask_hide_in_tray"] = value

