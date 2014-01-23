#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-29 17:48

"""

from PySide.QtGui import *
from modules.lunar.window.lunartiptoday import TipToday
from modules.lunar.window.lunartipflag import TipFlag


class LunarTip(QFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.tipToday = TipToday(self, db)
        self.tipFlag = TipFlag(self, db)
        self.setupUI()

    def setupUI(self):
        self.setObjectName("tip")
        self.setMinimumHeight(120)

        style = "QFrame#tip {" \
                "border-bottom-width: 2px;" \
                "border-top-width: 1px;" \
                "border-style: solid;" \
                "border-color: rgb(93, 174, 255); }"
        self.setStyleSheet(style)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        layout.addWidget(self.tipToday)
        layout.addWidget(self.tipFlag)
        self.setLayout(layout)

    def updateDay(self, date):
        self.tipToday.refresh(date)