#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-12-06 16:36

"""
from PySide.QtSql import *
from utils import log


def save(db, year, month, day, term):
    query = QSqlQuery(db)

    query.prepare("INSERT INTO SolarTerm (l_year, l_month, l_day, l_term) \
                   VALUES (:l_year, :l_month, :l_day, :l_term)")
    query.bindValue(":l_year", year)
    query.bindValue(":l_month", month)
    query.bindValue(":l_day", day)
    query.bindValue(":l_term", term)

    db.transaction()
    if query.exec_():
        db.commit()
    else:
        db.rollback()
        log.error("Save SolarTerm Record Failed: " + query.lastError().text())

    query.finish()


def update(db, year, month, day, term):
    query = QSqlQuery(db)

    query.prepare("UPDATE SolarTerm                     \
                   SET l_term = :l_term                 \
                   WHERE l_year = :l_year AND l_month = :l_month AND l_day = :l_day")
    query.bindValue(":l_year", year)
    query.bindValue(":l_month", month)
    query.bindValue(":l_day", day)
    query.bindValue(":l_term", term)

    db.transaction()
    if query.exec_():
        db.commit()
    else:
        db.rollback()
        log.error("Update SolarTerm Record Failed: " + query.lastError().text())

    query.finish()


def del_by_id(db, idx):
    query = QSqlQuery(db)

    query.prepare("DELETE FROM SolarTerm WHERE id = :idx")
    query.bindValue(":idx", idx)

    db.transaction()
    if query.exec_():
        db.commit()
    else:
        db.rollback()
        log.error("Delete SolarTerm Record Failed: " + query.lastError().text())

    query.finish()