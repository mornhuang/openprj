#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-29 17:41

"""

from PySide.QtGui import *
from PySide.QtCore import *
from modules.lunar.dao.lunardb import LunarDB
from modules.lunar.dao.model.todomodel import TodoSqlModel
from modules.lunar.dao.model.todoproxy import TodoProxy
from modules.lunar.window.tododelegate import TodoDelegate, PRIORITY_TIP
from modules.lunar.window.addtodo import AddTodoDialog


class LunarInfo(QFrame):
    def __init__(self, parent, dbc):
        super().__init__(parent)
        self.model = TodoSqlModel(self, dbc.db)
        self.proxy = TodoProxy()
        self.proxy.setSourceModel(self.model)
        self.slctModel = None
        self.setupUI()

    def setupUI(self):
        self.setMinimumWidth(250)
        self.setObjectName("info")

        layout = QGridLayout()
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(1)

        todoTitle = QLabel("任务列表")
        todoTitle.setObjectName("title")
        todoTitle.setMinimumHeight(28)
        todoTitle.setAlignment(Qt.AlignCenter)
        style = "font-family: 'arial'; font-style: bold; font-size: 15px;"
        todoTitle.setStyleSheet(style)
        layout.addWidget(todoTitle)

        line = QFrame()
        style = "color: red"
        line.setStyleSheet(style)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Raised)
        layout.addWidget(line)

        todoView = QTableView()
        todoView.setObjectName("view")
        todoView.setModel(self.proxy)
        todoView.setItemDelegate(TodoDelegate())
        todoView.setFrameShape(QFrame.NoFrame)
        todoView.setMouseTracking(True)
        todoView.entered.connect(self.showToolTip)
        todoView.hideColumn(0)
        todoView.hideColumn(3)
        todoView.hideColumn(4)
        todoView.setShowGrid(False)
        todoView.setWordWrap(True)
        todoView.setEditTriggers(QAbstractItemView.DoubleClicked
                                 | QAbstractItemView.SelectedClicked)
        todoView.setSelectionBehavior(QAbstractItemView.SelectRows)
        todoView.verticalHeader().setDefaultSectionSize(20)
        todoView.horizontalHeader().setResizeMode(1, QHeaderView.Stretch)
        todoView.horizontalHeader().setResizeMode(2, QHeaderView.Fixed)
        todoView.setColumnWidth(2, 25)
        todoView.verticalHeader().hide()
        todoView.horizontalHeader().hide()
        todoView.setContextMenuPolicy(Qt.CustomContextMenu)
        todoView.customContextMenuRequested.connect(self.showContextMenu)
        self.slctModel = todoView.selectionModel()
        layout.addWidget(todoView)

        self.setLayout(layout)

        style = "QFrame#info {" \
            "border-width: 2px;" \
            "border-left-width: 1px;" \
            "border-style: solid;" \
            "border-color: rgb(93, 174, 255);" \
            "border-left-color: rgb(93, 174, 255);" \
            "background: white }"

        self.setStyleSheet(style)

    @staticmethod
    @Slot(QModelIndex)
    def showToolTip(index):
        if index.column() == 2:
            QToolTip.showText(QCursor.pos(), PRIORITY_TIP[index.data()-1])
        else:
            createDateIndex = index.sibling(index.row(), 3)
            createDate = createDateIndex.data()
            QToolTip.showText(QCursor.pos(), createDate + "\n" + index.data())

    @Slot(QPoint)
    def showContextMenu(self, point):
        ctxMenu = QMenu()
        if self.slctModel.hasSelection():
            actComp = ctxMenu.addAction("完成")
            actDel = ctxMenu.addAction("删除")
            actComp.triggered.connect(self.completeTodo)
            actDel.triggered.connect(self.deleteTodo)

        actNew = ctxMenu.addAction("新增")
        actNew.triggered.connect(self.newTodo)

        ctxMenu.exec_(QCursor.pos())

    @Slot()
    def completeTodo(self):
        idxList = []
        for index in self.slctModel.selectedRows():
            idx = index.data()
            idxList.append(idx)
        self.model.completeTodo(idxList)

    @Slot()
    def deleteTodo(self):
        idxList = []
        for index in self.slctModel.selectedRows():
            idx = index.data()
            idxList.append(idx)
        self.model.delTodo(idxList)

    @Slot()
    def newTodo(self):
        dialog = AddTodoDialog(self)
        if dialog.exec_():
            content = dialog.content.toPlainText()
            priority = dialog.priority.currentIndex() + 1
            if len(content):
                self.model.newTodo(priority, content)