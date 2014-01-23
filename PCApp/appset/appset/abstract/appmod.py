#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-20 10:48

Abstract global module interface.
All application modules must be inherit from this class.
"""

import abc


class AppMod(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def init(self):
        """
        Module initial operation.
        """
        return True

    @abc.abstractmethod
    def fini(self):
        """
        Module finish operation.
        """
        return True

    @staticmethod
    @abc.abstractmethod
    def getIcon():
        """
        Return module's display icon.
        """
        return None

    @staticmethod
    @abc.abstractmethod
    def getShowName():
        """
        Return module's display name.
        """
        return ""


if __name__ == "__main__":
    import doctest

    doctest.testmod()
