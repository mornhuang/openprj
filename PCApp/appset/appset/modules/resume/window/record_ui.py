# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'record.ui'
#
# Created: Wed Dec 11 19:57:04 2013
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_PostRrd(object):
    def setupUi(self, PostRrd):
        PostRrd.setObjectName("PostRrd")
        PostRrd.resize(805, 478)
        PostRrd.setMinimumSize(QtCore.QSize(72, 0))
        self.gridLayout_2 = QtGui.QGridLayout(PostRrd)
        self.gridLayout_2.setContentsMargins(6, 6, 6, 2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.corpLabel = QtGui.QLabel(PostRrd)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.corpLabel.sizePolicy().hasHeightForWidth())
        self.corpLabel.setSizePolicy(sizePolicy)
        self.corpLabel.setMinimumSize(QtCore.QSize(0, 0))
        self.corpLabel.setObjectName("corpLabel")
        self.horizontalLayout.addWidget(self.corpLabel)
        self.corpLineEdit = LineEdit(PostRrd)
        self.corpLineEdit.setObjectName("corpLineEdit")
        self.horizontalLayout.addWidget(self.corpLineEdit)
        self.addBtn = QtGui.QPushButton(PostRrd)
        self.addBtn.setObjectName("addBtn")
        self.horizontalLayout.addWidget(self.addBtn)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.saveWidget = QtGui.QWidget(PostRrd)
        self.saveWidget.setObjectName("saveWidget")
        self.gridLayout = QtGui.QGridLayout(self.saveWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.saveBtn = QtGui.QPushButton(self.saveWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveBtn.sizePolicy().hasHeightForWidth())
        self.saveBtn.setSizePolicy(sizePolicy)
        self.saveBtn.setObjectName("saveBtn")
        self.gridLayout.addWidget(self.saveBtn, 0, 7, 1, 1)
        self.delBtn = QtGui.QPushButton(self.saveWidget)
        self.delBtn.setObjectName("delBtn")
        self.gridLayout.addWidget(self.delBtn, 0, 10, 1, 1)
        self.dateLabel = QtGui.QLabel(self.saveWidget)
        self.dateLabel.setObjectName("dateLabel")
        self.gridLayout.addWidget(self.dateLabel, 0, 2, 1, 1)
        self.officeLabel = QtGui.QLabel(self.saveWidget)
        self.officeLabel.setMinimumSize(QtCore.QSize(72, 0))
        self.officeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.officeLabel.setObjectName("officeLabel")
        self.gridLayout.addWidget(self.officeLabel, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 6, 1, 1)
        self.cancelBtn = QtGui.QPushButton(self.saveWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelBtn.sizePolicy().hasHeightForWidth())
        self.cancelBtn.setSizePolicy(sizePolicy)
        self.cancelBtn.setObjectName("cancelBtn")
        self.gridLayout.addWidget(self.cancelBtn, 0, 8, 1, 1)
        self.dateEdit = QtGui.QDateTimeEdit(self.saveWidget)
        self.dateEdit.setDisplayFormat("yyyy-M-d")
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName("dateEdit")
        self.gridLayout.addWidget(self.dateEdit, 0, 3, 1, 1)
        self.ivwCbx = QtGui.QComboBox(self.saveWidget)
        self.ivwCbx.setObjectName("ivwCbx")
        self.ivwCbx.addItem("")
        self.ivwCbx.addItem("")
        self.gridLayout.addWidget(self.ivwCbx, 0, 5, 1, 1)
        self.resetBtn = QtGui.QPushButton(self.saveWidget)
        self.resetBtn.setObjectName("resetBtn")
        self.gridLayout.addWidget(self.resetBtn, 0, 9, 1, 1)
        self.ivwLabel = QtGui.QLabel(self.saveWidget)
        self.ivwLabel.setObjectName("ivwLabel")
        self.gridLayout.addWidget(self.ivwLabel, 0, 4, 1, 1)
        self.officeCbx = QtGui.QComboBox(self.saveWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.officeCbx.sizePolicy().hasHeightForWidth())
        self.officeCbx.setSizePolicy(sizePolicy)
        self.officeCbx.setMinimumSize(QtCore.QSize(0, 0))
        self.officeCbx.setEditable(True)
        self.officeCbx.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.officeCbx.setMinimumContentsLength(14)
        self.officeCbx.setObjectName("officeCbx")
        self.officeCbx.addItem("")
        self.officeCbx.addItem("")
        self.officeCbx.addItem("")
        self.gridLayout.addWidget(self.officeCbx, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.saveWidget, 1, 0, 1, 1)
        self.postTableView = QtGui.QTableView(PostRrd)
        self.postTableView.setMinimumSize(QtCore.QSize(685, 0))
        self.postTableView.setObjectName("postTableView")
        self.gridLayout_2.addWidget(self.postTableView, 2, 0, 1, 1)

        self.retranslateUi(PostRrd)
        QtCore.QMetaObject.connectSlotsByName(PostRrd)

    def retranslateUi(self, PostRrd):
        PostRrd.setWindowTitle(QtGui.QApplication.translate("PostRrd", "Resume Manage", None, QtGui.QApplication.UnicodeUTF8))
        self.corpLabel.setText(QtGui.QApplication.translate("PostRrd", "Corporation:", None, QtGui.QApplication.UnicodeUTF8))
        self.addBtn.setText(QtGui.QApplication.translate("PostRrd", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.saveBtn.setText(QtGui.QApplication.translate("PostRrd", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.delBtn.setText(QtGui.QApplication.translate("PostRrd", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.dateLabel.setText(QtGui.QApplication.translate("PostRrd", "Date:", None, QtGui.QApplication.UnicodeUTF8))
        self.officeLabel.setText(QtGui.QApplication.translate("PostRrd", "Office:", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelBtn.setText(QtGui.QApplication.translate("PostRrd", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.ivwCbx.setItemText(0, QtGui.QApplication.translate("PostRrd", "No", None, QtGui.QApplication.UnicodeUTF8))
        self.ivwCbx.setItemText(1, QtGui.QApplication.translate("PostRrd", "Yes", None, QtGui.QApplication.UnicodeUTF8))
        self.resetBtn.setText(QtGui.QApplication.translate("PostRrd", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.ivwLabel.setText(QtGui.QApplication.translate("PostRrd", "Interview:", None, QtGui.QApplication.UnicodeUTF8))
        self.officeCbx.setItemText(0, QtGui.QApplication.translate("PostRrd", "Project Director", None, QtGui.QApplication.UnicodeUTF8))
        self.officeCbx.setItemText(1, QtGui.QApplication.translate("PostRrd", "Project Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.officeCbx.setItemText(2, QtGui.QApplication.translate("PostRrd", "Senior Developer", None, QtGui.QApplication.UnicodeUTF8))

from modules.resume.window.lineedit import LineEdit
