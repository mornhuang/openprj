#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-12-06 16:34

"""
from PySide.QtSql import *
from utils import log


def save(db, year, month, day, flag):
    query = QSqlQuery(db)

    query.prepare("INSERT INTO LeaveDay (l_year, l_month, l_day, l_flag) \
                   VALUES (:l_year, :l_month, :l_day, :l_flag)")
    query.bindValue(":l_year", year)
    query.bindValue(":l_month", month)
    query.bindValue(":l_day", day)
    query.bindValue(":l_flag", flag)

    db.transaction()
    if query.exec_():
        db.commit()
    else:
        db.rollback()
        log.error("Save LeaveDay Record Failed: " + query.lastError().text())

    query.finish()


def query_year(db, year):
    query = QSqlQuery(db)
    query.prepare("SELECT l_month, l_day, l_flag FROM LeaveDay WHERE l_year = :l_year")
    query.bindValue(":l_year", year)
    query.exec_()
    return query


def update_by_id(db, idx, year, month, day, flag):
    query = QSqlQuery(db)

    query.prepare("UPDATE LeaveDay \
                   SET l_year = :l_year, l_month = :l_month, l_day = :l_day, l_flag = :l_flag  \
                   WHERE id = :idx")
    query.bindValue(":idx", idx)
    query.bindValue(":l_year", year)
    query.bindValue(":l_month", month)
    query.bindValue(":l_day", day)
    query.bindValue(":l_flag", flag)

    db.transaction()
    if query.exec_():
        db.commit()
    else:
        db.rollback()
        log.error("Update LeaveDay Record Failed: " + query.lastError().text())

    query.finish()


def update(db, year, month, day, flag):
    query = QSqlQuery(db)

    query.prepare("UPDATE LeaveDay \
                   SET l_flag = :l_flag  \
                   WHERE l_year = :l_year AND l_month = :l_month AND l_day = :l_day")
    query.bindValue(":l_year", year)
    query.bindValue(":l_month", month)
    query.bindValue(":l_day", day)
    query.bindValue(":l_flag", flag)

    db.transaction()
    if query.exec_():
        db.commit()
    else:
        db.rollback()
        log.error("Update LeaveDay Record Failed: " + query.lastError().text())

    query.finish()


def delete(db, year, month, day):
    query = QSqlQuery(db)

    query.prepare("DELETE FROM LeaveDay \
                   WHERE l_year = :l_year AND l_month = :l_month AND l_day = :l_day")
    query.bindValue(":l_year", year)
    query.bindValue(":l_month", month)
    query.bindValue(":l_day", day)

    db.transaction()
    if query.exec_():
        db.commit()
    else:
        db.rollback()
        log.error("Delete LeaveDay Record Failed: " + query.lastError().text())

    query.finish()


def del_by_id(db, idx):
    query = QSqlQuery(db)

    query.prepare("DELETE FROM LeaveDay WHERE id = :idx")
    query.bindValue(":idx", idx)

    db.transaction()
    if query.exec_():
        db.commit()
    else:
        db.rollback()
        log.error("Delete LeaveDay Record Failed: " + query.lastError().text())

    query.finish()
