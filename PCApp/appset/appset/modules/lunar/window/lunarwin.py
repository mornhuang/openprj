#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-28 10:34

"""

from modules.lunar.window.lunarcal import *
from modules.lunar.window.lunarcalnav import *
from modules.lunar.window.lunarday import *
from modules.lunar.window.lunarinfo import *
from modules.lunar.window.lunartip import *
from modules.lunar.dao.lunardb import LunarDB


class LunarWin(QWidget):
    def __init__(self, parent, conf):
        super().__init__(parent)
        parent.setWindowTitle(self.tr("LunarCalendar"))
        self.__conf = conf
        self.__db = LunarDB(conf.getDataFile())

        self.gridLayout = QGridLayout(self)
        self.lunar_cal = LunarCal(self, self.__db)
        self.lunar_cal_nav = LunarCalNav(self)
        self.lunar_day = LunarDay(self)
        self.lunar_info = LunarInfo(self, self.__db)
        self.lunar_tip = LunarTip(self, self.__db)
        self.setupUi()

        self.lunar_cal_nav.today.clicked.connect(self.navToday)
        self.lunar_cal_nav.year.valueChanged.connect(self.navPageChange)
        self.lunar_cal_nav.month.currentIndexChanged.connect(self.navPageChange)
        self.lunar_cal.selectionChanged.connect(self.selectChanged)
        self.lunar_cal.currentPageChanged.connect(self.currentPageChanged)

    def setupUi(self):
        self.setObjectName(self.tr("LunarWin"))

        # add lunar_day
        self.gridLayout.addWidget(self.lunar_day, 0, 0, 3, 1)

        # add lunar_cal_nav
        self.gridLayout.addWidget(self.lunar_cal_nav, 0, 1, 1, 1)

        # add lunar_cal
        self.lunar_cal.setNavigationBarVisible(False)
        self.lunar_cal.setHorizontalHeaderFormat(QCalendarWidget.ShortDayNames)
        self.lunar_cal.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.lunar_cal.setGridVisible(True)
        self.lunar_cal.setMaximumDate(QDate(2099, 12, 31))
        self.lunar_cal.setMinimumDate(QDate(1900, 1, 1))
        self.lunar_cal.setFirstDayOfWeek(Qt.Monday)
        self.gridLayout.addWidget(self.lunar_cal, 1, 1, 1, 1)

        # add lunar_tip
        self.gridLayout.addWidget(self.lunar_tip, 2, 1, 1, 1)

        # add lunar_info
        self.gridLayout.addWidget(self.lunar_info, 0, 2, 3, 1)

        # other setting
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setRowStretch(2, 1)

    @Slot()
    def navPageChange(self):
        year = self.lunar_cal_nav.year.value()
        month = self.lunar_cal_nav.month.currentIndex() + 1

        self.lunar_cal.setCurrentPage(year, month)

    @Slot()
    def navToday(self):
        date = QDate.currentDate()
        y = date.year()
        m = date.month()
        self.lunar_cal_nav.year.setValue(y)
        self.lunar_cal_nav.month.setCurrentIndex(m-1)
        self.lunar_cal.showToday()

    @Slot()
    def selectChanged(self):
        self.lunar_day.updateDay(self.lunar_cal.selectedDate())
        self.lunar_tip.updateDay(self.lunar_cal.selectedDate())

    @Slot(int, int)
    def currentPageChanged(self, year, month):
        old_year = self.lunar_cal_nav.year.value()
        old_month = self.lunar_cal_nav.month.currentIndex() + 1
        if old_year != year:
            self.lunar_cal_nav.year.setValue(year)
        if old_month != month:
            self.lunar_cal_nav.month.setCurrentIndex(month-1)


if __name__ == "__main__":
    import sys
    from modules.lunar.settings.lunarconf import LunarConf

    app = QApplication(sys.argv)
    mainWin = QMainWindow()
    conf1 = LunarConf()
    cal = LunarWin(mainWin, conf1)
    mainWin.setCentralWidget(cal)
    mainWin.resize(424, 400)
    mainWin.show()
    app.exec_()