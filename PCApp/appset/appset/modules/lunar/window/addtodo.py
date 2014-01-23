#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-12-10 17:01

"""

from PySide.QtGui import *
from modules.lunar.window.addtodo_ui import Ui_Dialog


class AddTodoDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
