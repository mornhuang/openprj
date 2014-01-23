#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-28 10:34


"""

from abstract.appqtmod import *
from modules.lunar.window.lunarwin import *
from modules.lunar.settings.lunarconf import LunarConf
from modules.lunar.lunar_rc import *


class LunarMod(AppQtMod):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__conf = LunarConf()
        self.__conf.loadConf()

        self.__lunar_win = LunarWin(self, self.__conf)

        grid_layout = QGridLayout(self)
        self.setLayout(grid_layout)

        grid_layout.setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.__lunar_win, 1, 1)

    def fini(self):
        self.__conf.saveConf()

    @staticmethod
    def getIcon():
        return QIcon(":/images/Calendar.png")

    @staticmethod
    def getShowName():
        return QObject().tr("Lunar")


