#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-12-06 16:38

"""
from PySide.QtSql import *
from utils import log


def save(db, typal, month, day, name, hds):
    query = QSqlQuery(db)

    query.prepare("INSERT INTO LawHDay (l_typal, l_month, l_day, l_name, l_hds) \
                   VALUES (:l_typal, :l_month, :l_day, :l_name, :l_hds)")
    query.bindValue(":l_typal", typal)
    query.bindValue(":l_month", month)
    query.bindValue(":l_day", day)
    query.bindValue(":l_name", name)
    query.bindValue(":l_hds", hds)

    db.transaction()
    if query.exec_():
        db.commit()
    else:
        db.rollback()
        log.error("Save LawHDay Record Failed: " + query.lastError().text())

    query.finish()


def query_all(db):
    query = QSqlQuery(db)
    query_str = "SELECT * FROM LawHDay"
    query.exec_(query_str)
    return query


def update_by_id(db, idx, typal, month, day, name, hds):
    query = QSqlQuery(db)

    query.prepare("UPDATE LawHDay                                               \
                   SET l_typal = :l_typal, l_month = :l_month, l_day = :l_day,  \
                       l_name = :l_name, l_hds = :l_hds                         \
                   WHERE id = :idx")
    query.bindValue(":idx", idx)
    query.bindValue(":l_typal", typal)
    query.bindValue(":l_month", month)
    query.bindValue(":l_day", day)
    query.bindValue(":l_name", name)
    query.bindValue(":l_hds", hds)

    db.transaction()
    if query.exec_():
        db.commit()
    else:
        db.rollback()
        log.error("Update LawHDay Record Failed: " + query.lastError().text())

    query.finish()


def del_by_id(db, idx):
    query = QSqlQuery(db)

    query.prepare("DELETE FROM LawHDay WHERE id = :idx")
    query.bindValue(":idx", idx)

    db.transaction()
    if query.exec_():
        db.commit()
    else:
        db.rollback()
        log.error("Delete LawHDay Record Failed: " + query.lastError().text())

    query.finish()