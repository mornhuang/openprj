#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-29 17:52

"""

from PySide.QtGui import *
from PySide.QtCore import *
from modules.lunar.algorithm import *


class LunarCalNav(QFrame):
    def __init__(self, parent=None, date=QDate.currentDate()):
        super().__init__(parent)

        self.year = QSpinBox(self)
        self.l_month = QPushButton(self)
        self.month = QComboBox(self)
        self.r_month = QPushButton(self)
        self.today = QPushButton(self)

        self.setupUI(date)

        self.l_month.clicked.connect(self.setPreviousIndex)
        self.r_month.clicked.connect(self.setNextIndex)

    def setupUI(self, date):
        self.setMinimumHeight(50)
        style = "QFrame {" \
                "border-top-width: 2px;" \
                "border-style: solid;" \
                "border-color: rgb(93, 174, 255);" \
                "background: white;" \
                "}"
        self.setStyleSheet(style)

        self.year.setMinimumSize(QSize(80, 26))
        self.year.setSuffix("年")
        self.year.setMinimum(1900)
        self.year.setMaximum(2050)
        self.year.setProperty("value", date.year())

        self.l_month.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.l_month.setMinimumSize(QSize(24, 28))
        self.l_month.setMaximumSize(QSize(24, 16777215))
        self.l_month.setText("<")

        self.month.setMinimumSize(QSize(70, 26))
        self.month.addItems(["1月", "2月", "3月", "4月", "5月", "6月",
                             "7月", "8月", "9月", "10月", "11月", "12月"])
        self.month.setCurrentIndex(date.month() - 1)

        self.r_month.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.r_month.setMinimumSize(QSize(24, 28))
        self.r_month.setMaximumSize(QSize(24, 16777215))
        self.r_month.setText(">")

        self.today.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.today.setMinimumSize(QSize(40, 28))
        self.today.setMaximumSize(QSize(40, 16777215))
        self.today.setText("今天")

        layout1 = QHBoxLayout()
        layout1.setSpacing(0)
        layout1.addWidget(self.l_month)
        layout1.addWidget(self.month)
        layout1.addWidget(self.r_month)

        layout = QHBoxLayout(self)
        layout.addWidget(self.year)
        layout.addLayout(layout1)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addItem(spacerItem)
        layout.addWidget(self.today)

    @Slot()
    def setNextIndex(self):
        cur_idx = self.month.currentIndex()
        if cur_idx == self.month.count() - 1:
            self.month.setCurrentIndex(0)
            self.year.setValue(self.year.value() + 1)
        else:
            self.month.setCurrentIndex(cur_idx + 1)

    @Slot()
    def setPreviousIndex(self):
        cur_idx = self.month.currentIndex()
        if cur_idx == 0:
            self.month.setCurrentIndex(self.month.count() - 1)
            self.year.setValue(self.year.value() - 1)
        else:
            self.month.setCurrentIndex(cur_idx - 1)


