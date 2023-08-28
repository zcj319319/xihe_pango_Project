#!/usr/bin/env python 
# -*- coding: utf-8 -*-
'''
Time    : 2023/8/22 16:13
Author  : zhuchunjin
Email   : chunjin.zhu@taurentech.net
File    : xihe_pango_main.py
Software: PyCharm
'''
import sys
import traceback

from PyQt5 import QtWidgets

from script.load_ui_panel import load_xihepango_panel

if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        ex = load_xihepango_panel()
        ex.show()
        sys.exit(app.exec_())
    except Exception as e:
        traceback.print_exc()
        sys.exit(-1)
