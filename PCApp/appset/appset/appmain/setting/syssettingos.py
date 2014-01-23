#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-11 19:30
Save / Get system setting by operation system

>>> QCoreApplication.setOrganizationName("HongRay")
>>> QCoreApplication.setOrganizationDomain("hongray.com")
>>> QCoreApplication.setApplicationName("AppSet")
>>> settings = SysSettingOS()
>>> settings.setValue("test", 55)
>>> str(settings.value("test"))
'55'
"""

from PySide.QtCore import *


class SysSettingOS(QSettings):
    def __init__(self):
        super().__init__()


