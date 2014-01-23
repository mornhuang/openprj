#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-22 22:53

cx_Freeze setup file.
Use to create standalone executable file (special in window platform).
About how to use cx_Freeze, please refer to <a href="http://cx-freeze.sourceforge.net/" />
"""

import sys
from cx_Freeze import setup, Executable
from config import *

includeFiles = [
    (r"appset/appset.zh_CN.qm", ""),
    (r"C:\Python33\Lib\site-packages\PySide\plugins\sqldrivers\qsqlite4.dll", "sqldrivers/qsqlite4.dll")
]

options = {
    'build_exe': {
        'build_exe': 'dist/exe/',
        'optimize': '2',
        'include_files': includeFiles,
        'icon': 'appset/appmain/images/appset.ico',
    }
}

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('appset/appset.py', base=base)
]

setup(name='AppSet',
      version=APP_VERSION,
      description=DESCRIPTION,
      options=options,
      executables=executables
      )
