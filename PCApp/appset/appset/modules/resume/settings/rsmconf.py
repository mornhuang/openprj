#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-10 23:17

>>> import os
>>> import tempfile
>>> filename = os.path.join(tempfile.gettempdir(), "resume.conf")
>>> rsmConf = RsmConf(filename)
>>> rsmConf.loadConf()
>>> rsmConf.setDataFile("g:/temp/test.dat")
>>> rsmConf.getDataDir()
'g:/temp/'
>>> rsmConf.getDataFileName()
'test.dat'
>>> rsmConf.getDataFile()
'g:/temp/test.dat'
>>> rsmConf.setDataDir("f:/temp")
>>> rsmConf.getDataDir()
'f:/temp/'
"""

from abstract.commconfile import CommonConf


class RsmConf(CommonConf):
    # default config values
    _DEF_CONF = {
        "data_dir": "./data/",
        "data_file_name": "resume.db",
    }

    # default config file
    _CONFIG_FILE_NAME = "./config/resume.conf"

    def __init__(self, filename=None):
        super().__init__(filename)
        self._mergeDefConf()

