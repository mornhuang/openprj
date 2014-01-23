#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-12 01:09
Abstract config class. Can't be instanced.

>>> config = Config()
Traceback (most recent call last):
...
TypeError: Can't instantiate abstract class Config with abstract methods __init__, loadConf, saveConf
"""

import abc


class Config(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        super().__init__()
        self._conf = {}

    @abc.abstractmethod
    def loadConf(self):
        """
        Load persisted config values
        """
        pass

    @abc.abstractmethod
    def saveConf(self):
        """
        Persisting current config values
        """
        pass

    @abc.abstractmethod
    def setConfItem(self, key, value):
        """
        Set config value
        @param key: config key
        @param value: config value
        """
        pass

    @abc.abstractmethod
    def getConfItem(self, key):
        """
        Get config value, if key is not exist return None
        @param key: config key
        @return: config value
        """
        pass

    @abc.abstractmethod
    def contains(self, key):
        """
        Judge setting has key
        @param key: config key
        @return: bool
        """
        pass

    @abc.abstractmethod
    def resetDefConf(self):
        """
        Reset all config items to default values
        """
        pass

    @abc.abstractmethod
    def resetDefConfItem(self, key):
        """
        Reset some config item to default value
        """
    pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
