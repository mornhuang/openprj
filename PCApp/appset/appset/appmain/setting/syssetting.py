#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-11 19:41
system setting class

>>> s = consttype.SysSetting
>>> s.setValue("test", 13)
>>> str(s.value("test"))
'13'
>>> import os
>>> import tempfile
>>> filename = os.path.join(tempfile.gettempdir(), "setting")
>>> s = SysSettingFile(filename)
>>> s.setValue("test", 13)
>>> str(s.value("test"))
'13'
"""

from appmain.setting.syssettingfile import *
from appmain.setting.syssettingos import *
from utils import consttype
from config import *

# Set global setting
QCoreApplication.setOrganizationName(ORG_NAME)
QCoreApplication.setOrganizationDomain(ORG_DOMAIN)
QCoreApplication.setApplicationName(APP_NAME)
QCoreApplication.setApplicationVersion(APP_VERSION)

consttype.SysSetting = SysSettingOS()


