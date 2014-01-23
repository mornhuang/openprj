# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addtodo.ui'
#
# Created: Tue Dec 10 16:58:48 2013
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(401, 292)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(50, 260, 341, 21))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.layoutWidget = QtGui.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 9, 381, 231))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QtGui.QFormLayout(self.layoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.content = QtGui.QPlainTextEdit(self.layoutWidget)
        self.content.setObjectName("content")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.content)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.priority = QtGui.QComboBox(self.layoutWidget)
        self.priority.setObjectName("priority")
        self.priority.addItem("")
        self.priority.addItem("")
        self.priority.addItem("")
        self.priority.addItem("")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.priority)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "添加待办任务", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "内容", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "优先级", None, QtGui.QApplication.UnicodeUTF8))
        self.priority.setItemText(0, QtGui.QApplication.translate("Dialog", "紧急重要", None, QtGui.QApplication.UnicodeUTF8))
        self.priority.setItemText(1, QtGui.QApplication.translate("Dialog", "紧急不重要", None, QtGui.QApplication.UnicodeUTF8))
        self.priority.setItemText(2, QtGui.QApplication.translate("Dialog", "重要不紧急", None, QtGui.QApplication.UnicodeUTF8))
        self.priority.setItemText(3, QtGui.QApplication.translate("Dialog", "不重要不紧急", None, QtGui.QApplication.UnicodeUTF8))

