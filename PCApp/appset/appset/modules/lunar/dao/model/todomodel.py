#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-12-07 20:20

>>> import os
>>> import tempfile
>>> from modules.lunar.dao.lunardb import LunarDB
>>> dbfile = os.path.join(tempfile.gettempdir(), "lunar.db")
>>> sqlModel = TodoSqlModel(None, LunarDB(dbfile).db)
>>> sqlModel.newTodo(4, "test")

"""

from PySide.QtSql import *
from PySide.QtCore import *
from utils import log


class TodoSqlModel(QSqlQueryModel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.refresh()

    def flags(self, index):
        flags = super().flags(index)
        if index.column() == 1 or index.column() == 2:
            flags |= Qt.ItemIsEditable
        return flags

    def setData(self, index, value, role):
        if index.column() < 1 or index.column() > 2:
            return False

        if index.column() == 1 and not value:   # content is empty
            return False

        primaryKeyIndex = super().index(index.row(), 0)
        idx = self.data(primaryKeyIndex)

        self.clear()

        if index.column() == 2:             # priority
            ok = self.setPriority(idx, value)
        elif index.column() == 1:
            value = value[:249] if len(value) >= 250 else value
            ok = self.setContent(idx, value)

        self.refresh()

        return ok

    def refresh(self):
        self.setQuery("SELECT id, content, priority, create_date, comp_date \
                       FROM TodoList                                        \
                       ORDER BY priority, create_date",
                      self.db)

    def setPriority(self, idx, priority):
        query = QSqlQuery(self.db)
        query.prepare("update TodoList set priority = ? where id = ?")
        query.addBindValue(priority)
        query.addBindValue(idx)
        ok = query.exec_()
        query.finish()

        if not ok:
            log.error("Update TodoList Priority Failed: " + query.lastError().text())
        return ok

    def setContent(self, idx, content):
        query = QSqlQuery(self.db)
        query.prepare("update TodoList set content = ? where id = ?")
        query.addBindValue(content)
        query.addBindValue(idx)
        ok = query.exec_()
        query.finish()

        if not ok:
            log.error("Update TodoList Content Failed: " + query.lastError().text())
        return ok

    def newTodo(self, priority, content):
        self.clear()
        query = QSqlQuery(self.db)

        query.prepare("INSERT INTO TodoList (priority, content, create_date) \
                                    VALUES (?, ?, ?)")
        query.addBindValue(priority)
        query.addBindValue(content)
        query.addBindValue(QDate.currentDate())

        if not query.exec_():
            log.error("Save TodoList Record Failed: " + query.lastError().text())

        query.finish()
        self.refresh()

    def delTodo(self, idxList):
        self.clear()
        query = QSqlQuery(self.db)

        for idx in idxList:
            query.prepare("DELETE FROM TodoList WHERE id = ?")
            query.addBindValue(idx)

            if not query.exec_():
                log.error("Delete TodoList Record Failed: " + query.lastError().text())

        query.finish()
        self.refresh()

    def completeTodo(self, idxList):
        self.clear()
        query = QSqlQuery(self.db)

        for idx in idxList:
            query.prepare("update TodoList set comp_date = ? where id = ?")
            query.addBindValue(QDate.currentDate())
            query.addBindValue(idx)

            if not query.exec_():
                log.error("Delete TodoList Record Failed: " + query.lastError().text())

        query.finish()
        self.refresh()