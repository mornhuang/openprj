#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-20 20:58

>>> import os
>>> import tempfile
>>> filename = os.path.join(tempfile.gettempdir(), "resume.conf")
>>> conf = RsmConf(filename)
>>> conf.setDataDir(tempfile.gettempdir())
>>> dao = RsmDao(conf)
>>> dao.saveRecord("test", "test", "1992-10-1", "No")
"""

import os
from modules.resume.settings.rsmconf import *
from PySide.QtSql import *
from PySide.QtCore import *
from PySide.QtGui import *
from utils import log


class RsmDao(QObject):
    def __init__(self, conf, parent=None):
        # check parameter
        if not isinstance(conf, RsmConf):
            log.error("Type error, need RsmConf, real " + type(conf))
            raise TypeError("Arg conf has wrong type! ")

        # call super init
        super().__init__(parent)

        # define object's field
        self.__db = None
        self.__dataModel = None
        self.__proxyModel = None

        # init db
        self.__initDB(conf)

        # create model
        self.__createModel()

        # load data
        self.__fetchAllData()

    def __initDB(self, conf):
        """
        Initialize database. Create tables when first run.
        """
        dbFile = os.path.realpath(conf.getDataFile())
        dirName = os.path.dirname(dbFile)
        if not os.path.exists(dirName):
            os.makedirs(dirName)

        # open database
        self.__db = QSqlDatabase.database("resume_db")

        if not self.__db.isValid():
            self.__db = QSqlDatabase.addDatabase("QSQLITE", "resume_db")
            self.__db.setDatabaseName(dbFile)
            self.__db.setHostName("localhost")
            self.__db.setPort(-1)
            self.__db.setUserName("HongRay")
            self.__db.setPassword("Resume")

        if not self.__db.open():
            log.error(self.__db.lastError().text())

        # create table if not exist
        if not self.__isTableExist("PostRrd"):
            self.__createTable()

    def __createTable(self):
        q = QSqlQuery("", self.__db)
        sql = "CREATE TABLE PostRrd (                                           \
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,       \
                    Corporation VARCHAR(250) NOT NULL,                          \
                    Office VARCHAR(50) NOT NULL,                                \
                    PostDate DATE NOT NULL,                                     \
                    Interview VARCHAR(8) NOT NULL                               \
                )"

        q.exec_(sql)

    def __createModel(self):
        queryModel = QSqlQueryModel()

        sortFilterModel = QSortFilterProxyModel()
        sortFilterModel.setDynamicSortFilter(True)
        sortFilterModel.setSourceModel(queryModel)
        sortFilterModel.setSortCaseSensitivity(Qt.CaseInsensitive)

        self.__dataModel = queryModel
        self.__proxyModel = sortFilterModel

    def getDB(self):
        return self.__db

    def getModel(self):
        return self.__proxyModel

    def __isTableExist(self, tblName):
        """
        Check table has existed in database.
        @arg tblName: checked table
        @return bool: True if exist else False
        """
        if tblName in self.__db.tables():
            return True
        else:
            return False

    def __fetchAllData(self):
        self.__dataModel.setQuery("SELECT * FROM PostRrd", self.__db)
        self.__dataModel.setHeaderData(0, Qt.Horizontal, self.tr("Id"))
        self.__dataModel.setHeaderData(1, Qt.Horizontal, self.tr("Corporation"))
        self.__dataModel.setHeaderData(2, Qt.Horizontal, self.tr("Office"))
        self.__dataModel.setHeaderData(3, Qt.Horizontal, self.tr("Post Date"))
        self.__dataModel.setHeaderData(4, Qt.Horizontal, self.tr("Interview"))

    def filterCorp(self, text=""):
        """
        Filter data according corporation text
        """
        self.__proxyModel.setFilterKeyColumn(1)
        regExp = QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString)
        self.__proxyModel.setFilterRegExp(regExp)

    def saveRecord(self, corp, office, date, ivw):
        query = self.__dataModel.query()
        query.prepare("INSERT INTO PostRrd (Corporation, Office, PostDate, Interview) \
                                    VALUES (:crop, :office, :pdate, :ivw)")
        query.bindValue(":crop", corp)
        query.bindValue(":office", office)
        query.bindValue(":pdate", date)
        query.bindValue(":ivw", ivw)

        self.__db.transaction()
        if query.exec_():
            self.__db.commit()
        else:
            self.__db.rollback()
            log.error(self.__db.lastError().text())

        # reload data
        self.__fetchAllData()

    def updateRecord(self, idx, corp, office, date, ivw):
        query = self.__dataModel.query()
        query.prepare("UPDATE PostRrd \
                        SET Corporation = :crop, Office = :office, PostDate = :postdate, Interview = :ivw \
                        WHERE id = :id")
        query.bindValue(":id", idx)
        query.bindValue(":crop", corp)
        query.bindValue(":office", office)
        query.bindValue(":postdate", date)
        query.bindValue(":ivw", ivw)

        self.__db.transaction()
        if query.exec_():
            self.__db.commit()
        else:
            self.__db.rollback()
            log.error(self.__db.lastError().text())

        # reload data
        self.__fetchAllData()

    def deleteRecord(self, idx):
        query = self.__dataModel.query()
        query.prepare("DELETE FROM PostRrd WHERE id = :id")
        query.bindValue(":id", idx)

        self.__db.transaction()
        if query.exec_():
            self.__db.commit()
        else:
            self.__db.rollback()
            log.error(self.__db.lastError().text())

        # reload data
        self.__fetchAllData()


