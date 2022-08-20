import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QApplication

from datetime import datetime
import math
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.dates
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from data_output import data_suntime 

from UI_suntime import Ui_Suntime

css_button = """QPushButton{\
  background-color: rgba(255, 255, 255, 0);\
  border-style: outset;\
    border-width: 1px;\
    border-color:rgb(88, 88, 88);\
    border-right-color:rgb(213, 213, 213);\
    border-bottom-color:rgb(213, 213, 213)\
}
QPushButton:hover{
    background-color:rgba(88, 88, 88,100);\
    border-style: outset;\
    border-width: 2px;\
    border-color:rgb(88, 88, 88);\
    border-right-color:rgb(213, 213, 213);\
    border-bottom-color:rgb(213, 213, 213)\
}"""
css_press_button = """QPushButton{
    background-color:rgba(88, 88, 88,180);\
    color: rgb(239, 238, 238);\
    border-style: outset;\
    border-width: 2px;\
    border-color:rgb(88, 88, 88);\
    border-right-color:rgb(213, 213, 213);\
    border-bottom-color:rgb(213, 213, 213)\
}"""

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=6, height=4, dpi=100,type_1 = "2D"):
        fig = Figure(figsize=(width, height), dpi=dpi,facecolor='#EFEEEE')
        fig.tight_layout()
        if type_1 == "2D":
            fig.subplots_adjust(left=0.19, right=0.97, top=0.92, bottom=0.115)
            self.axes = fig.add_subplot(111)
        elif type_1 == "3D":
            fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
            self.axes = fig.add_subplot(111,projection='3d')
        super(MplCanvas, self).__init__(fig)


class Suntime(QWidget):
    def __init__(self,start, end, lat, lon,index):
        super().__init__()
        self.Ui_Suntime = Ui_Suntime()
        self.Ui_Suntime.setupUi(self)
        self.title = "Suntime"
        self.setWindowTitle(self.title)
        self.showMaximized()
        self.data_sun = data_suntime(start, end, lat, lon,index).data_sun
        self.set_zeta_all()
        self.set_3D(0)
        self.set_2D(0)
        self.widget_day_2D.show()
        self.widget_day_3D.show()
        self.set_year(start["year"],end["year"],start["month"],end["month"],start["day"],end["day"])

    def set_zeta_all(self):
        x_values = []
        y_values = []
        y_Ox = []

        for x in self.data_sun:
            for i in x:
                x_values.append(datetime(i["year"],i["month"],i["day"],i["hour"],i["minute"]))
                y_values.append(math.sin(math.radians(i["al_s"])))
                y_Ox.append(0)
        dates = matplotlib.dates.date2num(x_values)
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot_date(dates, y_values,'b-')
        sc.axes.plot_date(dates, y_Ox,'b-',color="black")
        sc.axes.axis([dates[0],dates[-1], -1, 1])
        sc.axes.grid("TRUE")
        sc.axes.set_facecolor("#EFEEEE")

        toolbar = NavigationToolbar(sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)
        
        self.Ui_Suntime.zeta_all.setLayout(layout)
        

    def set_3D(self,day):
        x1 = []
        y1 = []
        z1 = []
        x2 = []
        y2 = []
        z2 = []
        for i in self.data_sun[day]:
            if math.sin(math.radians(i["al_s"]))>=0:
                x1.append(math.cos(math.radians(i["al_s"]))*math.cos(math.radians(i["az_s"])))
                y1.append(math.cos(math.radians(i["al_s"]))*math.sin(math.radians(i["az_s"])))
                z1.append(math.sin(math.radians(i["al_s"])))
            else:
                x2.append(math.cos(math.radians(i["al_s"]))*math.cos(math.radians(i["az_s"])))
                y2.append(math.cos(math.radians(i["al_s"]))*math.sin(math.radians(i["az_s"])))
                z2.append(math.sin(math.radians(i["al_s"])))
        xx = np.linspace(-1, 1, 100)
        yy = np.linspace(-1, 1, 100)
        xx, yy = np.meshgrid(xx, yy)
        zz = 0*xx+0*yy

        ax = MplCanvas(self, width=10, height=4, dpi=100,type_1="3D")
        ax.axes.set_xlabel('S(-)-N(+)')
        ax.axes.set_ylabel('E(+)-W(-)')
        ax.axes.invert_yaxis()
        ax.axes.set_zlabel('z');
        ax.axes.scatter(x1,y1,z1)
        ax.axes.scatter(x2,y2,z2,color = 'r')
        ax.axes.plot_surface(xx,yy,zz,color='#58585840')
        ax.axes.scatter(0,0,0)
        ax.axes.view_init(elev=20, azim=160)
        #toolbar = NavigationToolbar(ax, self)
        layout = QtWidgets.QVBoxLayout()
        #layout.addWidget(toolbar)
        layout.addWidget(ax)
        self.widget_day_3D = QtWidgets.QWidget(self.Ui_Suntime.widget_3D)
        self.widget_day_3D.setGeometry(QtCore.QRect(0, 0, 521, 391))
        self.widget_day_3D.setObjectName("widget_day{}_3D".format(day))
        self.widget_day_3D.setLayout(layout)

    def set_2D(self,day):
        find_sunrise = 0
        find_sunset = 0
        find_sunmax = 0
        x1 = []
        y1 = []
        x2 = []
        y2 = []
        for i in range(len(self.data_sun[day])):
            if math.sin(math.radians(self.data_sun[day][i]["al_s"]))>=0:
                x1.append(math.cos(math.radians(self.data_sun[day][i]["al_s"]))*math.cos(math.radians(self.data_sun[day][i]["az_s"])))
                y1.append(math.cos(math.radians(self.data_sun[day][i]["al_s"]))*math.sin(math.radians(self.data_sun[day][i]["az_s"])))
                if i < len(self.data_sun[day])-1:
                    if  math.sin(math.radians(self.data_sun[day][i+1]["al_s"])) < 0 and find_sunset == 0 :
                        self.sunset = {"hour":self.data_sun[day][i]["hour"],"minute":self.data_sun[day][i]["minute"]}
                        find_sunset = 1
                    if  math.sin(math.radians(self.data_sun[day][i+1]["al_s"])) < math.sin(math.radians(self.data_sun[day][i]["al_s"])) and find_sunmax==0 :
                        self.sunmax = {"hour":self.data_sun[day][i]["hour"],"minute":self.data_sun[day][i]["minute"],"N":round(math.cos(math.radians(self.data_sun[day][i]["al_s"]))*math.cos(math.radians(self.data_sun[day][i]["az_s"])),2)\
                        ,"E":round(math.cos(math.radians(self.data_sun[day][i]["al_s"]))*math.sin(math.radians(self.data_sun[day][i]["az_s"])),2)}
                        find_sunmax = 1
            else:
                x2.append(math.cos(math.radians(self.data_sun[day][i]["al_s"]))*math.cos(math.radians(self.data_sun[day][i]["az_s"])))
                y2.append(math.cos(math.radians(self.data_sun[day][i]["al_s"]))*math.sin(math.radians(self.data_sun[day][i]["az_s"])))
                if i < len(self.data_sun[day])-1:
                    if math.sin(math.radians(self.data_sun[day][i+1]["al_s"])) > 0 and find_sunrise == 0 :
                        self.sunrise = {"hour":self.data_sun[day][i]["hour"],"minute":self.data_sun[day][i]["minute"]}
                        find_sunrise = 1

        if find_sunmax == 0:
            if math.sin(math.radians(self.data_sun[day][0]["al_s"]))>0:
                self.sunmax = {"hour":self.data_sun[day][0]["hour"],"minute":self.data_sun[day][0]["minute"],"N":x1[0],"E":x1[0]}
            else:
                self.sunmax = {"hour":"un","minute":"un","N":"un","E":"un"}

        if find_sunrise == 0:
            self.sunrise = {"hour":"un","minute":"un","N":"un","E":"un"}
        else:
            self.sunrise["N"] = round(x1[0],2)
            self.sunrise["E"] = round(y1[0],2)
        if find_sunset == 0:
            self.sunset = {"hour":"un","minute":"un","N":"un","E":"un"}
        else:
            self.sunset["N"] = round(x1[-1],2)
            self.sunset["E"] = round(y1[-1],2)

        ax = MplCanvas(self, width=1, height=1, dpi=100,type_1="2D")
        ax.axes.set_xlabel('N(+)-S(-)')
        ax.axes.set_ylabel('E(+)-W(-)')
        ax.axes.plot(x1,y1)
        ax.axes.plot(x2,y2,color = 'r')
        ax.axes.scatter(0,0)
        ax.axes.scatter(self.sunmax["N"],self.sunmax["E"])
        ax.axes.axis([-1,1,-1,1])
        ax.axes.grid("TRUE")
        ax.axes.set_facecolor("#EFEEEE")
        #tight_layout()
        #toolbar = NavigationToolbar(ax, self)
        layout = QtWidgets.QVBoxLayout()
        #layout.addWidget(toolbar)
        layout.addWidget(ax)
        self.widget_day_2D = QtWidgets.QWidget(self.Ui_Suntime.widget_2D)
        self.widget_day_2D.setGeometry(QtCore.QRect(0, 0,  401, 391))
        self.widget_day_2D.setObjectName("widget_day{}_2D".format(day))
        self.widget_day_2D.setLayout(layout)

        self.Ui_Suntime.label_data.setText("Sunrise:\n{}:{}\nN{} E{}\n\nSunset:\n{}:{}\nN{} E{}\n\nSunmax:\n{}:{}\nN{} E{}".\
            format(self.sunrise["hour"],self.sunrise["minute"],self.sunrise["N"],self.sunrise["E"],self.sunset["hour"],\
                self.sunset["minute"],self.sunset["N"],self.sunset["E"],self.sunmax["hour"],self.sunmax["minute"],self.sunmax["N"],self.sunmax["E"]))



    def set_year(self,year_start,year_end,month_start,month_end,day_start,day_end):
        def set_button(widget,x,y,year = None,month = None, day = None,type_1 = "year"):
            button = QtWidgets.QPushButton(widget)
            if type_1 == "year":
                button.setGeometry(x,y,91, 28)
                button.setObjectName("button_year_{}".format(year))
                button.clicked.connect(lambda ch, year=year: self.function_year(year))
                button.setText(str(year))
                button.show()
            elif type_1 == "month":
                button.setGeometry(x,y,91, 28)
                button.setObjectName("button_month_{}_of_year_{}".format(month,year))
                button.clicked.connect(lambda ch, year=year: self.function_month(year,month))
                button.setText(str(month))
            if type_1 == "day":
                button.setGeometry(x,y,41, 41)
                button.setObjectName("button_d_{}_of_m_{}_of_y_{}".format(day,month,year))
                button.clicked.connect(lambda ch, year=year: self.function_day(year,month,day,year_start,month_start,day_start))
                button.setText(str(day))
            button.setStyleSheet(css_button)
            font = QtGui.QFont()
            font.setPointSize(12)
            button.setFont(font)

        def number_day(year,month):
            if month == 1 or month ==3 or month ==5 or month ==7 or month ==8 or month ==10 or month == 12:
                return 31
            elif month == 4 or month ==6 or month ==9 or month ==11:
                return 30
            else:
                if year % 4 == 0 and year % 100 != 0:
                    return 29
                else:
                    return 28
        
        count_year = year_start
        y_year = 10

        while count_year <= year_end:
            y_month = 10
            set_button(self.Ui_Suntime.widget_year,10,y_year,year=count_year,type_1 = "year")
            self.widget_of_year = QtWidgets.QWidget(self.Ui_Suntime.widget_month)
            self.widget_of_year.setGeometry(QtCore.QRect(0, 0, 111, 411))
            self.widget_of_year.setObjectName("widget_of_year{}".format(count_year))
            if count_year == year_start:
                y_month = y_month + 33*(month_start-1)
                if month_start == month_end and year_end == year_start:
                    range_button = month_start + 1
                else:
                    range_button = 13
                for count_month in range(month_start,range_button):
                    set_button(self.widget_of_year,10,y_month,count_year,count_month,type_1 = "month")
                    y_month += 33
                    #set day
                    self.widget_month_of_year = QtWidgets.QWidget(self.Ui_Suntime.widget_day)
                    self.widget_month_of_year.setGeometry(QtCore.QRect(0, 0, 425, 410))
                    self.widget_month_of_year.setObjectName("widget_month{}_of_year{}".format(count_month,count_year))

                    if count_month == month_start:
                        if month_start == month_end and year_end == year_start:
                            range_button = day_end + 1
                        else:
                            range_button = number_day(count_year,count_month) + 1
                        date_value = datetime(count_year,count_month,day_start).date()
                        week = date_value.weekday()
                        week_of_month = date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1] + 1
                        x_day = 22 + week*57
                        y_day = -35 + week_of_month*65
                        print(week_of_month)
                        week+=1
                        
                        for count_day in range(day_start,range_button):
                            set_button(self.widget_month_of_year,x_day,y_day,count_year,count_month,count_day,type_1 = "day")
                            if week == 7:
                                week = 0
                                y_day += 65
                                x_day = -35
                            x_day += 57
                            week+=1
                    else:
                        week = datetime(count_year,count_month,1).weekday()
                        x_day = 22 + week*57
                        y_day = 25
                        week+=1
                        for count_day in range(1,number_day(count_year,count_month) + 1):
                            set_button(self.widget_month_of_year,x_day,y_day,count_year,count_month,count_day,type_1 = "day")
                            if week == 7:
                                week = 0
                                y_day += 65
                                x_day = -35
                            x_day += 57
                            week+=1

            elif count_year == year_end:
                for count_month in range(1,month_end+1):
                    set_button(self.widget_of_year,10,y_month,count_year,count_month,type_1 = "month")
                    y_month += 33
                    #set day
                    self.widget_month_of_year = QtWidgets.QWidget(self.Ui_Suntime.widget_day)
                    self.widget_month_of_year.setGeometry(QtCore.QRect(0, 0, 425, 410))
                    self.widget_month_of_year.setObjectName("widget_month{}_of_year{}".format(count_month,count_year))
                    week = datetime(count_year,count_month,1).weekday()
                    x_day = 22 + week*57
                    y_day = 25
                    week+=1
                    if count_month == month_end:
                        
                        for count_day in range(1,day_end):
                            set_button(self.widget_month_of_year,x_day,y_day,count_year,count_month,count_day,type_1 = "day")
                            if week == 7:
                                week = 0
                                y_day += 65
                                x_day = -35
                            x_day += 57
                            week+=1
                    else:
                        for count_day in range(1,number_day(count_year,count_month) + 1):
                            set_button(self.widget_month_of_year,x_day,y_day,count_year,count_month,count_day,type_1 = "day")
                            if week == 7:
                                week = 0
                                y_day += 65
                                x_day = -35
                            x_day += 57
                            week+=1
                    
            else:
                for count_month in range(1,13):
                    set_button(self.widget_of_year,10,y_month,count_year,count_month,type_1 = "month")
                    y_month += 33
                    #set day
                    self.widget_month_of_year = QtWidgets.QWidget(self.Ui_Suntime.widget_day)
                    self.widget_month_of_year.setGeometry(QtCore.QRect(0, 0, 425, 410))
                    self.widget_month_of_year.setObjectName("widget_month{}_of_year{}".format(count_month,count_year))
                    week = datetime(count_year,count_month,1).weekday()
                    x_day = 22 + week*57
                    y_day = 25
                    week+=1
                    for count_day in range(1,number_day(count_year,count_month) + 1):
                        set_button(self.widget_month_of_year,x_day,y_day,count_year,count_month,count_day,type_1 = "day")
                        if week == 7:
                            week = 0
                            y_day += 65
                            x_day = -35
                        x_day += 57
                        week+=1
                    
            y_year+= 33
            count_year+=1

        self.widget_of_year = self.findChild(QWidget, "widget_of_year{}".format(year_start))
        self.widget_of_year.show()
        self.widget_month_of_year = self.findChild(QWidget, "widget_month{}_of_year{}".format(month_start,year_start))
        self.widget_month_of_year.show()
        self.press_button_year = self.findChild(QtWidgets.QPushButton,"button_year_{}".format(year_start))
        self.press_button_year.setStyleSheet(css_press_button)
        self.press_button_month_of_year = self.findChild(QtWidgets.QPushButton,"button_month_{}_of_year_{}".format(month_start,year_start))
        self.press_button_month_of_year.setStyleSheet(css_press_button)
        self.press_button_d_of_m_of_y = self.findChild(QtWidgets.QPushButton,"button_d_{}_of_m_{}_of_y_{}".format(day_start,month_start,year_start))
        self.press_button_d_of_m_of_y.setStyleSheet(css_press_button)
           
    def function_year(self, year):
        self.widget_of_year.hide()
        self.widget_of_year = self.findChild(QWidget, "widget_of_year{}".format(year))
        self.widget_of_year.show()
        self.press_button_year.setStyleSheet(css_button)
        self.press_button_year = self.findChild(QtWidgets.QPushButton,"button_year_{}".format(year))
        self.press_button_year.setStyleSheet(css_press_button)

    def function_month(self,year,month):
        self.widget_month_of_year.hide()
        self.widget_month_of_year = self.findChild(QWidget, "widget_month{}_of_year{}".format(month,year))
        self.widget_month_of_year.show()
        self.press_button_month_of_year.setStyleSheet(css_button)
        self.press_button_month_of_year = self.findChild(QtWidgets.QPushButton,"button_month_{}_of_year_{}".format(month,year))
        self.press_button_month_of_year.setStyleSheet(css_press_button)

    def function_day(self,year,month,day,year_start,month_start,day_start):
        n = (datetime(year,month,day).date() - datetime(year_start,month_start,day_start).date()).days
        self.widget_day_2D.hide()
        self.widget_day_3D.hide()
        self.set_3D(n)
        self.set_2D(n)
        self.widget_day_2D.show()
        self.widget_day_3D.show()
        self.press_button_d_of_m_of_y.setStyleSheet(css_button)
        self.press_button_d_of_m_of_y = self.findChild(QtWidgets.QPushButton,"button_d_{}_of_m_{}_of_y_{}".format(day,month,year))
        self.press_button_d_of_m_of_y.setStyleSheet(css_press_button)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Suntime({ "year": 2022, "month": 1, "day": 1, "hour": 0, "minute": 0, "second": 0 }, { "year": 2022, "month": 12, "day": 31, "hour": 23, "minute": 59, "second": 59}, -26.75, 133.25,5)
    window.show()
    sys.exit(app.exec_()) 


