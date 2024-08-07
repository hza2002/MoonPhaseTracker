# -*- coding: utf-8 -*-
# Lunar Phase Prediction
# 本程序定义一个月相周期从右边开始形成满月，再从右边逐渐消失，且为北半球观测结果
# 月相数据参考：https://www.moonconnection.com/moon_phases_calendar.phtml
import calendar
import datetime
import math
import tkinter
import tkinter.ttk
import turtle


def process_day(year, month):
    """将 calendar 生成的某月二维列表转化为日期一维列表"""
    date_list = []
    for i in calendar.monthcalendar(int(year), int(month)):
        for j in range(7):
            if i[j] != 0:
                date_list.append(i[j])
    return date_list


moonCycle = 29.5305882  # 月相周期/天
yearConst, monthConst, dayConst = 2002, 9, 7  # 基准日期
angleMoonConst = 0  # 基准日期月相角度
yearList = [i for i in range(1930, 2030)]
monthList = [i + 1 for i in range(12)]
dayList = process_day(yearConst, monthConst)


def angle_calculate(year, month, day):  # 输入年月日计算当天角度
    date_delta = datetime.date(year, month, day) - datetime.date(
        yearConst, monthConst, dayConst)
    angle_list = []  # 记录附近 3 个点的角度值
    for i in [-1, 0, 1]:
        angle_list.append(
            (angleMoonConst * moonCycle +
             ((date_delta.days + i) % moonCycle)) % moonCycle / moonCycle * 360)
    if angle_list[1] - angle_list[0] < 0 and 360 - angle_list[0] >= angle_list[1]:
        angle_list[1] = 0
    elif angle_list[2] - angle_list[1] < 0 and 360 - angle_list[1] <= angle_list[2]:
        angle_list[1] = 0
    elif angle_list[1] >= 180 >= angle_list[0] and angle_list[1] - 180 < 180 - angle_list[0]:
        angle_list[1] = 180
    elif angle_list[2] >= 180 >= angle_list[1] and angle_list[2] - 180 > 180 - angle_list[1]:
        angle_list[1] = 180
    return angle_list[1]


def draw_moon(a, moon, r, day="", list=[], c=0):
    """输入角度和 turtle 画笔，绘制当天月相图
    Args:
            a: 输入内圆弧度数 [0-360)
            moon: RawTurtle
            r: 输入外圆半径
            list: 位置坐标
            c: 旋转角度
    """
    moon.seth(0)
    moon.color("white")
    if a == 180:
        moon.color("yellow")
    moon.pensize(0)
    moon.hideturtle()
    moon.up()
    if list:
        moon.goto(list[1], list[0])
        moon.write(day, font=("Copperplate", 18, "bold"), align="center")
    if a == 0:
        moon.begin_fill()
        moon.fillcolor("#282C34")
        moon.circle(-r)
        moon.end_fill()
    else:
        if a > 180:
            a, c = 360 - a, 180
        else:
            moon.right(90)
            moon.fd(2 * r)
            moon.left(90)
        moon.down()
        moon.setheading(c)
        moon.begin_fill()
        moon.circle(r, 180)
        moon.left(-a)
        moon.circle(r / math.cos(a * math.pi / 180), -abs(180 - 2 * a))
        moon.end_fill()


def moon(a):
    """在画布上绘制当天月相图
    Args:
            a: 输入内圆弧度数 [0-360)
    """
    moon_screen = turtle.TurtleScreen(moonCanvas)
    moon_screen.bgpic("resources/sky.png")
    moon_screen.screensize(300, 650)
    moon_screen.tracer(n=0, delay=0)
    moon = turtle.RawTurtle(moon_screen)
    draw_moon(a, moon, r=100, list=[100, -20])


def moon_calendar(year, month):
    """在画布上绘制整月月相图"""
    moon_calendar_screen = turtle.TurtleScreen(moonCalendarCanvas)
    moon_calendar_screen.tracer(n=0, delay=0)
    moon_calendar_screen.bgpic("resources/sky.png")
    moon_calendar_screen.screensize(720, 650)
    moon_calendar_screen.setworldcoordinates(0, -650, 720, 0)
    moon = turtle.RawTurtle(moon_calendar_screen)
    # 绘制星期标签栏
    week_name = [
        "Monday", "Tuesday", "Wednesday", "Tuesday", "Friday", "Saturday",
        "Sunday"
    ]
    for column in range(7):
        moon.pencolor("white")
        moon.penup()
        moon.goto(x=column * 105 + 50, y=0)
        moon.pendown()
        moon.write(week_name[column],
                   font=("Copperplate", 18, "bold"),
                   align="center")
    # 绘制月亮
    for row, i in enumerate(calendar.monthcalendar(year, month)):
        for column in range(7):
            if i[column] != 0:
                draw_moon(
                    angle_calculate(year, month, i[column]),
                    moon,
                    day=i[column],
                    r=30,
                    list=[-row * 105 - 50, column * 105 + 50],
                )


def change():
    """获取当前年月日，并返回元组"""
    global dayList, chooseDay
    dayList = process_day(int(chooseYear.combobox.get()),
                          int(chooseMonth.combobox.get()))
    chooseDay.combobox["value"] = dayList
    if int(chooseDay.combobox.get()) not in dayList:
        chooseDay.var.set(chooseDay["value"][-1])
    return int(chooseYear.combobox.get()), int(chooseMonth.combobox.get()), int(
        chooseDay.combobox.get())


def change_moon(*args):
    """更改当天月相图"""
    tuple = change()
    moon(angle_calculate(tuple[0], tuple[1], tuple[2]))


def change_all(*args):
    """更改所有月相图"""
    tuple = change()
    moon(angle_calculate(tuple[0], tuple[1], tuple[2]))
    moon_calendar(tuple[0], tuple[1])


top = tkinter.Tk()
top.resizable(False, False)  # 设置窗体不可放缩
top.title("Lunar Phase Prediction")  # 窗体标题
top.configure(bg="#FDFFFB")  # 窗体颜色
top.iconphoto(False, tkinter.PhotoImage(file='resources/icon.png'))  # 窗体图标

# 设置窗口初始位置在屏幕居中
winWidth, winHeight = 1080, 690  # 设置窗口大小
x = int((top.winfo_screenwidth() - winWidth) / 2)
y = int((top.winfo_screenheight() - winHeight) / 2)
top.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))

# 侧边栏
labalMain = tkinter.Label(top, text="月\n相\n图\n预\n测", bg="black", fg="white", font=("微软雅黑", 40))
labalMain.grid(row=1, column=0, sticky=tkinter.NSEW)

# 月相画布
moonCanvas = tkinter.Canvas(master=top, relief="groove", bg="black", width=300, height=650)
moonCanvas.grid(row=1, column=1)

# 整月月相图
moonCalendarCanvas = tkinter.Canvas(master=top, relief="groove", bg="black", width=720, height=650)
moonCalendarCanvas.grid(row=0, rowspan=2, column=2, sticky=tkinter.NSEW)

# 日期选择栏
dateframe = tkinter.LabelFrame(top, relief="groove")
dateframe.grid(row=0, column=0, columnspan=2, sticky=tkinter.NSEW)


class Choosedate:
    """定义类选择日期
    Attributes:
            labelframe: 包含 label 和 combobox
            label: 指示 combobox
            var: combobox 的变量，归属于全局窗口
            combobox: 选择框
    """

    def __init__(self, name, list, function):
        self.labelframe = tkinter.LabelFrame(dateframe, relief="flat")
        self.label = tkinter.Label(self.labelframe,
                                   relief="flat",
                                   text=name,
                                   font=("微软雅黑", 16))
        self.label.grid(row=0, column=0)
        self.var = tkinter.StringVar(top)
        self.combobox = tkinter.ttk.Combobox(self.labelframe,
                                             textvariable=self.var,
                                             state="readonly",
                                             value=list,
                                             width=4)
        self.combobox.bind("<<ComboboxSelected>>", function)
        self.combobox.grid(row=0, column=1)


# 选择年份
chooseYear = Choosedate("Year", yearList, change_all)
chooseYear.var.set(datetime.datetime.today().year)
chooseYear.labelframe.grid(row=0, column=0)
# 选择月份
chooseMonth = Choosedate("Month", monthList, change_all)
chooseMonth.var.set(datetime.datetime.today().month)
chooseMonth.labelframe.grid(row=0, column=1)
# 选择日期
chooseDay = Choosedate("Day", dayList, change_moon)
chooseDay.var.set(datetime.datetime.today().day)
chooseDay.labelframe.grid(row=0, column=2)

change_all()  # 初始化界面

top.mainloop()
