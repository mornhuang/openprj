#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-12-02 10:49

"""

import os
from PySide.QtSql import *
from utils import log
from modules.lunar.dao.table import lawday
from modules.lunar.dao.table import leaveday
from modules.lunar.dao.checkver import check_version


class DayType():
    SOLAR = 0
    LUNAR = 1
    WORK = 0
    LEAVE = 1
    INVALID = -1


class LunarDB:
    """
    Handle solar/lunar holiday.
    """
    def __init__(self, dbFile):

        # open database
        self.__db = LunarDB.openDB("lunar_db", dbFile, "QSQLITE",
                                   "localhost", -1, "HongRay", "Lunar")

        check_version(self.__db)

    @property
    def db(self):
        return self.__db

    @staticmethod
    def openDB(name, dbname, dbtype="QSQLITE", host="localhost",
               port=-1, username="", password=""):
        # open database
        db = QSqlDatabase.database(name)

        if not db.isValid():
            if dbtype == "QSQLITE":
                # ensure sqlite db file exist
                dbFile = os.path.realpath(dbname)
                dirName = os.path.dirname(dbFile)
                if not os.path.exists(dirName):
                    os.makedirs(dirName)
            db = QSqlDatabase.addDatabase(dbtype, name)
            db.setDatabaseName(dbname)
            db.setHostName(host)
            db.setPort(port)
            db.setUserName(username)
            db.setPassword(password)

            if not db.open():
                log.critical("Open Database Error: " + db.lastError().text())
                return None

        return db

    def saveRecord(self, tblName, valDic):
        """
        >>> import os, tempfile
        >>> conf_file = os.path.join(tempfile.gettempdir(), "lunar.conf")
        >>> conf = LunarConf(conf_file)
        >>> conf.setDataDir(tempfile.gettempdir())
        >>> db = LunarDB(conf)
        >>> db.initDB()
        True
        >>> val_dic = {"h_typal": 1, "h_month": 12, "h_day": 12, "h_name": "test"}
        >>> db.saveRecord("Holiday", val_dic)

        """
        query = QSqlQuery(self.__db)
        bind_val = []

        field_str = ""
        value_str = ""
        for key in valDic.keys():
            field_str += key
            value_str += ":" + key
            field_str += ", "
            value_str += ", "
            bind_val.append((":" + key, valDic[key]))
        field_str = field_str[:-2]
        value_str = value_str[:-2]

        query_str = "INSERT" + " INTO " + tblName
        query_str += " (" + field_str + ") " + "VALUES" + " (" + value_str + ")"

        query.prepare(query_str)
        for k, v in bind_val:
            query.bindValue(k, v)

        self.__db.transaction()
        if query.exec_():
            self.__db.commit()
        else:
            self.__db.rollback()
            log.debug("Query sql: " + query_str)
            log.error("Save Record Failed: " + query.lastError().text())

        query.finish()

    def updateRecord(self, tblName, valDic, condDic):
        """
        >>> import os, tempfile
        >>> conf_file = os.path.join(tempfile.gettempdir(), "lunar.conf")
        >>> conf = LunarConf(conf_file)
        >>> conf.setDataDir(tempfile.gettempdir())
        >>> db = LunarDB(conf)
        >>> db.initDB()
        True
        >>> val_dic = {"h_typal": 0, "h_month": 2, "h_day": 3, "h_name": "come"}
        >>> con_dic = {"id": 1}
        >>> db.updateRecord("Holiday", val_dic, con_dic)
        """
        query = QSqlQuery(self.__db)
        bind_val = []

        value_str = ""
        for key in valDic.keys():
            value_str += (key + " = :" + key + ", ")
            bind_val.append((":" + key, valDic[key]))
        value_str = value_str[:-2]

        cond_str = ""
        for key in condDic.keys():
            cond_str += (key + " = :" + key + ", ")
            bind_val.append((":" + key, condDic[key]))
        cond_str = cond_str[:-2]

        query_str = "UPDATE " + tblName + " SET "
        query_str += value_str
        if cond_str:
            query_str += (" WHERE " + cond_str)

        query.prepare(query_str)
        for k, v in bind_val:
            query.bindValue(k, v)

        self.__db.transaction()
        if query.exec_():
            self.__db.commit()
        else:
            self.__db.rollback()
            log.debug("Query sql: " + query_str)
            log.error("Update Record Failed: " + query.lastError().text())

        query.finish()

    #############################################
    # Wrapped Function
    #############################################
    def queryLawDay(self):
        return lawday.query_all(self.__db)

    def queryYearLeaveDay(self, year):
        return leaveday.query_year(self.__db, year)

    def saveLeaveDay(self, year, month, day, flag):
        leaveday.save(self.__db, year, month, day, flag)

    def updateLeaveDay(self, year, month, day, flag):
        leaveday.update(self.__db, year, month, day, flag)

    def delLeaveDay(self, year, month, day):
        leaveday.delete(self.__db, year, month, day)