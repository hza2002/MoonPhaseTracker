# -*- coding: utf-8 -*-
# Lunar Phase Prediction
# 本程序定义一个月相周期从右边开始形成满月，再从右边逐渐消失，且为北半球观测结果
# 月相数据参考：https://www.moonconnection.com/moon_phases_calendar.phtml
import math
import turtle
import calendar
import datetime
import tkinter
import tkinter.ttk


def processDay(year, month):
    """将 calendar 生成的某月二维列表转化为日期一维列表"""
    list = []
    for i in calendar.monthcalendar(int(year), int(month)):
        for j in range(7):
            if i[j] != 0: list.append(i[j])
    return list


moonCycle = 29.5305882  # 月相周期/天
yearConst, monthConst, dayConst = 2002, 9, 7  # 基准日期
angleMoonConst = 0  # 基准日期月相角度
yearList = [i for i in range(1930, 2030)]
monthList = [i + 1 for i in range(12)]
dayList = processDay(yearConst, monthConst)


def angleCalculate(year, month, day):  # 输入年月日计算当天角度
    dateDelta = datetime.date(year, month, day) - datetime.date(
        yearConst, monthConst, dayConst)
    angleList = []  # 记录附近 3 个点的角度值
    for i in [-1, 0, 1]:
        angleList.append(
            (angleMoonConst * moonCycle +
             ((dateDelta.days + i) % moonCycle)) % moonCycle / moonCycle * 360)
    if angleList[1] - angleList[0] < 0 and 360 - angleList[0] >= angleList[1]:
        angleList[1] = 0
    elif angleList[2] - angleList[1] < 0 and 360 - angleList[1] <= angleList[2]:
        angleList[1] = 0
    elif angleList[1] >= 180 and angleList[
            0] <= 180 and angleList[1] - 180 < 180 - angleList[0]:
        angleList[1] = 180
    elif angleList[2] >= 180 and angleList[
            1] <= 180 and angleList[2] - 180 > 180 - angleList[1]:
        angleList[1] = 180
    return angleList[1]


def drawMoon(a, moon, r, day="", list=[], c=0):
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
    if a == 180: moon.color("yellow")
    moon.pensize(0)
    moon.hideturtle()
    moon.up()
    if list != []:
        moon.goto(list[1], list[0])
        moon.write(day, font=("Copperplate", 18, "bold"), align="center")
    if a == 0:
        moon.begin_fill()
        moon.fillcolor("#282C34")
        moon.circle(-r)
        moon.end_fill()
    else:
        if a > 180: a, c = 360 - a, 180
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
    moonScreen = turtle.TurtleScreen(moonCanvas)
    moonScreen.bgpic("starry.gif")
    moonScreen.screensize(300, 650)
    moonScreen.tracer(n=0, delay=0)
    moon = turtle.RawTurtle(moonScreen)
    drawMoon(a, moon, r=100, list=[100, -20])


def moonCalendar(year, month):
    """在画布上绘制整月月相图"""
    moonCalendarScreen = turtle.TurtleScreen(moonCalendarCanvas)
    moonCalendarScreen.tracer(n=0, delay=0)
    moonCalendarScreen.bgpic("starry.gif")
    moonCalendarScreen.screensize(720, 650)
    moonCalendarScreen.setworldcoordinates(0, -650, 720, 0)
    moon = turtle.RawTurtle(moonCalendarScreen)
    # 绘制星期标签栏
    weekName = [
        "Monday", "Tuesday", "Wednesday", "Tuesday", "Friday", "Saturday",
        "Sunday"
    ]
    for column in range(7):
        moon.pencolor("white")
        moon.penup()
        moon.goto(x=column * 105 + 50, y=0)
        moon.pendown()
        moon.write(weekName[column],
                   font=("Copperplate", 18, "bold"),
                   align="center")
    # 绘制月亮
    for row, i in enumerate(calendar.monthcalendar(year, month)):
        for column in range(7):
            if i[column] != 0:
                drawMoon(
                    angleCalculate(year, month, i[column]),
                    moon,
                    day=i[column],
                    r=30,
                    list=[-row * 105 - 50, column * 105 + 50],
                )


def change():
    """获取当前年月日，并返回元组"""
    global dayList, chooseDay
    dayList = processDay(int(chooseYear.combobox.get()),
                         int(chooseMonth.combobox.get()))
    chooseDay.combobox["value"] = dayList
    if int(chooseDay.combobox.get()) not in dayList:
        chooseDay.var.set(chooseDay["value"][-1])
    return int(chooseYear.combobox.get()), int(chooseMonth.combobox.get()), int(
        chooseDay.combobox.get())


def changeMoon():
    """更改当天月相图"""
    tuple = change()
    moon(angleCalculate(tuple[0], tuple[1], tuple[2]))


def changeAll():
    """更改所有月相图"""
    tuple = change()
    moon(angleCalculate(tuple[0], tuple[1], tuple[2]))
    moonCalendar(tuple[0], tuple[1])


top = tkinter.Tk()
top.resizable(False, False)  # 设置窗体不可放缩
top.title("Lunar Phase Prediction")  # 窗体标题
top.configure(bg="#FDFFFB")  # 窗体颜色
top.iconphoto(False, tkinter.PhotoImage(file='icon.png'))  # 窗体图标

# 设置窗口初始位置在屏幕居中
winWidth, winHeight = 1080, 690  # 设置窗口大小
x = int((top.winfo_screenwidth() - winWidth) / 2)
y = int((top.winfo_screenheight() - winHeight) / 2)
top.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))

# 侧边栏
labalMain = tkinter.Label(top,
                          text="月\n相\n图\n预\n测",
                          bg="black",
                          fg="white",
                          font=("微软雅黑", 40))
labalMain.grid(row=1, column=0, sticky=tkinter.NSEW)

# 月相画布
moonCanvas = tkinter.Canvas(
    master=top,
    relief="groove",
    bg="black",
    width=300,
    height=650,
)
moonCanvas.grid(row=1, column=1)

# 整月月相图
moonCalendarCanvas = tkinter.Canvas(
    master=top,
    relief="groove",
    bg="black",
    width=720,
    height=650,
)
moonCalendarCanvas.grid(row=0, rowspan=2, column=2, sticky=tkinter.NSEW)

# 日期选择栏
dateframe = tkinter.LabelFrame(top, relief="groove")
dateframe.grid(row=0, column=0, columnspan=2, sticky=tkinter.NSEW)


class chooseDate:
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
chooseYear = chooseDate("Year", yearList, changeAll)
chooseYear.var.set(datetime.datetime.today().year)
chooseYear.labelframe.grid(row=0, column=0)
# 选择月份
chooseMonth = chooseDate("Month", monthList, changeAll)
chooseMonth.var.set(datetime.datetime.today().month)
chooseMonth.labelframe.grid(row=0, column=1)
# 选择日期
chooseDay = chooseDate("Day", dayList, changeMoon)
chooseDay.var.set(datetime.datetime.today().day)
chooseDay.labelframe.grid(row=0, column=2)

changeAll()  # 初始化界面

top.mainloop()
