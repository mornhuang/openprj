#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-11 19:30
Save / Get system setting by file

>>> import os
>>> import tempfile
>>> filename = os.path.join(tempfile.gettempdir(), "setting.ini")
>>> settings = SysSettingFile(filename)
>>> settings.setValue("test", 13)
>>> str(settings.value("test"))
'13'
"""

from PySide.QtCore import *


class SysSettingFile(QSettings):
    def __init__(self, path):
        super().__init__(path, QSettings.IniFormat)

