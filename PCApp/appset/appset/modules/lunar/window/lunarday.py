#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-29 17:03

"""
from PySide.QtGui import *
from PySide.QtCore import *
from modules.lunar.algorithm import *


class LunarDay(QFrame):
    def __init__(self, parent=None, date=QDate.currentDate()):
        super().__init__(parent)

        self.year_label = QLabel(self)
        self.week_label = QLabel(self)
        self.day_label = QLabel(self)
        self.ganzhi_label = QLabel(self)
        self.month_label = QLabel(self)
        self.solar_term_label = QLabel(self)
        self.yi_label = QLabel(self)
        self.ji_label = QLabel(self)
        self.yi_info_label = QLabel(self)
        self.ji_info_label = QLabel(self)

        self.setupUI()
        self.updateDay(date)

    def setupUI(self):
        self.setMinimumSize(QSize(152, 400))
        style = "background-color: rgb(93, 174, 255);" \
                "color: white"
        self.setStyleSheet(style)

        # set layout character
        layout1 = QHBoxLayout()
        layout1.addWidget(self.year_label)
        layout1.addWidget(self.week_label)
        layout1.setAlignment(Qt.AlignCenter)
        layout1.setContentsMargins(0, 10, 0, 10)

        layout2 = QVBoxLayout()
        layout2.addWidget(self.ganzhi_label)
        layout2.addWidget(self.month_label)
        layout2.addWidget(self.solar_term_label)
        layout2.setSpacing(8)
        layout2.setContentsMargins(0, 4, 0, 0)

        line = QFrame()
        style = "color: white"
        line.setStyleSheet(style)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setMinimumHeight(35)

        layout3 = QHBoxLayout()
        layout3.addWidget(self.yi_label)
        layout3.addWidget(self.ji_label)

        layout4 = QHBoxLayout()
        layout4.addWidget(self.yi_info_label)
        layout4.addWidget(self.ji_info_label)

        layout5 = QGridLayout()
        layout5.addWidget(self.day_label, 0, 0)

        layout = QVBoxLayout(self)
        layout.addLayout(layout1)
        layout.addLayout(layout5)
        layout.addLayout(layout2)
        layout.addWidget(line)
        layout.addLayout(layout3)
        layout.addLayout(layout4)
        layout.setStretch(5, 1)

        # set special character
        self.year_label.setFont(QFont("arial", 10))

        style = "background-color: rgb(255, 187, 0); " \
                "font-family: 'arial'; "\
                "font-size: 45px; " \
                "font-style: bold; "
        self.day_label.setStyleSheet(style)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.day_label.sizePolicy().hasHeightForWidth())
        self.day_label.setSizePolicy(sizePolicy)
        self.day_label.setMinimumSize(QSize(75, 75))
        self.day_label.setLayoutDirection(Qt.LeftToRight)
        self.day_label.setAlignment(Qt.AlignCenter)

        self.ganzhi_label.setAlignment(Qt.AlignCenter)
        self.month_label.setAlignment(Qt.AlignCenter)

        style = "color: red;" \
                "font-size: 20px; " \
                "font-style: bold; "
        self.solar_term_label.setStyleSheet(style)
        self.solar_term_label.setAlignment(Qt.AlignCenter)

        self.yi_label.setFont(QFont("arial", 20, QFont.Bold))
        self.yi_label.setAlignment(Qt.AlignCenter)
        self.yi_label.setText("宜")

        self.ji_label.setFont(QFont("arial", 20, QFont.Bold))
        self.ji_label.setAlignment(Qt.AlignCenter)
        self.ji_label.setText("忌")

        self.yi_info_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.ji_info_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

    @Slot(QDate)
    def updateDay(self, date):
        y = date.year()
        m = date.month()
        d = date.day()
        lunar = solar_to_lunar(y, m, d)

        year_str = "{:4d}-{:02d}-{:02d}".format(y, m, d)
        self.year_label.setText(year_str)
        week_str = "星期"
        week_str += lunar["week_day_str"]
        self.week_label.setText(week_str)

        self.day_label.setText(str(d))

        ganzhi_str = lunar["year_ganzhi"]
        ganzhi_str += "年 【"
        ganzhi_str += lunar["zodiac"]
        ganzhi_str += "年】"
        self.ganzhi_label.setText(ganzhi_str)

        month_str = lunar["lunar_month_cn"]
        month_str += "月"
        month_str += lunar["lunar_day_cn"]
        month_str += "   "
        month_str += lunar["constellation"]
        self.month_label.setText(month_str)

        month_str = lunar["solar_term"]
        self.solar_term_label.setText(month_str)

        #self.yi_info_label.setText("出行 纳财\n开市 交易\n立券 动土\n移徙 入宅\n裁衣 会亲友\n拆卸 进人口\n安香 经络\n出货财")
        #self.ji_info_label.setText("造庙 谢土\n作灶 作梁\n伐木 安葬\n行丧 修坟\n探病 ")

