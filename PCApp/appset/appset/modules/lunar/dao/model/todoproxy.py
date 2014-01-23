#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-12-10 14:10

"""

from PySide.QtGui import *


class TodoProxy(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def filterAcceptsRow(self, sourceRow, sourceParent):
        index4 = self.sourceModel().index(sourceRow, 4, sourceParent)
        return True if not index4.data() else False
