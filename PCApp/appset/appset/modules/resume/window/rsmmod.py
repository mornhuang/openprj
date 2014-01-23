#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-20 10:45
Resume modules entry route.
"""

from PySide.QtGui import *
from PySide.QtCore import *
from abstract.appqtmod import *
from modules.resume.window.record_ui import *
from modules.resume.settings.rsmconf import *
from modules.resume.model.rsmdao import *


class MODE:
    EDIT = "edit"
    ADD = "add"
    QUERY = "query"
    SENIOR_QUERY = "senior_query"


class PostRrdMod(AppQtMod, Ui_PostRrd):
    def __init__(self, parent=None):
        """
        Class initial method
        """
        super().__init__(parent)
        self.setupUi(self)

        # load config value
        self.__modConf = RsmConf()
        self.__modConf.loadConf()

        # initial model/view
        self.__dao = RsmDao(self.__modConf)

        self.postTableView.setModel(self.__dao.getModel())
        self.postTableView.hideColumn(0)
        self.postTableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.postTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.postTableView.setSortingEnabled(True)
        self.postTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.postTableView.horizontalHeader().setResizeMode(1, QHeaderView.Stretch)
        self.postTableView.sortByColumn(3, Qt.DescendingOrder)

        selectMode = self.postTableView.selectionModel()
        selectMode.currentRowChanged.connect(self.__currentRowChange)

        # set ui component
        self.__mode = MODE.QUERY
        self.__setUIByMode()

        # set default edit row
        self.__editRow = 0
        self.__editId = 0

        # adjust ui position
        self.officeLabel.setMinimumWidth(self.corpLabel.sizeHint().width())

    @Slot()
    def on_addBtn_clicked(self):
        self.__mode = MODE.ADD
        self.__setUIByMode()

        # reset initial data
        self.officeCbx.setCurrentIndex(0)
        self.dateEdit.setDate(QDate.currentDate())
        self.ivwCbx.setCurrentIndex(0)

        if len(self.corpLineEdit.text()):
            self.saveBtn.setEnabled(True)
        else:
            self.saveBtn.setEnabled(False)

    @Slot()
    def on_saveBtn_clicked(self):
        if self.__mode == MODE.ADD:
            if not len(self.corpLineEdit.text()):
                QMessageBox.critical(self, self.tr("Error"), self.tr("Corporation can't be empty!"))
                return
            if not len(self.officeCbx.currentText()):
                QMessageBox.critical(self, self.tr("Error"), self.tr("Office can't be empty!"))
                return
            self.__saveNewRecord()
            self.corpLineEdit.clear()
            self.ivwCbx.setCurrentIndex(0)
            #self.__mode = MODE.QUERY
            #self.__setUIByMode()
            self.__dao.filterCorp()

        elif self.__mode == MODE.EDIT:
            self.__updateRecord()
            self.saveBtn.setDisabled(True)
            self.resetBtn.setDisabled(True)

    @Slot()
    def on_cancelBtn_clicked(self):
        self.corpLineEdit.clear()
        self.__mode = MODE.QUERY
        self.__setUIByMode()
        self.__dao.filterCorp()

    @Slot()
    def on_resetBtn_clicked(self):
        self.__resetDataInEdit()

    @Slot()
    def on_delBtn_clicked(self):
        if self.__editId is None:
            return

        ret = QMessageBox.question(self, self.tr("Confirm"),
                                   self.tr("Are you sure delete this record?"),
                                   QMessageBox.Ok | QMessageBox.Cancel)
        if ret == QMessageBox.Ok:
            self.__dao.deleteRecord(self.__editId)

    @Slot()
    def on_corpLineEdit_textChanged(self):
        if MODE.QUERY == self.__mode:
            self.__dao.filterCorp(self.corpLineEdit.text())

        elif MODE.ADD == self.__mode:
            self.__dao.filterCorp(self.corpLineEdit.text())
            if len(self.corpLineEdit.text()):
                self.saveBtn.setEnabled(True)
            else:
                self.saveBtn.setEnabled(False)

        elif MODE.EDIT == self.__mode:
            self.__setBtnStatInEdit()

    @Slot()
    def on_officeCbx_editTextChanged(self):
        if MODE.EDIT == self.__mode:
            self.__setBtnStatInEdit()

    @Slot()
    def on_dateEdit_dateChanged(self):
        if MODE.EDIT == self.__mode:
            self.__setBtnStatInEdit()

    @Slot()
    def on_ivwCbx_currentIndexChanged(self):
        if MODE.EDIT == self.__mode:
            self.__setBtnStatInEdit()

    @Slot(QModelIndex)
    def on_postTableView_activated(self, index):
        self.__mode = MODE.EDIT
        self.__setUIByMode()
        self.__editRow = index.row()
        model = self.postTableView.model()
        self.__editId = model.data(model.index(self.__editRow, 0, QModelIndex()))
        self.__resetDataInEdit()

    @Slot(QModelIndex, QModelIndex)
    def __currentRowChange(self, current, old):
        if self.__mode == MODE.EDIT:
            self.__editRow = current.row()
            model = self.postTableView.model()
            self.__editId = model.data(model.index(self.__editRow, 0, QModelIndex()))
            self.__resetDataInEdit()

    def __setUIByMode(self):
        """
        Set how to show UI Component in different mode.
        """
        if self.__mode == MODE.QUERY:
            self.saveWidget.hide()
            self.addBtn.show()

        elif self.__mode == MODE.ADD:
            self.addBtn.hide()
            self.resetBtn.hide()
            self.delBtn.hide()
            self.saveWidget.show()
            self.corpLineEdit.setFocus()

        elif self.__mode == MODE.EDIT:
            self.addBtn.hide()
            self.resetBtn.show()
            self.delBtn.show()
            self.saveWidget.show()

    def __saveNewRecord(self):
        """
        Save new added record to database
        """
        corp = self.corpLineEdit.text()
        office = self.officeCbx.currentText()
        date = self.dateEdit.date()
        ivw = self.ivwCbx.currentText()

        self.__dao.saveRecord(corp, office, date, ivw)

    def __updateRecord(self):
        """
        Update changed record to database
        """
        corp = self.corpLineEdit.text()
        office = self.officeCbx.currentText()
        date = self.dateEdit.date()
        ivw = self.ivwCbx.currentText()

        self.__dao.updateRecord(self.__editId, corp, office, date, ivw)

    def __getRowRecord(self, row):
        """
        Get selected row data.
        """
        idIndex = self.postTableView.model().index(row, 0, QModelIndex())
        corpIndex = self.postTableView.model().index(row, 1, QModelIndex())
        officeIndex = self.postTableView.model().index(row, 2, QModelIndex())
        dateIndex = self.postTableView.model().index(row, 3, QModelIndex())
        ivwIndex = self.postTableView.model().index(row, 4, QModelIndex())

        idx = self.postTableView.model().data(idIndex)
        corp = self.postTableView.model().data(corpIndex)
        office = self.postTableView.model().data(officeIndex)
        date = QDate.fromString(self.postTableView.model().data(dateIndex), "yyyy-MM-dd")
        ivw = self.postTableView.model().data(ivwIndex)

        return idx, corp, office, date, ivw

    def __getEditRowRecord(self):
        """
        Get current edit row data.
        """
        return self.__getRowRecord(self.__editRow)

    def __resetDataInEdit(self):
        """
        Reset corporation/office/date data to current select row in edit mode.
        """
        record = self.__getEditRowRecord()

        self.corpLineEdit.setText(record[1])
        self.officeCbx.setEditText(record[2])
        self.dateEdit.setDate(record[3])
        idx = self.ivwCbx.findText(record[4])
        self.ivwCbx.setCurrentIndex(idx)

        self.saveBtn.setDisabled(True)
        self.resetBtn.setDisabled(True)

    def __setBtnStatInEdit(self):
        """
        Set save/reset button enable or disable when data changed in edit mode.
        """
        corp = self.corpLineEdit.text()
        office = self.officeCbx.currentText()
        date = self.dateEdit.date()
        ivw = self.ivwCbx.currentText()

        record = self.__getEditRowRecord()
        if corp == record[1] and office == record[2] and date == record[3] and ivw == record[4]:
            self.saveBtn.setDisabled(True)
            self.resetBtn.setDisabled(True)
        else:
            self.saveBtn.setEnabled(True)
            self.resetBtn.setEnabled(True)

    @staticmethod
    def getIcon():
        return QIcon(":/images/resume.png")

    @staticmethod
    def getShowName():
        return QObject().tr("Resume")

    def fini(self):
        self.__modConf.saveConf()


