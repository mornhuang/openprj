#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-12-11 13:42

"""

from PySide.QtGui import *
from PySide.QtCore import *
from modules.lunar.dao.table.holiday import *


class TipToday(QWidget):
    def __init__(self, parent, ldb):
        super().__init__(parent)
        self.editor = QPlainTextEdit(self)
        self.db = ldb.db
        self.setupUI()
        self.refresh()

    def setupUI(self):
        self.editor.setEnabled(False)
        self.editor.setFrameShape(QFrame.NoFrame)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.editor)
        self.setLayout(layout)

    def refresh(self, date=QDate.currentDate()):
        month = date.month()
        day = date.day()
        query = query_data(self.db, 0, month, day)
        self.editor.clear()
        while query.next():
            self.editor.appendPlainText(query.value(0))

