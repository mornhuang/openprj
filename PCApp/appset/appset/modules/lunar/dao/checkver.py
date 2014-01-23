#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-12-08 14:28

"""

from PySide.QtSql import *
from utils.version import Version, VersionMatch
from config import APP_VERSION
from modules.lunar.dao.inittable import *
from modules.lunar.dao.initdata import *


def check_version(db):
    old_ver = get_version(db)

    match = VersionMatch('> 0')
    if not match.test(old_ver):                 # first run, has not created table.
        create_tbl(db)
        init_data(db)
        old_ver = APP_VERSION

    match = VersionMatch('< ' + APP_VERSION)
    if match.test(old_ver):                     # less than current version, update version.
        set_version(db, APP_VERSION)


def get_version(db):
    if "Version" not in db.tables():
        return Version("0.0.0")

    query = QSqlQuery("Select * from Version", db)
    query.exec_()
    query.next()
    ver = query.value(0)
    query.finish()

    return Version(ver)


def set_version(db, version):
    query = QSqlQuery("update Version set version = ?", db)
    query.addBindValue(version)
    query.exec_()
    query.finish()
