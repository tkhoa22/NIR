import sys
import os
import json

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import matplotlib.pyplot as plt

from UI_input import Ui_Input
from suntime import Suntime

from mathsun import *
from mathgraphic import *

from data_output import *



#56.49771, 84.97437,5
class Input(QWidget):
    def __init__(self,parent = None):
        super().__init__(parent)
        self.setFixedSize(740,680)
        self.ui_input = Ui_Input()
        self.ui_input.setupUi(self)
        self.title = "Goodname"
        self.setWindowTitle(self.title)

        self.data = []
        #
        self.count_run = 0
        self.ui_input.run.clicked.connect(lambda:self.run_simulator())
        #save
        self.ui_input.Button_Save.clicked.connect(lambda:self.save())
        self.shortcut_save = QShortcut(QKeySequence('Ctrl+S'), self)
        self.shortcut_save.activated.connect(self.save)
        #
        self.ui_input.Button_Open.clicked.connect(lambda:self.open())
        self.shortcut_open = QShortcut(QKeySequence('Ctrl+O'), self)
        self.shortcut_open.activated.connect(self.open)
        #new
        self.ui_input.Button_New.clicked.connect(lambda:self.new())
        self.shortcut_new = QShortcut(QKeySequence('Ctrl+N'), self)
        self.shortcut_new.activated.connect(self.new)
        #
        self.ui_input.run_sun.clicked.connect(lambda:self.run_sun())
        self.shortcut_run_sun = QShortcut(QKeySequence('Ctrl+Y'), self)
        self.shortcut_run_sun.activated.connect(self.run_sun)
        #PV panel
        self.count_PV = 0
        self.check_prev_PV = 0 # 1: when use click button, 0: never click buton, because when clcik buton 1 times so count_PV = count_PV-1
        self.check_next_PV = 0 # 1: add element in dât_PV, 0 : not add
        self.data_PV = []
        self.ui_input.PrevPV.clicked.connect(lambda:self.PrevPV())
        self.ui_input.NextPV.clicked.connect(lambda:self.NextPV())
        self.ui_input.GoPV.clicked.connect(lambda:self.GoPV())
        self.ui_input.UpdatePV.clicked.connect(lambda:self.UpdatePV())

        #Mirror
        self.count_Mirror= 0
        self.check_prev_Mirror= 0 # 1: when use click button, 0: never click buton, because when clcik buton 1 times so count_mirror= count_Mirror-1
        self.check_next_Mirror= 0 # 1: add element in dât_Mirror, 0 : not add
        self.data_Mirror= []
        self.ui_input.PrevMirror.clicked.connect(lambda:self.PrevMirror())
        self.ui_input.NextMirror.clicked.connect(lambda:self.NextMirror())
        self.ui_input.GoMirror.clicked.connect(lambda:self.GoMirror())
        self.ui_input.UpdateMirror.clicked.connect(lambda:self.UpdateMirror())

    def run_sun(self):
        if self.ui_input.start.text() and self.ui_input.end.text() and self.ui_input.lon.text() and self.ui_input.lat.text():
            date_start = self.ui_input.start.date()
            time_start = self.ui_input.start.time()
            date_end = self.ui_input.end.date()
            time_end = self.ui_input.end.time()
            if self.ui_input.index.text():
                index = int(self.ui_input.index.text())/60
            else:
                index = 5
            self.Ui_Suntime = Suntime({"year":date_start.year(),"month":date_start.month(),"day":date_start.day(),
            "hour":time_start.hour(),"minute":time_start.minute(),"second":time_start.second()},{"year":date_end.year(),"month":date_end.month(),"day":date_end.day(),
            "hour":time_end.hour(),"minute":time_end.minute(),"second":time_end.second()},float(self.ui_input.lat.text()),float(self.ui_input.lon.text()),index)
            self.title = "Suntime"
            self.Ui_Suntime.setWindowTitle(self.title)
            self.Ui_Suntime.showMaximized()

    def run_simulator(self):
        def on_close(event):
            print('Closed Figure!')
            self.count_run = 0
        if self.count_run == 0:
            self.count_run = 1
            fig = plt.figure(figsize=(4,4))
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(2,3,4) # plot the point (2,3,4) on the figure
            fig.canvas.mpl_connect('close_event', on_close)
            plt.show()
        else:
            print("dm thg loz nay cái kia đang chạy bật thêm ăn loz hả????")

    def new(self):
        self.count_PV = 0
        self.check_prev_PV = 0 
        self.check_next_PV = 0 
        self.data_PV = []
        self.count_Mirror= 0
        self.check_prev_Mirror= 0 
        self.check_next_Mirror= 0 
        self.data_Mirror= []
        self.ui_input.start.setDateTime(QtCore.QDateTime(2000,1,1,0,0,0))
        self.ui_input.end.setDateTime(QtCore.QDateTime(2000,1,1,0,0,0))
        self.data = []
        self.count_run = 0
        self.ui_input.lat.clear()
        self.ui_input.lon.clear()
        self.ui_input.Irradiance.clear()
        self.ui_input.x_Mirror.clear()
        self.ui_input.y_Mirror.clear()
        self.ui_input.z_Mirror.clear()
        self.ui_input.weight_Mirror.clear()
        self.ui_input.height_Mirror.clear() 
        self.ui_input.azimuth_Mirror.clear()
        self.ui_input.altitude_Mirror.clear()
        self.ui_input.label_18.setText("1/1")
        self.ui_input.x_PV.clear()
        self.ui_input.y_PV.clear()
        self.ui_input.z_PV.clear()
        self.ui_input.weight_PV.clear()
        self.ui_input.height_PV.clear()
        self.ui_input.azimuth_PV.clear()
        self.ui_input.altitude_PV.clear()
        self.ui_input.label_11.clear()

    def save(self):
        self.NextPV()
        self.NextMirror()
        def filter_data(data):
            #xóa các thành phần có weight or height = 0:
            a = 0
            i = 0
            while i < len(data):
                if data[i]["w"] == "0" or data[i]["h"] == "0":
                    data.pop(i)
                    a+=1
                if i !=len(data):
                    data[i]["index"] -= a
                i+=1
            return data
        if len(self.data_PV) > 0 and len(self.data_Mirror)> 0 and self.ui_input.lat.text() and self.ui_input.lon.text() and self.ui_input.Irradiance.text():
            date_start = self.ui_input.start.date()
            time_start = self.ui_input.start.time()
            date_end = self.ui_input.end.date()
            time_end = self.ui_input.end.time()
            
            self.data_PV = filter_data(self.data_PV)
            self.data_Mirror = filter_data(self.data_Mirror)

            save_data = {"PV":self.data_PV,
            "Mirror":self.data_Mirror,
            "location":{"lat":self.ui_input.lat.text(),"lon":self.ui_input.lon.text()},
            "time":{"start":
            {"year":date_start.year(),"month":date_start.month(),"day":date_start.day(),
            "hour":time_start.hour(),"minute":time_start.minute(),"second":time_start.second()},
            "end":{"year":date_end.year(),"month":date_end.month(),"day":date_end.day(),
            "hour":time_end.hour(),"minute":time_end.minute(),"second":time_end.second()}},
            "Irradiance":self.ui_input.Irradiance.text()
            }
            if self.title == "Goodname":    
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog
                fileName, _ = QFileDialog.getSaveFileName(
                    parent = self,
                    caption = "Save file",
                    directory = "vd.json",
                    filter = "All Files (*);;Json Files (*.json)", 
                    options=options)
                if fileName:
                    with open(fileName, 'w') as f:
                        json.dump(save_data ,f, ensure_ascii=False, indent=4)
                        self.setWindowTitle(str(os.path.basename(fileName)) + " - Notepad Alpha[*]")
            else:
                with open(self.title, 'w') as f:
                    json.dump(save_data ,f, ensure_ascii=False, indent=4)


    def open(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        self.title = fileName
        if fileName:
            with open(fileName, 'r') as openfile:
                json_object = json.load(openfile)
                openfile.close()
                print(json_object)
                self.setWindowTitle(fileName)
                self.data_PV = json_object["PV"]
                self.ui_input.x_PV.setText(json_object["PV"][0]["x"])
                self.ui_input.y_PV.setText(json_object["PV"][0]["y"])
                self.ui_input.z_PV.setText(json_object["PV"][0]["y"])
                self.ui_input.zB_zA_PV.setText(json_object["PV"][0]["zB_zA"])
                self.ui_input.weight_PV.setText(json_object["PV"][0]["w"])
                self.ui_input.height_PV.setText(json_object["PV"][0]["h"]) 
                self.ui_input.azimuth_PV.setText(json_object["PV"][0]["az"]) 
                self.ui_input.altitude_PV.setText(json_object["PV"][0]["al"])
                self.ui_input.label_11.setText("1/"+str(len(json_object["PV"])))
                self.count_PV = 0
                self.check_prev_PV = 1
                self.check_next_PV = 1 

                self.data_Mirror = json_object["Mirror"]
                self.ui_input.x_Mirror.setText(json_object["Mirror"][0]["x"])
                self.ui_input.y_Mirror.setText(json_object["Mirror"][0]["y"])
                self.ui_input.z_Mirror.setText(json_object["Mirror"][0]["y"])
                self.ui_input.zB_zA_Mirror.setText(json_object["PV"][0]["zB_zA"])
                self.ui_input.weight_Mirror.setText(json_object["Mirror"][0]["w"])
                self.ui_input.height_Mirror.setText(json_object["Mirror"][0]["h"]) 
                self.ui_input.azimuth_Mirror.setText(json_object["Mirror"][0]["az"]) 
                self.ui_input.altitude_Mirror.setText(json_object["Mirror"][0]["al"])
                self.ui_input.label_18.setText("1/"+str(len(json_object["Mirror"])))
                self.count_Mirror = 0
                self.check_prev_Mirror = 1 
                self.check_next_Mirror = 1
                
                self.ui_input.lat.setText(json_object["location"]["lat"])
                self.ui_input.lon.setText(json_object["location"]["lon"])
                self.ui_input.Irradiance.setText(json_object["Irradiance"])

                self.ui_input.start.setDateTime(QtCore.QDateTime(json_object["time"]["start"]["year"],json_object["time"]["start"]["month"],json_object["time"]["start"]["day"],\
                    json_object["time"]["start"]["hour"],json_object["time"]["start"]["minute"],json_object["time"]["start"]["second"]))
                self.ui_input.end.setDateTime(QtCore.QDateTime(json_object["time"]["end"]["year"],json_object["time"]["end"]["month"],json_object["time"]["end"]["day"],\
                    json_object["time"]["end"]["hour"],json_object["time"]["end"]["minute"],json_object["time"]["end"]["second"]))

    def PrevPV(self):
        if len(self.data_PV) == 0:
            self.check_prev_PV = 0
        else:
            self.check_prev_PV = 1
            self.check_next_PV = 1
        if self.count_PV >= self.check_prev_PV:
            data_prePV = self.data_PV[self.count_PV - 1]
            self.count_PV -= 1
            self.ui_input.x_PV.setText(str(data_prePV["x"]))
            self.ui_input.y_PV.setText(str(data_prePV["y"]))
            self.ui_input.z_PV.setText(str(data_prePV["z"]))
            self.ui_input.zB_zA_PV.setText(str(data_prePV["zB_zA"]))
            self.ui_input.weight_PV.setText(str(data_prePV["w"]))
            self.ui_input.height_PV.setText(str(data_prePV["h"])) 
            self.ui_input.azimuth_PV.setText(str(data_prePV["az"])) 
            self.ui_input.altitude_PV.setText(str(data_prePV["al"]))
            self.ui_input.label_11.setText(str(data_prePV["index"]) + "/" + str(len(self.data_PV)))


    def NextPV(self):
        if self.count_PV == len(self.data_PV) - self.check_prev_PV:   
            if self.ui_input.x_PV.text() and self.ui_input.y_PV.text() and self.ui_input.z_PV.text() and self.ui_input.weight_PV.text()\
            and self.ui_input.height_PV.text() and self.ui_input.azimuth_PV.text() and self.ui_input.altitude_PV.text():
                if self.check_next_PV == 0:
                    data_nextPV = {"type" : "PV", 
                        "x": float(self.ui_input.x_PV.text()), 
                        "y": float(self.ui_input.y_PV.text()), 
                        "z":  float(self.ui_input.z_PV.text()),
                        "zB_zA": float(self.ui_input.zB_zA_PV.text()),
                        "w": float(self.ui_input.weight_PV.text()), 
                        "h": float(self.ui_input.height_PV.text()),
                        "az": float(self.ui_input.azimuth_PV.text()),
                        "al": float(self.ui_input.altitude_PV.text()),
                        "index": self.count_PV+self.check_prev_PV+1}
                    self.data_PV.append(data_nextPV)
                    self.count_PV += 1
                elif self.check_next_PV == 1:
                    self.check_next_PV = 0
                    if self.check_prev_PV == 1:
                        self.count_PV+=1
                        self.check_prev_PV = 0

                self.ui_input.x_PV.clear()
                self.ui_input.y_PV.clear()
                self.ui_input.z_PV.clear()
                self.ui_input.weight_PV.clear()
                self.ui_input.height_PV.clear() 
                self.ui_input.azimuth_PV.clear() 
                self.ui_input.altitude_PV.clear()
                self.ui_input.label_11.setText(str(self.count_PV+self.check_prev_PV+1) + "/" + str(len(self.data_PV)))
        else:
            if len(self.data_PV) != 0 :
                self.count_PV += 1

                data_nextPV = self.data_PV[self.count_PV]
                self.ui_input.x_PV.setText(str(data_nextPV["x"]))
                self.ui_input.y_PV.setText(str(data_nextPV["y"]))
                self.ui_input.z_PV.setText(str(data_nextPV["z"]))
                self.ui_input.zB_zA_PV.setText(str(data_nextPV["zB_zA"]))
                self.ui_input.weight_PV.setText(str(data_nextPV["w"]))
                self.ui_input.height_PV.setText(str(data_nextPV["h"]))
                self.ui_input.azimuth_PV.setText(str(data_nextPV["az"]))
                self.ui_input.altitude_PV.setText(str(data_nextPV["al"]))
                self.ui_input.label_11.setText(str(data_nextPV["index"]) + "/" + str(len(self.data_PV)))

        print(self.count_PV)
        print(self.check_prev_PV)
        print(self.check_next_PV)
        print("-----------------------------")
        
    def UpdatePV(self):
        if self.ui_input.x_PV.text() and self.ui_input.y_PV.text() and self.ui_input.z_PV.text() and self.ui_input.weight_PV.text()\
        and self.ui_input.height_PV.text() and self.ui_input.azimuth_PV.text() and self.ui_input.altitude_PV.text():
            data_updatePV = {"type" : "PV", 
                "x": float(self.ui_input.x_PV.text()), 
                "y": float(self.ui_input.y_PV.text()), 
                "z":  float(self.ui_input.z_PV.text()),
                "zB_zA": float(self.ui_input.zB_zA_PV.text()),
                "w": float(self.ui_input.weight_PV.text()), 
                "h": float(self.ui_input.height_PV.text()),
                "az": float(self.ui_input.azimuth_PV.text()),
                "al": float(self.ui_input.altitude_PV.text()),
                "index": self.count_PV}
            self.data_PV[self.count_PV] = data_updatePV

    def GoPV(self):
        if self.ui_input.page_go_PV.text() and 0 < int(self.ui_input.page_go_PV.text()) <= len(self.data_PV):
            data_goPV = self.data_PV[int(self.ui_input.page_go_PV.text()) - 1]
            self.ui_input.x_PV.setText(str(data_goPV["x"]))
            self.ui_input.y_PV.setText(str(data_goPV["y"]))
            self.ui_input.z_PV.setText(str(data_goPV["z"]))
            self.ui_input.zB_zA_PV.setText(str(data_goPV["zB_zA"]))
            self.ui_input.weight_PV.setText(str(data_goPV["w"]))
            self.ui_input.height_PV.setText(str(data_goPV["h"])) 
            self.ui_input.azimuth_PV.setText(str(data_goPV["az"])) 
            self.ui_input.altitude_PV.setText(str(data_goPV["al"]))
            self.ui_input.label_11.setText(str(data_goPV["index"]) + "/" + str(len(self.data_PV)))
            
            self.count_PV = int(self.ui_input.page_go_PV.text()) - 1 - self.check_prev_PV
            self.check_prev_PV = 1
            self.check_next_PV = 1

    def PrevMirror(self):
        if len(self.data_Mirror) == 0:
            self.check_prev_Mirror = 0
        else:
            self.check_prev_Mirror = 1
            self.check_next_Mirror = 1
        if self.count_Mirror > 0:
            data_preMirror = self.data_Mirror[self.count_Mirror - 1]
            self.count_Mirror -= 1
            self.ui_input.x_Mirror.setText(str(data_preMirror["x"]))
            self.ui_input.y_Mirror.setText(str(data_preMirror["y"]))
            self.ui_input.z_Mirror.setText(str(data_preMirror["z"]))
            self.ui_input.zB_zA_Mirror.setText(str(data_preMirror["zB_zA"]))
            self.ui_input.weight_Mirror.setText(str(data_preMirror["w"]))
            self.ui_input.height_Mirror.setText(str(data_preMirror["h"]))
            self.ui_input.azimuth_Mirror.setText(str(data_preMirror["az"])) 
            self.ui_input.altitude_Mirror.setText(str(data_preMirror["al"]))
            self.ui_input.label_18.setText(str(data_preMirror["index"]) + "/" + str(len(self.data_Mirror)))

    def NextMirror(self):
        if self.count_Mirror == len(self.data_Mirror) - self.check_prev_Mirror:   
            if self.ui_input.x_Mirror.text() and self.ui_input.y_Mirror.text() and self.ui_input.z_Mirror.text() and self.ui_input.weight_Mirror.text()\
            and self.ui_input.height_Mirror.text() and self.ui_input.azimuth_Mirror.text() and self.ui_input.altitude_Mirror.text():
                if self.check_next_Mirror == 0:
                    data_nextMirror = {"type" : "Mirror", 
                        "x": float(self.ui_input.x_Mirror.text()), 
                        "y": float(self.ui_input.y_Mirror.text()), 
                        "z":  float(self.ui_input.z_Mirror.text()),
                        "zB_zA":  float(self.ui_input.zB_zA_Mirror.text()),
                        "w": float(self.ui_input.weight_Mirror.text()), 
                        "h": float(self.ui_input.height_Mirror.text()),
                        "az": float(self.ui_input.azimuth_Mirror.text()),
                        "al": float(self.ui_input.altitude_Mirror.text()),
                        "index": self.count_Mirror+self.check_prev_Mirror+1}
                    self.data_Mirror.append(data_nextMirror)
                    self.count_Mirror += 1
                elif self.check_next_Mirror == 1:
                    self.check_next_Mirror = 0
                    if self.check_prev_Mirror== 1:
                        self.count_Mirror+=1
                        self.check_prev_Mirror = 0

                self.ui_input.x_Mirror.clear()
                self.ui_input.y_Mirror.clear()
                self.ui_input.z_Mirror.clear()
                self.ui_input.weight_Mirror.clear()
                self.ui_input.height_Mirror.clear() 
                self.ui_input.azimuth_Mirror.clear() 
                self.ui_input.altitude_Mirror.clear()
                self.ui_input.label_18.setText(str(self.count_Mirror+self.check_prev_Mirror+1) + "/" + str(len(self.data_Mirror)))
        else:
            if len(self.data_Mirror) != 0:
                self.count_Mirror += 1
                data_nextMirror = self.data_Mirror[self.count_Mirror]
                self.ui_input.x_Mirror.setText(str(data_nextMirror["x"]))
                self.ui_input.y_Mirror.setText(str(data_nextMirror["y"]))
                self.ui_input.z_Mirror.setText(str(data_nextMirror["z"]))
                self.ui_input.zB_zA_Mirror.setText(str(data_nextMirror["zB_zA"]))
                self.ui_input.weight_Mirror.setText(str(data_nextMirror["w"]))
                self.ui_input.height_Mirror.setText(str(data_nextMirror["h"])) 
                self.ui_input.azimuth_Mirror.setText(str(data_nextMirror["az"])) 
                self.ui_input.altitude_Mirror.setText(str(data_nextMirror["al"]))
                self.ui_input.label_18.setText(str(data_nextMirror["index"]) + "/" + str(len(self.data_Mirror)))

    def UpdateMirror(self):
        if self.ui_input.x_Mirror.text() and self.ui_input.y_Mirror.text() and self.ui_input.z_Mirror.text() and self.ui_input.weight_Mirror.text()\
        and self.ui_input.height_Mirror.text() and self.ui_input.azimuth_Mirror.text() and self.ui_input.altitude_Mirror.text():
            data_updateMirror = {"type" : "Mirror", 
                "x": float(self.ui_input.x_Mirror.text()), 
                "y": float(self.ui_input.y_Mirror.text()), 
                "z":  float(self.ui_input.z_Mirror.text()),
                "zB_zA":  float(self.ui_input.zB_zA_Mirror.text()),
                "w": float(self.ui_input.weight_Mirror.text()), 
                "h": float(self.ui_input.height_Mirror.text()),
                "az": float(self.ui_input.azimuth_Mirror.text()),
                "al": float(self.ui_input.altitude_Mirror.text()),
                "index": self.count_Mirror}
            self.data_Mirror[self.count_Mirror] = data_updateMirror

    def GoMirror(self):
        if self.ui_input.page_go_Mirror.text() and 0 < int(self.ui_input.page_go_Mirror.text()) <= len(self.data_Mirror):
            data_goMirror = self.data_Mirror[int(self.ui_input.page_go_Mirror.text()) - 1]
            self.ui_input.x_Mirror.setText(str(data_goMirror["x"]))
            self.ui_input.y_Mirror.setText(str(data_goMirror["y"]))
            self.ui_input.z_Mirror.setText(str(data_goMirror["z"]))
            self.ui_input.zB_zA_Mirror.setText(str(data_goMirror["zB_zA"]))
            self.ui_input.weight_Mirror.setText(str(data_goMirror["w"]))
            self.ui_input.height_Mirror.setText(str(data_goMirror["h"])) 
            self.ui_input.azimuth_Mirror.setText(str(data_goMirror["az"])) 
            self.ui_input.altitude_Mirror.setText(str(data_goMirror["al"]))
            self.ui_input.label_18.setText(str(data_goMirror["index"]) + "/" + str(len(self.data_Mirror)))
            
            self.count_Mirror = int(self.ui_input.page_go_Mirror.text()) - 1 - self.check_prev_Mirror
            self.check_prev_Mirror = 1
            self.check_next_Mirror = 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Input()
    window.show()
    sys.exit(app.exec_())    
