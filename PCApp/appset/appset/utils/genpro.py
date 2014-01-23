#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-12-11 13:24

>>> gen_pro_file()
"""

import os
import re


def gen_pro_file():
    root_dir = os.path.realpath(os.path.dirname(__file__) + "../../")
    target_file = os.path.join(root_dir, "appset.pro")

    with open(target_file, "w") as f:
        f.write("SOURCES = \\" + "\n")

        for root, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if re.match(r'^[^_](?:(?!_rc).)*(\.py)$', filename):
                    f.write("\t")
                    str_out = root.replace(root_dir, "")
                    if str_out:
                        str_out += "/"
                    str_out += filename
                    str_out = str_out.replace('\\', "/").lstrip('/')
                    str_out += " \\\n"
                    f.write(str_out)

        f.write("\n\n")
        f.write("TRANSLATIONS = appset.zh_CN.ts")
