#!/usr/bin/env python 
# -*- coding: utf-8 -*-
'''
Time    : 2022/11/23 10:35
Author  : zhuchunjin
Email   : chunjin.zhu@taurentech.net
File    : mem_read.py
Software: PyCharm
'''
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog

class Ui_Dialog1(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(334, 145)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(30, 30, 280, 25))
        self.comboBox.setObjectName("comboBox")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(110, 90, 120, 25))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "select sheet"))
        self.pushButton.setText(_translate("Dialog", "OK"))

class MainDialog1(QDialog):
    Signal_parp = pyqtSignal(str)
    def __init__(self, sheet_lst):
        super(MainDialog1, self).__init__()
        self.ui = Ui_Dialog1()
        self.ui.setupUi(self)
        self.sheet_lst = sheet_lst
        self.ui.comboBox.addItem('select one sheet')
        for x in sheet_lst:
            self.ui.comboBox.addItem(x)
        self.ui.comboBox.currentIndexChanged.connect(self.select_sheet)
        self.ui.pushButton.clicked.connect(self.ok_and_quit)

    def select_sheet(self):
        self.select_sheet = self.ui.comboBox.currentText()
        self.Signal_parp.emit(self.select_sheet)

    def ok_and_quit(self):
        self.close()