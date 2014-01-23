#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-12-06 17:43

"""

from PySide.QtSql import *
from modules.lunar.dao.data import lawday
from modules.lunar.dao.data import holiday
from config import APP_VERSION


def init_data(db):
    query = QSqlQuery(db)

    for sql in lawday.sql_list:
        query.exec_(sql)

    for sql in holiday.sql_list:
        query.exec_(sql)

    sql = r"INSERT INTO Version (version) VALUES ('" + APP_VERSION + r"');"
    query.exec_(sql)

    query.finish()