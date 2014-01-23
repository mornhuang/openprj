#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-12-06 16:25

"""

from PySide.QtSql import *
from utils import log


def save(db, typal, month, day, name):
    query = QSqlQuery(db)

    query.prepare("INSERT INTO Holiday (h_typal, h_month, h_day, h_name) \
                                VALUES (:typal, :month, :day, :name)")
    query.bindValue(":typal", typal)
    query.bindValue(":month", month)
    query.bindValue(":day", day)
    query.bindValue(":name", name)

    db.transaction()
    if query.exec_():
        db.commit()
    else:
        db.rollback()
        log.error("Save Holiday Record Failed: " + query.lastError().text())

    query.finish()


def update(db, idx, typal, month, day, name):
    query = QSqlQuery(db)

    query.prepare("UPDATE Holiday \
                   SET h_typal = :typal, h_month = :month, h_day = :day, h_name = :name \
                   WHERE id = :idx")
    query.bindValue(":idx", idx)
    query.bindValue(":typal", typal)
    query.bindValue(":month", month)
    query.bindValue(":day", day)
    query.bindValue(":name", name)

    db.transaction()
    if query.exec_():
        db.commit()
    else:
        db.rollback()
        log.error("Update Holiday Record Failed: " + query.lastError().text())
    query.finish()


def del_by_id(db, idx):
    query = QSqlQuery(db)

    query.prepare("DELETE FROM Holiday WHERE id = :idx")
    query.bindValue(":idx", idx)

    db.transaction()
    if query.exec_():
        db.commit()
    else:
        db.rollback()
        log.error("Delete Holiday Record Failed: " + query.lastError().text())

    query.finish()


def query_data(db, typal, month, day):
    query = QSqlQuery(db)
    query.prepare("SELECT h_name FROM Holiday where h_typal = ? and h_month = ? and h_day = ?")
    query.addBindValue(typal)
    query.addBindValue(month)
    query.addBindValue(day)
    if not query.exec_():
        log.error("Query Holiday Record Failed: " + query.lastError().text())

    return query
