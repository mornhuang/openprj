#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-12-11 13:58

"""

from PySide.QtGui import *


class TipFlag(QWidget):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.setupUI()

    def setupUI(self):
        self.setMinimumWidth(100)