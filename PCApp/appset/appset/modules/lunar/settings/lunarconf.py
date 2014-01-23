#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-12-02 15:43

"""

from abstract.commconfile import CommonConf


class LunarConf(CommonConf):
    # default config values
    _DEF_CONF = {
        "data_dir": "./data/",
        "data_file_name": "lunar.db",
    }

    # default config file
    _CONFIG_FILE_NAME = "./config/lunar.conf"

    def __init__(self, filename=None):
        super().__init__(filename)

