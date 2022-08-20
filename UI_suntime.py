# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sun_time.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Suntime(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1927, 1011)
        self.zeta_all = QtWidgets.QWidget(Form)
        self.zeta_all.setGeometry(QtCore.QRect(40, 40, 1840, 500))
        self.zeta_all.setStyleSheet("background-color: rgb(239, 238, 238);border: 3px solid;border-color: rgb(88, 88, 88);")
        self.zeta_all.setObjectName("zeta_all")
        self.widget_month = QtWidgets.QWidget(Form)
        self.widget_month.setGeometry(QtCore.QRect(170, 560, 111, 411))
        self.widget_month.setStyleSheet("#widget_month{background-color: rgb(239, 238, 238);border: 3px solid;border-color: rgb(88, 88, 88);}")
        self.widget_month.setObjectName("widget_month")
        self.widget_day = QtWidgets.QWidget(Form)
        self.widget_day.setGeometry(QtCore.QRect(300, 560, 425, 410))
        self.widget_day.setStyleSheet("background-color: rgb(239, 238, 238);border: 3px solid;border-color: rgb(88, 88, 88);")
        self.widget_day.setObjectName("widget_day")
        self.widget_year = QtWidgets.QWidget(Form)
        self.widget_year.setGeometry(QtCore.QRect(40, 560, 111, 411))
        self.widget_year.setStyleSheet("#widget_year{background-color: rgb(239, 238, 238);border: 3px solid;border-color: rgb(88, 88, 88);}")
        self.widget_year.setObjectName("widget_year")
        self.widget_3D = QtWidgets.QWidget(Form)
        self.widget_3D.setGeometry(QtCore.QRect(750, 560, 521, 391))
        self.widget_3D.setStyleSheet("background-color: rgb(239, 238, 238);border: 3px solid;border-color: rgb(88, 88, 88);")
        self.widget_3D.setObjectName("widget_3D")
        self.widget_2D = QtWidgets.QWidget(Form)
        self.widget_2D.setGeometry(QtCore.QRect(1290, 560, 401, 391))
        self.widget_2D.setStyleSheet("background-color: rgb(239, 238, 238);border: 3px solid;border-color: rgb(88, 88, 88);")
        self.widget_2D.setObjectName("widget_2D")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(1000, 950, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(1470, 950, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(960, 5, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_data = QtWidgets.QLabel(Form)
        self.label_data.setGeometry(QtCore.QRect(1720, 560, 141, 411))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_data.setFont(font)
        self.label_data.setObjectName("label_data")
        self.label_data.setAlignment(QtCore.Qt.AlignCenter)
        self.label_monday = QtWidgets.QLabel(Form)
        self.label_monday.setGeometry(QtCore.QRect(322, 965, 241, 31))
        self.label_monday.setFont(font)
        self.label_monday.setObjectName("label_monday")
        self.label_tuesday = QtWidgets.QLabel(Form)
        self.label_tuesday.setGeometry(QtCore.QRect(379, 965, 241, 31))
        self.label_tuesday.setFont(font)
        self.label_tuesday.setObjectName("label_tuesday")
        self.label_wednesday = QtWidgets.QLabel(Form)
        self.label_wednesday.setGeometry(QtCore.QRect(436, 965, 241, 31))
        self.label_wednesday.setFont(font)
        self.label_wednesday.setObjectName("label_wednesday")
        self.label_thursday = QtWidgets.QLabel(Form)
        self.label_thursday.setGeometry(QtCore.QRect(493, 965, 241, 31))
        self.label_thursday.setFont(font)
        self.label_thursday.setObjectName("label_thursday")
        self.label_friday = QtWidgets.QLabel(Form)
        self.label_friday.setGeometry(QtCore.QRect(550, 965, 241, 31))
        self.label_friday.setFont(font)
        self.label_friday.setObjectName("label_friday")
        self.label_saturday = QtWidgets.QLabel(Form)
        self.label_saturday.setGeometry(QtCore.QRect(607, 965, 241, 31))
        self.label_saturday.setFont(font)
        self.label_saturday.setObjectName("label_saturday") 
        self.label_sunday = QtWidgets.QLabel(Form)
        self.label_sunday.setGeometry(QtCore.QRect(664, 965, 241, 31))
        self.label_sunday.setFont(font)
        self.label_sunday.setObjectName("label_sunday") 

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "3D"))
        self.label_2.setText(_translate("Form", "2D"))
        self.label_3.setText(_translate("Form", "ALL time"))
        self.label_monday.setText(_translate("Form", "Mon"))
        self.label_tuesday.setText(_translate("Form", "Tue"))
        self.label_wednesday.setText(_translate("Form", "Wed"))
        self.label_thursday.setText(_translate("Form", " Thu"))
        self.label_friday.setText(_translate("Form", "  Fri"))
        self.label_saturday.setText(_translate("Form", " Sat"))
        self.label_sunday.setText(_translate("Form", "Sun"))
        self.label_data.setText(_translate("Form", "Sunrise:\n12:30\nN12aS14\n\nSunset:\n12:30\nN1 S2\n\nSunmax:\n12:30\nN12 S12"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Suntime()
    ui.setupUi(Form)
    Form.showMaximized()
    Form.show()
    sys.exit(app.exec_())
