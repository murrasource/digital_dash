#!/usr/bin/env python3

import os
import sys
import subprocess as sp
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from obd import *

# make our own double-click enabled button
class QDoublePushButton(QtWidgets.QPushButton):
    doubleClicked = QtCore.pyqtSignal()
    clicked = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        QtWidgets.QPushButton.__init__(self, *args, **kwargs)
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.clicked.emit)
        super().clicked.connect(self.checkDoubleClick)

    @QtCore.pyqtSlot()
    def checkDoubleClick(self):
        if self.timer.isActive():
            self.doubleClicked.emit()
            self.timer.stop()
        else:
            self.timer.start(250)


# the real meat of the operation
class Ui_MainWindow(object):
    # graphics and design with PyQt5
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)
        palette = QtGui.QPalette()
        MainWindow.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("High Tower Text")
        MainWindow.setFont(font)
        #MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        MainWindow.setStyleSheet("background-color: rgb(29, 29, 29); border-color: rgb(232, 232, 232);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # FRIZ LOGO
        self.friz = QtWidgets.QLabel(self.centralwidget)
        self.friz.setGeometry(QtCore.QRect(225, 30, 350, 50))
        self.friz.setPixmap(QtGui.QPixmap("/home/pi/Dashboard/logo.png"))
        self.friz.setScaledContents(True)
        self.friz.setObjectName("friz")


        # SPEED WIDGET
        self.spedometer = QtWidgets.QLabel(self.centralwidget)
        self.spedometer.setGeometry(QtCore.QRect(347, 140, 200, 200))
        font = QtGui.QFont()
        font.setFamily("Javanese Text")
        font.setPointSize(62)
        self.spedometer.setFont(font)
        self.spedometer.setStyleSheet("color: rgb(248, 248, 248);")
        self.spedometer.setObjectName("speed")

        # RPM LABEL
        self.rpm_label = QtWidgets.QLabel(self.centralwidget)
        self.rpm_label.setGeometry(QtCore.QRect(10, 10, 81, 51))
        font = QtGui.QFont()
        font.setFamily("Javanese Text")
        font.setPointSize(18)
        self.rpm_label.setFont(font)
        self.rpm_label.setStyleSheet("color: rgb(222, 222, 222);")
        self.rpm_label.setObjectName("rpm_label")

        # LOAD LABEL
        self.load_label = QtWidgets.QLabel(self.centralwidget)
        self.load_label.setGeometry(QtCore.QRect(689, 10, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Javanese Text")
        font.setPointSize(18)
        self.load_label.setFont(font)
        self.load_label.setStyleSheet("color: rgb(222, 222, 222);")
        self.load_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.load_label.setObjectName("load_label")

        # GAL LABEL
        self.gal_label = QtWidgets.QLabel(self.centralwidget)
        self.gal_label.setGeometry(QtCore.QRect(10, 400, 81, 51))
        font = QtGui.QFont()
        font.setFamily("Javanese Text")
        font.setPointSize(18)
        self.gal_label.setFont(font)
        self.gal_label.setStyleSheet("color: rgb(222, 222, 222);")
        self.gal_label.setObjectName("gal_label")

        # MI LABEL
        self.mi_label = QtWidgets.QLabel(self.centralwidget)
        self.mi_label.setGeometry(QtCore.QRect(710, 400, 81, 51))
        font = QtGui.QFont()
        font.setFamily("Javanese Text")
        font.setPointSize(18)
        self.mi_label.setFont(font)
        self.mi_label.setStyleSheet("color: rgb(222, 222, 222);")
        self.mi_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.mi_label.setObjectName("mi_label")

        # RPM WIDGET
        self.tachometer = QtWidgets.QLabel(self.centralwidget)
        self.tachometer.setGeometry(QtCore.QRect(10, 60, 171, 61))
        font = QtGui.QFont()
        font.setFamily("Lucida Calligraphy")
        font.setPointSize(32)
        self.tachometer.setFont(font)
        self.tachometer.setStyleSheet("color: rgb(248, 248, 248);")
        self.tachometer.setObjectName("rpm")

        #LOAD WIDGET
        self.load_meter = QtWidgets.QLabel(self.centralwidget)
        self.load_meter.setGeometry(QtCore.QRect(620, 60, 171, 61))
        font = QtGui.QFont()
        font.setFamily("Lucida Calligraphy")
        font.setPointSize(32)
        self.load_meter.setFont(font)
        self.load_meter.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.load_meter.setStyleSheet("color: rgb(248, 248, 248);")
        self.load_meter.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.load_meter.setObjectName("load")

        # MI WIDGET
        self.mi = QtWidgets.QLabel(self.centralwidget)
        self.mi.setGeometry(QtCore.QRect(620, 335, 171, 61))
        font = QtGui.QFont()
        font.setFamily("Lucida Calligraphy")
        font.setPointSize(32)
        self.mi.setFont(font)
        self.mi.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.mi.setStyleSheet("color: rgb(248, 248, 248);")
        self.mi.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.mi.setObjectName("mi")

        # GAL WIDGET
        self.gal = QtWidgets.QLabel(self.centralwidget)
        self.gal.setGeometry(QtCore.QRect(10, 335, 180, 61))
        font = QtGui.QFont()
        font.setFamily("Lucida Calligraphy")
        font.setPointSize(32)
        self.gal.setFont(font)
        self.gal.setStyleSheet("color: rgb(248, 248, 248);")
        self.gal.setObjectName("gal")

        # REFILL BUTTON
        self.refill_button = QDoublePushButton(self.centralwidget)
        self.refill_button.setGeometry(QtCore.QRect(334, 385, 132, 45))
        font = QtGui.QFont()
        font.setFamily("Javanese Text")
        font.setPointSize(14)
        self.refill_button.setFont(font)
        self.refill_button.setStyleSheet("color: rgb(248, 248, 248);")
        self.refill_button.setAutoDefault(False)
        self.refill_button.setDefault(False)
        self.refill_button.setFlat(False)
        self.refill_button.setObjectName("refill_button")
        # click once to refill
        self.refill_button.clicked.connect(self.refill)
        # double click to exit application
        self.refill_button.doubleClicked.connect(self.fullscreen)


        # general settings
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # set initial values before receiving OBD signals. Essentially the "booting state"
    def retranslateUi(self, MainWindow):
        global gallons
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dashboard"))
        self.spedometer.setText(_translate("MainWindow", "..."))
        self.rpm_label.setText(_translate("MainWindow", "RPM"))
        self.load_label.setText(_translate("MainWindow", "LOAD"))
        self.gal_label.setText(_translate("MainWindow", "GAL"))
        self.mi_label.setText(_translate("MainWindow", "MI"))
        self.tachometer.setText(_translate("MainWindow", "..."))
        self.load_meter.setText(_translate("MainWindow", "..."))
        self.mi.setText(_translate("MainWindow", "..."))
        self.gal.setText(_translate("MainWindow", "..."))
        self.refill_button.setText(_translate("MainWindow", "REFILL"))
    
    # warn when fuel level is low by changing the color of the refill button
    def warning(self):
        text = open("/home/pi/Dashboard/gallons.txt", "r")
        gallons = float(text.read())
        text.close()
        if gallons <= 3.5:
            return "color: rgb(248, 248, 248); background-color: rgb(245, 27, 27);"
        else:
            return "color: rgb(248,248,248); background-color: rgb(29, 29, 29);"

    # set fuel level to max (not necessary if your fuel indicator is functional)
    def refill(self):
        gallons = 26.0
        text = open("/home/pi/Dashboard/gallons.txt", "w")
        text.write(str(gallons))
        text.close()

    # query speed from OBD
    def speed(self):
        cmd = obd.commands.SPEED
        response = connection.query(cmd)
        return str(response.value.to('mph').magnitude).split(".")[0]
    
    # query RPM from OBD
    def rpm(self):
        cmd = obd.commands.RPM
        response = connection.query(cmd)
        return str(response.value.magnitude).split(".")[0]
    
    # calculate estimated fuel range
    def distance(self):
        text = open("/home/pi/Dashboard/gallons.txt", "r")
        gallons = float(text.read())
        text.close()
        t = str(gallons * 12.12)
        return t.split(".")[0]
    
    # query engine load from OBD
    def load(self):
        cmd = obd.commands.ENGINE_LOAD
        response = connection.query(cmd)
        return str(response.value.magnitude).split(".")[0] + "%"

    # calculate gasoline usage and return new fuel level
    def gas(self):
        # fetch the global gallons variable we read from the text document
        text = open("/home/pi/Dashboard/gallons.txt", "r+")
        g = float(text.read())

        # speed-based burn function
        def burn(speed):
            gpm = 0.0825
            miles_traveled = speed / 36000
            if miles_traveled == 0:
                miles_traveled = 0.000001
            fuel_burnt = gpm * miles_traveled
            return float(fuel_burnt)

        
        burnt = burn(float(self.speed()))

        # update text document storing fuel level
        g -= burnt
        g = str(g)
        text.seek(0)
        text.write(g)
        text.close()

        # rounding for the display (and not for the calculations) ensures more accuracy
        integer = g.split(".")[0]
        decimal = g.split(".")[1][0:2]
        g = integer + "." + decimal

        return g
    
    # enter or exit fullscreen
    def fullscreen(self):
        sys.exit()
    
    # update all values
    def update(self):
        try:
            gallons = self.gas()
            speed = self.speed()
            rpm = self.rpm()
            distance = self.distance()
            load = self.load()
            warning = self.warning()
            self.spedometer.setText(speed)
            self.gal.setText(gallons)
            self.tachometer.setText(rpm)
            self.mi.setText(distance)
            self.load_meter.setText(load)
            self.refill_button.setStyleSheet(warning)
            os.system("xset dpms force on")
        except:
            print("Car is turned off")
            os.system("xset dpms force off")
            time.sleep(3)
            global connection
            connection = obd.OBD()
            # connection = obd.OBD(portstr='/dev/pts/2')


# call our main loop
if __name__ == "__main__":
    # make sure bluetooth ELM327 device is connected
    stdoutdata = sp.getoutput('hcitool con')
    while '00:1D:A5:06:25:63' not in stdoutdata.split():
        print('ELM327 Device Not Yet Paired...')
        os.system('sudo systemctl start bluetooth && sudo rfkill unblock bluetooth && sudo bluetoothctl pair 00:1D:A5:06:25:63 && sudo bluetoothctl trust 00:1D:A5:06:25:63 && echo Paired')
        cmd = "sudo rfcomm connect /dev/rfcomm0 {} {} &".format('00:1D:A5:06:25:63', 1)
        conn = sp.Popen(cmd, shell=True)
        stdoutdata = sp.getoutput('hcitool con')
    else:
        pass
    
    connection = obd.OBD()

    while connection.status() not in [OBDStatus.CAR_CONNECTED, OBDStatus.OBD_CONNECTED, OBDStatus.ELM_CONNECTED]:
        print('Waiting for OBD-II Connection to be Established...')
        time.sleep(3)
        connection = obd.OBD()
        # connection = obd.OBD(portstr='/dev/pts/2')
    else:
        pass
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showFullScreen()
    
    timer = QtCore.QTimer()
    timer.timeout.connect(ui.update)
    timer.start(100)
    
    sys.exit(app.exec_())
