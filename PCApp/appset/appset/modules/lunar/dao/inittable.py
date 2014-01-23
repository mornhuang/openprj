#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-12-06 16:19

"""
from PySide.QtSql import *
from utils import log


def create_tbl(db):
    q = QSqlQuery(db)

    sql = "CREATE TABLE IF NOT EXISTS Version (version VARCHAR(250))"
    if not q.exec_(sql):
        log.critical("Created Table Holiday Error: " + q.lastError().text())

    sql = "CREATE TABLE IF NOT EXISTS Holiday (                             \
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,       \
                h_typal INTEGER,                                            \
                h_month INTEGER,                                            \
                h_day INTEGER,                                              \
                h_name VARCHAR(250)                                         \
            )"
    if not q.exec_(sql):
        log.critical("Created Table Holiday Error: " + q.lastError().text())

    sql = "CREATE TABLE IF NOT EXISTS  LawHDay (                            \
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,       \
                l_typal INTEGER,                                            \
                l_month INTEGER,                                            \
                l_day INTEGER,                                              \
                l_name VARCHAR(10),                                         \
                l_hds INTEGER                                               \
            )"
    if not q.exec_(sql):
        log.critical("Created Table LawHDay Error: " + q.lastError().text())

    sql = "CREATE TABLE IF NOT EXISTS  LeaveDay (                           \
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,       \
                l_year INTEGER,                                             \
                l_month INTEGER,                                            \
                l_day INTEGER,                                              \
                l_flag INTEGER                                              \
          )"
    if not q.exec_(sql):
        log.critical("Created Table LeaveDay Error: " + q.lastError().text())

    sql = "CREATE TABLE IF NOT EXISTS  SolarTerm (                          \
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,       \
                l_year INTEGER,                                             \
                l_month INTEGER,                                            \
                l_day INTEGER,                                              \
                l_term VARCHAR(20)                                          \
          )"
    if not q.exec_(sql):
        log.critical("Created Table SolarTerm Error: " + q.lastError().text())

    sql = "CREATE TABLE IF NOT EXISTS  TodoList (                           \
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,       \
                priority INTEGER,                                           \
                content VARCHAR(250),                                       \
                create_date DATE,                                           \
                comp_date DATE                                              \
          )"
    if not q.exec_(sql):
        log.critical("Created Table TodoList Error: " + q.lastError().text())

    q.finish()




