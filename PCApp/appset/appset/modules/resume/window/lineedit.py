#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-17 18:13
Line Edit with clear button
"""

from PySide.QtCore import *
from PySide.QtGui import *
from modules.resume.resume_rc import *


class LineEdit(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)

        self.clearButton = QToolButton(self)
        pixmap = QPixmap(":/images/close.png")
        self.clearButton.setIcon(QIcon(pixmap))
        self.clearButton.setIconSize(QSize(16, 16))
        self.clearButton.setCursor(Qt.ArrowCursor)
        self.clearButton.setStyleSheet("QToolButton { border: none; padding: 0px; }")
        self.clearButton.hide()
        self.clearButton.clicked.connect(self.clear)
        self.textChanged.connect(self.__updateCloseButton)
        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        style = "QLineEdit { " + \
            "padding-right: {0}px;".format(self.clearButton.sizeHint().width() + frameWidth + 1) + \
            " }"
        self.setStyleSheet(style)
        msz = self.minimumSizeHint()
        self.setMinimumSize(max(msz.width(), self.clearButton.sizeHint().height() + frameWidth * 2 + 2),
                            max(msz.height(), self.clearButton.sizeHint().height() + frameWidth * 2 + 2))

    def resizeEvent(self, *args, **kwargs):
        sz = self.clearButton.sizeHint()
        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.clearButton.move(self.rect().right() - frameWidth - sz.width(),
                              (self.rect().bottom() + 1 - sz.height())/2)

    @Slot()
    def __updateCloseButton(self, text):
        self.clearButton.setVisible(len(text))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
