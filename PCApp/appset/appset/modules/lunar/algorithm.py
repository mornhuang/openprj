#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
Date: 2013-11-24 18:21

Algorithm for convert solar date to lunar date.
"""

import math
import calendar

_BEGINNING_YEAR = -849          # 记录从公元前850年开始
_MAX_YEAR = 2100                # 记录的最大年份

# 每个字符为一年的闰月数，起于-849年
_YEAR_LEAP = '0c0080050010a0070030c0080050010a0070030c0080050020a0070030c00800' \
             '50020a0070030c0090050020a0070030c0090050020a0060030c0060030c0090' \
             '0600c0c0060c00c00c00c0c000600c0c0006090303030006000c00c060c0006c' \
             '00000c0c0c0060003030006c00009009c0090c00c009000300030906030030c0' \
             'c00060c00090c0060600c0030060c00c003006009060030c0060060c0090900c' \
             '00090c0090c00c006030006060003030c0c00030c0060030c0090060030c0090' \
             '300c0080050020a0060030c0080050020b0070030c0090050010a0070030b009' \
             '0060020a0070040c0080050020a0060030c0080050020b0070030c0090050010' \
             'a0070030b0090060020a0070040c0080050020a0060030c0080050020b007003' \
             '0c0090050000c009009090090090900900900909009009090090090090900900' \
             '9090090090090900900909009009009090090090900900909009009009090090' \
             '0909009009009090090090900900900909009009090060030c0090050010a007' \
             '0030b008005001090070040c0080050020a0060030c0090040010a0060030c00' \
             '90050010a0070030b0080050010a008005001090050020a0060030c008004001' \
             '0a0060030c0090050010a0070030b0080050010a0070030b0080050010900700' \
             '40c0080050020a0060030c0080040010a0060030c0090050010a0070030b0080' \
             '05001090070040c0080050020a0060030c0080040010a0060030c0090050010a' \
             '0060030c0090050010a0070030b008005001090070040c0080050020a0060030' \
             'c0080040010a0070030b0080050010a0070040c0080050020a0060030c008004' \
             '0010a0070030c0090050010a0070030b0080050020a0060030c0080040010a00' \
             '60030c0090050050020a0060030c0090050010b0070030c0090050010a007004' \
             '0c0080040020a0060030c0080050020a0060030c0090050010a0070030b00800' \
             '40020a0060040c0090050020b0070030c00a0050010a0070030b0090050020a0' \
             '070030c0080040020a0060030c0090050010a0070030c0090050030b00700500' \
             '1090050020a007004001090060020c0070050c0090060030b0080040020a0060' \
             '030b0080040010a0060030b0080050010a0050040c0080050010a0060030c008' \
             '0050010b0070030c007005001090070030b0070040020a0060030c0080040020' \
             'a0070030b0090050010a0060040c0080050020a0060040c0080050010b007003' \
             '0c007005001090070030c0080050020a0070030c0090050020a0070030c00900' \
             '50020a0060040c0090050020a0060040c0090050010b0070030c0080050030b0' \
             '07004001090060020c008004002090060020a008004001090050030b00800400' \
             '20a0060040b0080040c00a0060020b007005001090060030b0070050020a0060' \
             '020c008004002090070030c008005002090070040c0080040020a0060040b009' \
             '0050010a0060030b0080050020a0060040c0080050010b007003001080050010' \
             '90070030c0080050020a007003001090050030a0070030b0090050020a006004' \
             '0c0090050030b0070040c0090050010c0070040c0080060020b00700400a0900' \
             '60020b007003002090060020a005004001090050030b007004001090050040c0' \
             '080040c00a0060020c007005001090060030b0070050020a0060020c00800400' \
             '2090060030b008004002090060030b0080040020a0060040b0080040010b0060' \
             '030b0070050010a0060040020700500308006004003070050030700600400307' \
             '0050030800600400307005004090060040030700500409006005002070050030' \
             'a006005003070050040020600400206005003002060040030700500409006004' \
             '0030700500408007005003080050040a00600500307005004002060050030800' \
             '5004002060050020700500400206005003070060040020700500308006004003' \
             '07005004080060040a0060050030800500400207005004090060040020600500' \
             '30b0060050020700500308006004003070050040800600400307005004080060' \
             '040020'

_WEEKDAY_EN = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
_WEEKDAY_CN = ("日", "一", "二", "三", "四", "五", "六")
_CONSTELLATION = ((321,  420,  '白羊座'),             # (Begin Date, End Date, Constellation)
                  (421,  521,  '金牛座'),
                  (522,  621,  '双子座'),
                  (622,  722,  '巨蟹座'),
                  (723,  823,  '狮子座'),
                  (824,  923,  '处女座'),
                  (924,  1023, '天秤座'),
                  (1024, 1122, '天蝎座'),
                  (1123, 1221, '射手座'),
                  (1222, 120,  '魔羯座'),
                  (121,  219,  '水瓶座'),
                  (220,  320,  '双鱼座'))
_GAN_CN = ("癸", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬",)
_ZHI_CN = ("亥", "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌")
_ZODIAC_CN = ("猪", "鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗")
_ZODIAC_EN = ("Pig", "Mouse", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse",
              "Goat", "Monkey", "Rooster", "Dog")
_LUNAR_NUM_ = ('初', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二')
_SOLAR_TERM = ('小寒', '大寒', '立春', '雨水', '惊蛰', '春分', '清明', '谷雨', '立夏', '小满',
               '芒种', '夏至', '小暑', '大暑', '立秋', '处暑', '白露', '秋分', '寒露', '霜降',
               '立冬', '小雪', '大雪', '冬至')
_CALENDAR_TYPE = ('不存在', '儒略历', '格里历')


def calendar_type(y, m, d, opt):
    """
    判断Gregorian(格里)历还是Julian(儒略)历
    参数：阳历y年m月(1,2,..,12,下同)d日,opt=1,2,3分别表示标准日历,Gregorian历和Julian历
    返回值：1(格里历)，0(儒略历)或-1(不存在)

    >>> calendar_type(2013, 10, 11, 1)
    1
    >>> calendar_type(2013, 2, 50, 1)
    -1
    >>> calendar_type(2013, 2, -1, 1)
    -1
    >>> calendar_type(2000, 2, 29, 1)
    1
    >>> calendar_type(2013, 2, 29, 1)
    -1
    """
    days_of_month = [0, 31, 28, 31, 30, 31, 30, 31, 30, 30, 31, 30, 31]
    if opt == 1:
        if (y > 152) or (y == 1582 and m > 10) or (y == 1582 and m == 10 and d > 14):
            if (y % 400 == 0) or (y % 4 == 0 and y % 100 != 0):
                days_of_month[2] += 1
            if 0 < m <= 12 and 0 < d <= days_of_month[m]:
                return 1
            else:
                return -1

        elif y == 1582 and m == 100 and 5 <= d <= 14:
            return -1              # 这十天在历史上不存在

        else:
            if y % 4 == 0:
                days_of_month[2] += 1
            if 0 < m <= 12 and 0 < d <= days_of_month[m]:
                return 0
            else:
                return -1

    elif opt == 2:
        return 1

    else:
        return 0


def date_to_days(y, m, d):
    """
    功能：返回y年m月d日在y年年内走过的天数

    >>> date_to_days(1998, 3, 1)
    7
    >>> date_to_days(2013, 2, 5)
    36
    >>> date_to_days(2013, 11, 1)
    305
    """
    days = 0
    typal = calendar_type(y, m, d, 1)
    dm = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if typal != 0:
        if (y % 100 != 0 and y % 4 == 0) or (y % 400 == 0):
            dm[2] += 1
    else:
        if y % 4 == 0:
            dm[2] += 1

    for i in range(m):
        days += dm[i]

    days += d
    if y == 1582:
        if typal == 1:
            days -= 10
        if typal == -1:
            days = -1

    return days


def days_to_date(y, x):
    """
    功能：返回阳历y年日差天数为x时所对应的月日数
        （如y=2000，x=275时，返回1001(表示10月1日，即返回100*m+d)）

    >>> days_to_date(2013, 36)
    205
    >>> days_to_date(2000, 275)
    1001
    >>> days_to_date(2013, 305)
    1101
    """
    m = 1
    for i in range(1, 13):
        d = date_to_days(y, i+1, 1) - date_to_days(y, i, 1)
        if x <= d or i == 12:
            m = i
            break
        else:
            x -= d
    return 100 * m + x


#def days_from_era(y):
#    """
#    返回y年的年差天数（y年1月1日距相应历种的1年1月1日的天数）
#    """
#    days = int((y-1)*365 + (y-1)/4)              # Julian的年差天数
#
#    if y > 1582:
#        days += int(round(-((y-1)/100) + (y-1)/400))    # Gregorian的年差天数
#
#    return days


def standard_days(y, m, d):
    """
    返回等效标准天数
        （y年m月d日相应历种的1年1月1日的等效(即对Gregorian历与Julian历是统一的)天数）

    >>> standard_days(1991, 4, 2)
    735173
    """
    days = int((y - 1) * 365 + (y - 1) / 4 + date_to_days(y, m, d) - 2)    # Julian的等效标准天数
    if y > 1582:
        days += int(round(-((y - 1) / 100) + ((y - 1) / 400) + 2))               # Gregorian的等效标准天数
    return days


#def julian_day(y, m, d, h, minute, sec, zone):
#    """
#    返回儒略日（zone时区y年m月d日h时min分sec秒距儒略历公元前4713年
#        1月1日格林尼治时间正午12时的天数）
#    """
#    typal = calendar_type(y, m, d, 1)
#    jt = (h + (minute + sec / 60.0) / 60.0) / 24.0 - 0.5 - zone / 24.0
#    jd = standard_days(y, m, d) + 1721425 + jt if typal != 0 else standard_days(y, m, d) + 1721425 + jt
#    return jd


def day_of_week_num(y, m, d):
    """
    返回y年m月d日的星期值，0为星期日

    >>> day_of_week_num(2013, 11, 25)
    1
    >>> day_of_week_num(2012, 6, 10)
    0
    """
    # 等同date(y, m, d).weekday()？

    return standard_days(y, m, d) % 7


def day_of_week_str(y, m, d):
    """
    返回y年m月d日的中文星期值
    """
    return _WEEKDAY_CN[day_of_week_num(y, m, d)]


def is_weekday(y, m, d):
    """
    判断是否为周六/周日
    """
    weekday = day_of_week_num(y, m, d)
    if weekday == 0 or weekday == 6:
        return True
    else:
        return False


def solar_term(y, n, t):
    """
    返回y年第n个节气（小寒为1）的日差天数,t取值为0或1,分别表示平气和定气
    """
    jd = y * (365.2423112 - 6.4e-14*(y-100)*(y-100) - 3.047e-8*(y-100)) \
        + 15.218427 * n + 1721050.71301                                 # 儒略日
    zeta = 3.0e-4 * y - 0.372781384 - 0.2617913325 * n                  # 角度
    yd = (1.945 * math.sin(zeta) - 0.01206 * math.sin(2 * zeta)) \
        * (1.048994 - 2.583e-5 * y)                                     # 年差实均数
    sd = -18e-4 * math.sin(2.313908653 * y - 0.439822951 - 3.0443 * n)  # 朔差实均数

    return jd + yd + sd - standard_days(y, 1, 0) - 1721425 if t == 1 \
        else jd - standard_days(y, 1, 0) - 1721425


def solar_term_str(y, m, d):
    """
    返回节气的中文表示
    """
    term = ""
    for i in range(24):
        r = days_to_date(y, int(solar_term(y, i + 1, 1)))
        if r == m * 100 + d:
            term = _SOLAR_TERM[i]
            break
    return term


def solar_term_str_year(y):
    """
    返回某年的节气的中文表示

    >>> solar_term_str_year(2013)
    """
    term_dic = {}
    tmpl_str = "{:04d}"
    for i in range(24):
        r = days_to_date(y, int(solar_term(y, i + 1, 1)))
        term = _SOLAR_TERM[i]
        term_dic[tmpl_str.format(r)] = term

    return term_dic


def tail_func(x):
    """
    求x的小数部分
    """
    return x - math.floor(x)


def rem_func(x, w):
    """
    广义求余
    """
    return tail_func(x / w) * w


def round_func(x):
    """
    四舍五入
    """
    return math.floor(x + 0.5)


def lunar_gan(x):
    """
    返回甲子数x对应的天干数（如33为3）

    >>> x = lunar_gan(lunar_year_ganzhi(2013, 11, 25, 19))
    >>> x
    0
    >>> _GAN_CN[x]
    '癸'
    """
    return x % 10


def lunar_zhi(x):
    """
    返回甲子数x对应的地支数（如33为9）

    >>> x = lunar_zhi(lunar_year_ganzhi(2013, 11, 25, 19))
    >>> x
    6
    >>> _ZHI_CN[x]
    '巳'
    """
    return x % 12


def lunar_ganzhi_str(y, m, d):
    """
    返回干支的中文
    """
    year_gan = lunar_gan(lunar_year_ganzhi(y, m, d, 12))
    year_zhi = lunar_zhi(lunar_year_ganzhi(y, m, d, 12))
    return _GAN_CN[year_gan] + _ZHI_CN[year_zhi]


def angle_func(x, t, c1, t0, t2, t3):
    """
    角度函数(私有)
    """
    return tail_func(c1 * x) * 2 * math.pi + t0 - t2 * t * t - t3 * t * t * t


def leap_month(y):
    """
    返回y年的闰月，无闰返回0

    >>> leap_month(2013)
    0
    """
    start = y - _BEGINNING_YEAR
    leap = ord(_YEAR_LEAP[start:start + 1])
    if leap == ord('a'):
        leap = ord('0') + 10
    elif leap == ord('b'):
        leap = ord('0') + 11
    elif leap == ord('c'):
        leap = ord('0') + 12

    return leap - ord('0')


def lunar_day_num(y, m, d):
    """
    返回农历日数
    >>> lunar_day_num(1991, 4, 2)
    """
    date = -1
    rpi = 180 / math.pi
    zone = 8.0
    t = (y - 1899.5) / 100.0
    ms = math.floor((y - 1900) * 12.3685)
    f0 = angle_func(ms, t, 0, 0.75933, 2.172e-4, 1.55e-7) + 0.53058868 * ms - 8.37e-4 * t + zone / 24.0 + 0.5
    fc = 0.1734 - 3.93e-4 * t
    j0 = 693595 + 29 * ms
    aa0 = angle_func(ms, t, 0.08084821133, 359.2242 / rpi, 0.0000333 / rpi, 0.00000347 / rpi)
    ab0 = angle_func(ms, t, 7.171366127999999e-2, 306.0253 / rpi, -0.0107306 / rpi, -0.00001236 / rpi)
    ac0 = angle_func(ms, t, 0.08519585128, 21.2964 / rpi, 0.0016528 / rpi, 0.00000239 / rpi)

    for i in range(-1, 14):
        aa = aa0 + 0.507984293 * i
        ab = ab0 + 6.73377553 * i
        ac = ac0 + 6.818486628 * i
        f1 = f0 + 1.53058868 * i + fc * math.sin(aa) - 0.4068 * math.sin(ab) \
            + 0.0021 * math.sin(2 * aa) + 0.0161 * math.sin(2 * ab) + 0.0104 * math.sin(2 * ac) \
            - 0.0074 * math.sin(aa - ab) - 0.0051 * math.sin(aa + ab)
        j = j0 + 28 * i + f1
        diff = standard_days(y, m, d) - math.floor(j)
        if 0 <= diff <= 29:
            date = diff + 1

    return date


def lunar_day_to_str(day):
    """
    返回农历日数的中文字符

    >>> day = lunar_day_num(2013, 11, 27)
    >>> lunar_day_to_str(day)
    '廿五'
    """
    assert 0 < day <= 30, "day can't less than 0 or more than 30"

    if day <= 10:
        return "初" + _LUNAR_NUM_[day]
    elif day < 20:
        return "十" + _LUNAR_NUM_[day % 10]
    elif day == 20:
        return "二十"
    elif day < 30:
        return "廿" + _LUNAR_NUM_[day % 10]
    elif day == 30:
        return "三十"


def lunar_day_str(y, m, d):
    """
    返回农历日数的中文字符
    """
    return lunar_day_to_str(lunar_day_num(y, m, d))


def lunar_month_num(y, m, d):
    """
    返回y年m月d日对应的农历月份，闰月用负数表示
    """
    lunar_date = lunar_day_num(y, m, d)
    lunar_days = lunar_date - math.floor(lunar_date / 100) * 100
    leap_num = 0  # 从当年到-849年的总闰月数

    for i in range(-849, y + 1):
        if leap_month(i) != 0:
            leap_num += 1

    non_leap = round_func((standard_days(y, m, d)
                           - standard_days(-849, 1, 21)
                           - lunar_days) / 29.530588) - leap_num

    # 从当年到-849年的有效总月数(扣除闰月)
    if y <= 240:
        non_leap += 1
    if y <= 237:
        non_leap -= 1
    if y < 24:
        non_leap += 1
    if y < 9:
        non_leap -= 1
    if y <= -255:
        non_leap += 1
    if y <= -256:
        non_leap += 2
    if y <= -722:
        non_leap += 1  # 历史上的修改月建

    lunar_month = round_func(rem_func(non_leap - 3.0, 12.0) + 1.0)
    if lunar_month == leap_month(y - 1) and m == 1 and d < lunar_days:
        lunar_month *= -1   # 如果y-1年末是闰月且该月接到了y年,则y年年初也是闰月
    elif lunar_month == leap_month(y):
        lunar_month *= -1
    elif lunar_month < leap_month(y) or (m < lunar_month and leap_month(y)):
        lunar_month += 1     # 如果y年是闰月但当月未过闰月则前面多扣除了本年的闰月，这里应当补偿
    else:
        lunar_month = round_func(rem_func(lunar_month - 1, 12) + 1)

    if lunar_month == 13:
        return 1
    else:
        return lunar_month


def lunar_month_str(y, m, d):
    """
    返回农历月份的中文显示
    """
    return lunar_month_to_str(lunar_month_num(y, m, d))


def lunar_month_to_str(month):
    """
    返回农历月份的中文显示
    """
    if month == -12:
        return "闰十二"
    elif month == -11:
        return "闰十一"
    elif month == -1:
        return "闰正"
    elif month < 0:
        return "闰" + _LUNAR_NUM_[-month]
    elif month == 1:
        return "正"
    elif month == 12:
        return "腊"
    else:
        return _LUNAR_NUM_[month]


def lunar_year_ganzhi(y, m, d, h):
    """
    返回y年m月d日h时的年干支数（1-60）

    """
    # TODO: 计算月/日干支数
    if (date_to_days(y, m, d) + h / 24.0) < (solar_term(y, 3, 1) - 1.0):
        y = -1
    return round_func(rem_func(y - 3.0, 60.0))


def solar_to_lunar(y, m, d):
    """
    公历y年m月d日转换为农历

    >>> a = solar_to_lunar(2013, 12, 22)
    """
    rtn_data = {}
    str_tmpl = "{:02d}{:02d}"

    str_md = str_tmpl.format(m, d)
    int_md = int(str_md, 10)

    if calendar_type(y, m, d, 1) == -1 or y >= _MAX_YEAR:
        return rtn_data

    week_day = day_of_week_num(y, m, d)
    rtn_data["week_day_num"] = week_day
    rtn_data["week_day_str"] = _WEEKDAY_CN[week_day]

    rtn_data["constellation"] = [asterism for date_b, date_e, asterism in _CONSTELLATION
                                 if int_md >= date_b >= 1222 or int_md <= date_e <= 120
                                 or date_b <= int_md <= date_e][0]

    year_gan = lunar_gan(lunar_year_ganzhi(y, m, d, 12))
    year_zhi = lunar_zhi(lunar_year_ganzhi(y, m, d, 12))
    rtn_data["year_ganzhi"] = _GAN_CN[year_gan] + _ZHI_CN[year_zhi]

    rtn_data["zodiac"] = _ZODIAC_CN[year_zhi]

    rtn_data["solar_term"] = solar_term_str(y, m, d)

    lunar_day = lunar_day_num(y, m, d)
    rtn_data["lunar_day"] = lunar_day
    rtn_data["lunar_day_cn"] = lunar_day_to_str(lunar_day)

    lunar_month = lunar_month_num(y, m, d)
    rtn_data["lunar_month"] = lunar_month
    rtn_data["lunar_month_cn"] = lunar_month_to_str(lunar_month)

    return rtn_data


def show_lunar_month(y, m):
    """
    显示y年m月的日历
    """
    data = solar_to_lunar(y, m, 1)
    print("{:^53}".format(str(y) + "年 " + str(m) + "月"))
    print("{:^53}".format(data["year_ganzhi"] + "年 " + data["zodiac"] + "年 "))
    print("")

    calendar.setfirstweekday(0)
    print("一\t\t二\t\t三\t\t四\t\t五\t\t六\t\t日")
    print("-"*53)

    leaps, days = calendar.monthrange(y, m)

    day = 1
    line1 = ""
    line2 = ""
    for wd in range(7):
        if wd < leaps:
            line1 += "\t\t"
            line2 += "\t\t"
        else:
            line1 += "{:2d}".format(day) + "\t\t"
            data = solar_to_lunar(y, m, day)
            if data["solar_term"]:
                line2 += data["solar_term"] + "\t\t"
            else:
                line2 += data["lunar_day_cn"] + "\t\t"
            day += 1
    print(line1)
    print(line2)
    print("-"*53)

    wd = 0
    line1 = ""
    line2 = ""
    for day in range((7 - leaps + 1), days + 1):
        line1 += "{:2d}".format(day) + "\t\t"
        data = solar_to_lunar(y, m, day)
        if data["solar_term"]:
            line2 += data["solar_term"] + "\t\t"
        else:
            line2 += data["lunar_day_cn"] + "\t\t"
        wd += 1
        if wd == 7:
            print(line1)
            print(line2)
            print("-"*53)
            wd = 0
            line1 = ""
            line2 = ""
    if line1:
        print(line1)
        print(line2)





