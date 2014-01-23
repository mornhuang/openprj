#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-12 03:07

"""

import os


def create_file(path):
    """
    Deep create file.
    If file's directory is not exist, first create directory then create file.
    """
    if not os.path.exists(path):
        dirName = os.path.dirname(path)
        if dirName and not os.path.exists(dirName):
            os.makedirs(dirName)
        f = open(path, 'w')
        f.close()

