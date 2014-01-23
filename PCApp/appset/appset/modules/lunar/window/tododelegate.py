#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-12-09 12:54

"""

from PySide.QtGui import *
from PySide.QtCore import *

PRIORITY_COLOR = {
    1: Qt.red,
    2: QColor(128, 64, 191),
    3: QColor(250, 170, 0),
    4: Qt.gray
}

PRIORITY_TIP = {
    0: "紧急重要",
    1: "紧急不重要",
    2: "重要不紧急",
    3: "不重要不紧急"
}


class TodoDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        if index.column() == 2:
            x = option.rect.left() + (option.rect.width() - 12)/2
            y = option.rect.top() + (option.rect.height() - 12)/2
            rect = QRect(x, y, 12, 12)
            if option.state & QStyle.State_Selected:
                painter.fillRect(option.rect, option.palette.highlight())
            painter.fillRect(rect, PRIORITY_COLOR[index.data()])

        else:
            super().paint(painter, option, index)

    def createEditor(self, parent, option, index):
        if index.column() == 2:
            editor = QComboBox(parent)
            pixmap = QPixmap(12, 12)

            pixmap.fill(PRIORITY_COLOR[1])
            icon = QIcon(pixmap)
            editor.addItem(icon, None)
            editor.setItemData(0, PRIORITY_TIP[0], Qt.ToolTipRole)

            pixmap.fill(PRIORITY_COLOR[2])
            icon = QIcon(pixmap)
            editor.addItem(icon, None)
            editor.setItemData(1, PRIORITY_TIP[1], Qt.ToolTipRole)

            pixmap.fill(PRIORITY_COLOR[3])
            icon = QIcon(pixmap)
            editor.addItem(icon, None)
            editor.setItemData(2, PRIORITY_TIP[2], Qt.ToolTipRole)

            pixmap.fill(PRIORITY_COLOR[4])
            icon = QIcon(pixmap)
            editor.addItem(icon, None)
            editor.setItemData(3, PRIORITY_TIP[3], Qt.ToolTipRole)

            editor.currentIndexChanged.connect(self.commitAndCloseEditor)
            editor.highlighted.emit(index.data()-1)
        else:
            editor = QPlainTextEdit(parent)
            editor.setMinimumHeight(100)
            #editor = super().createEditor(parent, option, index)

        return editor

    def setEditorData(self, editor, index):
        if index.column() == 2:
            editor.setCurrentIndex(index.data() - 1)
        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if index.column() == 2:
            model.setData(index, editor.currentIndex() + 1, Qt.EditRole)
        else:
            super().setModelData(editor, model, index)

    @Slot()
    def commitAndCloseEditor(self):
        editor = self.sender()
        self.commitData.emit(editor)
        self.closeEditor.emit(editor, QAbstractItemDelegate.NoHint)
