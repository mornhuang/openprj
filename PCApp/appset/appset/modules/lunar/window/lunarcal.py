#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-28 10:41

"""

import datetime

from PySide.QtGui import *
from PySide.QtCore import *

from modules.lunar.algorithm import *
from utils.log import logged


_EN_FONT = QFont("arial", 11, QFont.Black)
_CN_FONT = QFont("arial", 9)
_TODAY_COLOR = Qt.white
_TODAY_BG_COLOR = QColor(255, 187, 0)
_EN_C_COLOR = Qt.black
_EN_NC_COLOR = QColor(191, 191, 191)
_EN_C_WD_COLOR = Qt.red
_CN_H_COLOR = Qt.red
_CN_NH_COLOR = QColor(153, 153, 153)
_INFO_COLOR = Qt.blue


class LunarCal(QCalendarWidget):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.__db = db
        self.__term = {}                    # {year: {"mmdd": "solar term name"}}
        self.__pg_data = {}                 # {QDate: {key1: val1, key2: val2}}
        self.__law_md = {}                  # {"ttmmdd": days}
        self.__law_d = set()
        self.__leave = [set(), {}]          # [set(year1, year2), {QDate: flag}]
        self.__date_rect = {}
        self.__ctxMenu = QMenu(self)
        self.__ctxActs = {}
        self.__ctxDate = None

        self.setMinimumSize(QSize(424, 400))
        self.__initSolarTerm()
        self.__getDBLawDay()
        self.__initLeaveDay()
        self.__initCurPage()
        self.__initCtxMenu()

    def paintCell(self, painter, rect, date):
        """
        Extend from super to handle lunar calendar show.
        """
        self.__paintDate(painter, rect, date)
        self.__paintFlag(painter, rect, date)
        self.__date_rect[date] = rect

    def __paintDate(self, painter, rect, date):
        """
        Paint solar date and lunar date info.
        """
        if date == QDate.currentDate():                 # Today
            painter.fillRect(self.__BoxRect(rect), QBrush(_TODAY_BG_COLOR))
            painter.setPen(_TODAY_COLOR)
            painter.setFont(_EN_FONT)
            painter.drawText(rect, Qt.AlignCenter, self.__pg_data[date]["solar"])
            painter.setFont(_CN_FONT)
            painter.drawText(rect, Qt.AlignCenter, self.__pg_data[date]["lunar"])

        else:
            if self.__pg_data[date]["isCM"]:          # Current Month day, except today
                if self.__pg_data[date]["isWD"]:
                    painter.setPen(_EN_C_WD_COLOR)
                else:
                    painter.setPen(_EN_C_COLOR)
                painter.setFont(_EN_FONT)
                painter.drawText(rect, Qt.AlignCenter, self.__pg_data[date]["solar"])

                if self.__pg_data[date]["isHD"]:
                    painter.setPen(_CN_H_COLOR)
                else:
                    painter.setPen(_CN_NH_COLOR)
                painter.setFont(_CN_FONT)
                painter.drawText(rect, Qt.AlignCenter, self.__pg_data[date]["lunar"])

                if date == self.selectedDate():
                    painter.setPen(QPen(_TODAY_BG_COLOR, 2))
                    painter.drawRect(self.__BoxRect(rect))

            else:                                       # Other Month day
                painter.setPen(_EN_NC_COLOR)
                painter.setFont(_EN_FONT)
                painter.drawText(rect, Qt.AlignCenter, self.__pg_data[date]["solar"])

                painter.setPen(_CN_NH_COLOR)
                painter.setFont(_CN_FONT)
                painter.drawText(rect, Qt.AlignCenter, self.__pg_data[date]["lunar"])

    def __paintFlag(self, painter, rect, date):
        """
        Paint extra function info flag.
        """
        if date in self.__leave[1]:
            flag = self.__leave[1][date]
            if flag == 1:           # leave day
                self.__drawInfo(painter, rect, 6, "休", Qt.white, Qt.gray)
            elif flag == 0:
                self.__drawInfo(painter, rect, 6, "班", Qt.white, Qt.red)

    @staticmethod
    def __BoxRect(rect):
        """
        Get box area to show frame.
        """
        innerRect = QRect(rect.left()+1, rect.top()+1, rect.width()-2, rect.height()-2)
        return innerRect

    @staticmethod
    def __InfoRect(rect, r, c):
        """
        Get area size for extra function flag show.
        """
        width = 15
        height = 17

        if c == 1:
            x = rect.left() + 2 + (c - 1) * width
            y = rect.top() + 2 + (r - 1) * height
        else:
            x = rect.left() + 13 + (c - 1) * width
            y = rect.top() + 2 + (r - 1) * height

        return QRect(x, y, width, height)

    @staticmethod
    def __drawInfo(painter, rect, pos, info, clr=None, bg_clr=None):
        """
        Draw extra function flag.
        """
        pos_rect = {
            1: LunarCal.__InfoRect(rect, 1, 1),
            2: LunarCal.__InfoRect(rect, 2, 1),
            3: LunarCal.__InfoRect(rect, 3, 1),
            4: LunarCal.__InfoRect(rect, 3, 3),
            5: LunarCal.__InfoRect(rect, 2, 3),
            6: LunarCal.__InfoRect(rect, 1, 3)
        }

        if bg_clr is not None:
            painter.fillRect(pos_rect[pos], bg_clr)

        if clr is not None:
            painter.setPen(clr)
        else:
            painter.setPen(_INFO_COLOR)

        painter.drawText(pos_rect[pos], Qt.AlignCenter, info)

    @logged
    def setCurrentPage(self, y, m):
        pds = QDate(y, m, 1).daysInMonth()
        sd = self.selectedDate().day()
        if sd <= pds:
            self.setSelectedDate(QDate(y, m, sd))
        else:
            self.setSelectedDate(QDate(y, m, pds))

        self.__getYearSolarTerm(y)
        self.__getDBYearLDS(y)
        if m == 12:
            self.__getYearSolarTerm(y+1)
            self.__getDBYearLDS(y+1)
        if m == 1:
            self.__getYearSolarTerm(y-1)
            self.__getDBYearLDS(y-1)

        self.__initPage(y, m)
        self.__date_rect.clear()

        super().setCurrentPage(y, m)

    def showToday(self):
        """
        Extends showToday to set current select day
        """
        super().showToday()

        self.setSelectedDate(QDate.currentDate())

    @logged
    def __getDBLawDay(self):
        """
        Get law holiday from database
        """
        rds = self.__db.queryLawDay()
        while rds.next():
            typal = rds.value(1)
            m = rds.value(2)
            d = rds.value(3)
            name = rds.value(4)
            hds = rds.value(5)
            key = "{:02d}{:02d}{:02d}".format(typal, m, d)
            self.__law_md[key] = (name, hds)
            self.__law_d.add(d)
        rds.finish()

    @logged
    def __initSolarTerm(self):
        """
        Get pre/cur/next year's solar term and save in variant to fast read data.
        """
        y = QDate.currentDate().year()
        self.__getYearSolarTerm(y-1)
        self.__getYearSolarTerm(y)
        self.__getYearSolarTerm(y+1)

    @logged
    def __getYearSolarTerm(self, y):
        """
        Get year's solar term string
        """
        if y not in self.__term:
            term_dic = solar_term_str_year(y)
            self.__term[y] = term_dic

    def __initLeaveDay(self):
        """
        Get pre/cur/next year's leave days
        """
        y = QDate.currentDate().year()
        self.__getDBYearLDS(y-1)
        self.__getDBYearLDS(y)
        self.__getDBYearLDS(y+1)

    def __getDBYearLDS(self, y):
        """
        Get leave days info for specific year.
        """
        if y not in self.__leave[0]:
            rds = self.__db.queryYearLeaveDay(y)
            while rds.next():
                m = rds.value(0)
                d = rds.value(1)
                flag = rds.value(2)
                self.__leave[1][QDate(y, m, d)] = flag
            rds.finish()

            self.__leave[0].add(y)

    @logged
    def __initCurPage(self):
        """
        Init current page.
        """
        cd = QDate.currentDate()
        y = cd.year()
        m = cd.month()
        self.__initPage(y, m)

    @logged
    def __initPage(self, y, m):
        """
        Initial page data. call this must after init solar term and init leave day.
        """
        # get first date of current page
        mfd = QDate(y, m, 1)
        mfdw = datetime.date(y, m, 1).weekday()
        if mfdw == 0:
            mfdw = 7
        date = mfd.addDays(-mfdw)

        # clear data first
        md_tmpl = "{:02d}{:02d}"
        key_tmpl = "{:02d}{:02d}{:02d}"
        self.__pg_data.clear()

        # begin init data
        for i in range(42):
            value = {}

            y1 = date.year()
            m1 = date.month()
            d1 = date.day()

            # is current month
            if m1 != m:
                value["isCM"] = False
            else:
                value["isCM"] = True

            # is weekday?
            if is_weekday(y1, m1, d1):
                value["isWD"] = True
            else:
                value["isWD"] = False

            # add solar day num string
            value["solar"] = str(d1) + "\n"

            # set default value
            value["isHD"] = False
            value["isLD"] = False

            # set lunar
            ld = lunar_day_num(y1, m1, d1)
            value["lunar"] = "\n" + lunar_day_to_str(ld)

            # add solar term
            md = md_tmpl.format(m1, d1)
            if md in self.__term[y1]:
                value["lunar"] = "\n" + self.__term[y1][md]
                value["isHD"] = True

            # add lunar law holiday
            if ld in self.__law_d:
                lm = lunar_month_num(y1, m1, d1)
                key = key_tmpl.format(1, lm, ld)
                if key in self.__law_md:
                    value["lunar"] = "\n" + self.__law_md[key][0]
                    value["isHD"] = True

                    if lm == 1 and ld == 1:         # chinese New Year
                        preDate = date.addDays(-1)
                        self.__pg_data[preDate]["lunar"] = "\n" + "除夕"
                        self.__pg_data[preDate]["isHD"] = True

                    hds = self.__law_md[key][1]
                    self.__addDefaultLD(date, 1, lm, ld, hds)

            # add solar law holiday
            key = key_tmpl.format(0, m1, d1)
            if key in self.__law_md:
                    value["lunar"] = "\n" + self.__law_md[key][0]
                    value["isHD"] = True

                    hds = self.__law_md[key][1]
                    self.__addDefaultLD(date, 0, 0, 0, hds)

            # save data and get next day's data
            self.__pg_data[date] = value
            date = date.addDays(1)

    def __addDefaultLD(self, date, typal, lm, ld, hds):
        """
        Add default leave day .
        """
        if typal == 1 and lm == 1 and ld == 1:       # Chinese New Year
            x = range(-1, hds-1)
        else:
            x = range(hds)

        for i in x:
            lvd = date.addDays(i)
            if lvd not in self.__leave[1]:
                self.__leave[1][lvd] = 1             # leave day
                self.__db.saveLeaveDay(lvd.year(), lvd.month(), lvd.day(), 1)

    def __initCtxMenu(self):
        act = QAction("上班", self)
        act.triggered.connect(self.setToWorkDay)
        self.__ctxMenu.addAction(act)
        self.__ctxActs["WorkDay"] = act

        act = QAction("休息", self)
        act.triggered.connect(self.setToLeaveDay)
        self.__ctxMenu.addAction(act)
        self.__ctxActs["LeaveDay"] = act

        act = QAction("取消", self)
        act.triggered.connect(self.cancelLeaveWorkDay)
        self.__ctxMenu.addAction(act)
        self.__ctxActs["CancelLWD"] = act

    def __setCtxMenu(self, date):
        """
        Set context action visible or invisible by condition of the date.
        """
        for tip, act in self.__ctxActs.items():         # reset all action visible
            act.setVisible(True)

        if date not in self.__leave[1] or self.__leave[1][date] == -1:
            self.__ctxActs["CancelLWD"].setVisible(False)
        elif self.__leave[1][date] == 1:        # leave day
            self.__ctxActs["LeaveDay"].setVisible(False)
        else:
            self.__ctxActs["WorkDay"].setVisible(False)

    @Slot()
    def setToWorkDay(self):
        if self.__ctxDate not in self.__leave[1]:
            self.__db.saveLeaveDay(self.__ctxDate.year(), self.__ctxDate.month(),
                                   self.__ctxDate.day(), 0)
        else:
            self.__db.updateLeaveDay(self.__ctxDate.year(), self.__ctxDate.month(),
                                     self.__ctxDate.day(), 0)
        self.__leave[1][self.__ctxDate] = 0

    @Slot()
    def setToLeaveDay(self):
        if self.__ctxDate not in self.__leave[1]:
            self.__db.saveLeaveDay(self.__ctxDate.year(), self.__ctxDate.month(),
                                   self.__ctxDate.day(), 1)
        else:
            self.__db.updateLeaveDay(self.__ctxDate.year(), self.__ctxDate.month(),
                                     self.__ctxDate.day(), 1)
        self.__leave[1][self.__ctxDate] = 1

    @Slot()
    def cancelLeaveWorkDay(self):
        if self.__ctxDate in self.__leave[1]:
            self.__db.saveLeaveDay(self.__ctxDate.year(), self.__ctxDate.month(),
                                   self.__ctxDate.day(), -1)
            self.__leave[1][self.__ctxDate] = -1

    def contextMenuEvent(self, event):
        pos = event.pos()
        for date in self.__date_rect:
            if date.month() == self.monthShown():   # only current month has context menu.
                rect = self.__date_rect[date]
                if rect.contains(pos):              # check this, we can get the correct date with right clicked.
                    self.__setCtxMenu(date)
                    self.__ctxDate = date
                    cur = self.cursor()
                    self.__ctxMenu.exec_(cur.pos())



