#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-12 01:25
Abstract file config class. Can't be instanced.

>>> import os
>>> import tempfile
>>> filename = os.path.join(tempfile.gettempdir(), "config.ini")
>>> conf = ConfigFile(filename)
Traceback (most recent call last):
...
TypeError: Can't instantiate abstract class ConfigFile with abstract methods __init__
"""

import pickle
from abstract.config import *
from utils.createfile import *
from utils import log


class ConfigFile(Config):
    @abc.abstractmethod
    def __init__(self, filename):
        super().__init__()

        self._filename = filename
        if not os.path.exists(filename):
            create_file(filename)

    def loadConf(self):
        """
        @override
        Load persisted config values
        """
        with open(self._filename, 'rb') as f:
            try:
                conf = pickle.load(f)
            except EOFError as e:
                log.exception(e)
            else:
                self._conf = conf

            self._mergeDefConf()

    def saveConf(self):
        """
        @override
        Persisting current config values
        """
        with open(self._filename, 'wb') as f:
            pickle.dump(self._conf, f, pickle.HIGHEST_PROTOCOL)

    @abc.abstractmethod
    def _mergeDefConf(self):
        """
        Merge default config value to current config
        """
        pass

    def setConfItem(self, key, value):
        """
        Set config value
        @override
        @param key: config key
        @param value: config value
        """
        self._conf[key] = value

    def getConfItem(self, key):
        """
        Get config value, if key is not exist return None
        @override
        @param key: config key
        @return: config value
        """
        return self._conf[key]

    def contains(self, key):
        """
        Judge setting has key
        @param key: config key
        @return: bool
        """
        return key in self._conf.keys()


