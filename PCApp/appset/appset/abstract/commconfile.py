#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-12-02 11:07


>>> import os
>>> import tempfile
>>> filename = os.path.join(tempfile.gettempdir(), "test.conf")
>>> commConf = CommonConf(filename)
>>> commConf.loadConf()

>>> commConf.setDataFile("g:/temp/test.dat")
>>> commConf.getDataFileName()
'test.dat'
>>> commConf.getDataDir()
'g:/temp/'
>>> commConf.getDataFile()
'g:/temp/test.dat'
>>> commConf.setDataDir("f:/temp")
>>> commConf.getDataDir()
'f:/temp/'
>>> commConf.setDataFileName('go.dat')
>>> commConf.getDataFileName()
'go.dat'
"""

from abstract.configfile import *


class CommonConf(ConfigFile):
    # default config values
    _DEF_CONF = {
        "data_dir": "./data/",
        "data_file_name": "common.db",
    }

    # default config file
    _CONFIG_FILE_NAME = "./config/common.conf"

    def __init__(self, filename=None):
        if filename is None:
            filename = self._CONFIG_FILE_NAME

        super().__init__(filename)
        self._mergeDefConf()

    def resetDefConf(self):
        """
        @override
        Reset all config items to default values
        """
        self._conf.update(self._DEF_CONF)

    def resetDefConfItem(self, key):
        """
        @override
        Reset some config item to default value
        """
        if key in self._DEF_CONF:
            self._conf[key] = self._DEF_CONF[key]

    def _mergeDefConf(self):
        """
        Merge default config value to current config
        """
        for key in (self._DEF_CONF.keys() - self._conf.keys()):
            self._conf[key] = self._DEF_CONF[key]

    def getDataDir(self):
        return self._conf["data_dir"]

    def setDataDir(self, value):
        if not value.endswith('/'):
            value += "/"

        self._conf["data_dir"] = value

    def getDataFileName(self):
        return self._conf["data_file_name"]

    def setDataFileName(self, value):
        self._conf["data_file_name"] = value

    def getDataFile(self):
        return self._conf["data_dir"] + self._conf["data_file_name"]

    def setDataFile(self, path):
        index = path.rfind('/')

        if not index:   # isn't a directory
            self._conf["data_file_name"] = path
        else:
            self._conf["data_dir"] = path[:index+1]
            self._conf["data_file_name"] = path[index+1:]

