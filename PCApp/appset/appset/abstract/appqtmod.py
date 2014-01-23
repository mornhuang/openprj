#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-20 14:51

Abstract global module interface.
Inherit from AppMod, QWidget, so subclass has widget function.

>>> mod = AppQtMod()
"""

from abstract.appmod import *
from PySide.QtGui import *
from utils.noconflict import classmaker


class AppQtMod(AppMod, QWidget, metaclass=classmaker()):
    @abc.abstractmethod
    def __init__(self, parent):
        AppMod.__init__(self)
        QWidget.__init__(self, parent)

    @abc.abstractmethod
    def addToolBar(self):
        pass

    @abc.abstractmethod
    def removeToolBar(self):
        pass

    @abc.abstractmethod
    def addMenu(self):
        pass

    @abc.abstractmethod
    def removeMenu(self):
        pass

if __name__ == "__main__":
    import doctest

    doctest.testmod()
