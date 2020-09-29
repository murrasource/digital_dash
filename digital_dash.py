#!/usr/bin/env python3

import os
import sys
import random
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from obd import *


# connect to the rfcomm channel
# os.system('sudo rfcomm connect 0 00:1D:A5:06:25:63')

i = 0

# variable to tell if screen is on or off
screen_state = 1

# set connection to OBD-II device
connection = obd.OBD()
 
# read the text file containing the fuel level information
# if your fuel sensor works (unlike mine), you don't need to do this. Instead, create a function to access the OBD fuel level
# a file is used so that if the RasPi looses power or the app is exited, the fuel consumption will still remain

text = open("/home/pi/Dashboard/gallons.txt", "r")
gallons = float(text.read())
text.close()

# make our own double-click enabled button
class QDoublePushButton(QtWidgets.QPushButton):
    doubleClicked = QtCore.pyqtSignal()
    clicked = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        QtWidgets.QPushButton.__init__(self, *args, **kwargs)
        self.timer = QTimer()
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
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
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
        global gallons
        if float(gallons) <= 3.5:
            return "color: rgb(248,248,248); background-color: rgb(245, 27, 27);"
        else:
            return "color: rgb(248,248,248);"

    # set fuel level to max (not necessary if your fuel indicator is functional)
    def refill(self):
        global gallons
        gallons = 26.0
        text = open("/home/pi/Dashboard/gallons.txt", "w")
        text.write(str(gallons))
        text.close()

    # calculate gasoline usage and return new fuel level
    def gas(self):
        # fetch the global gallons variable we read from the text document
        global gallons
        gallons = float(gallons)

        # function to calculate fuel burnt
        def burn(trim, air_mass):
            # adjust air-to-fuel ratio for bank 1
            if trim == 0:
                ratio = 14.7
            elif trim > 0:
                ratio = 14.7 * (1 + trim)
            else:
                ratio = 14.7 * (1 - trim)

            # calculate fuel burnt
            fuel_burnt_grams = air_mass / ratio
            fuel_burnt_mL = fuel_burnt_grams / 0.75
            fuel_burnt_gallons = fuel_burnt_mL / 3785.41

            return float(fuel_burnt_gallons)
        

        # query OBD for short fuel trim from engine bank 1
        cmd = obd.commands.SHORT_FUEL_TRIM_1
        response = connection.query(cmd)
        trim_1 = float(response.value.magnitude / 100)

        # query OBD for short fuel trim from engine bank 2
        cmd = obd.commands.SHORT_FUEL_TRIM_2
        response = connection.query(cmd)
        trim_2 = float(response.value.magnitude / 100)
        
        # query OBD for Air Flow Rate (MAF) given in grams/second
        cmd = obd.commands.MAF
        response = connection.query(cmd)
        # multiply response by 0.1 because the last update happened 0.1 seconds ago
        air_mass = float(response.value.magnitude * 0.1)

        # add fuel burnt by each engine bank
        burnt = burn(trim_1, air_mass) + burn(trim_2, air_mass)

        # update text document storing fuel level
        gallons -= burnt
        gallons = str(gallons)
        text = open("/home/pi/Dashboard/gallons.txt", "w")
        text.write(gallons)
        text.close()

        # rounding for the display (and not for the calculations) ensures more accuracy
        integer = gallons.split(".")[0]
        decimal = gallons.split(".")[1][0:2]
        gallons = integer + "." + decimal

        return gallons
    
    # query speed from OBD
    def speed(self):
        cmd = obd.commands.SPEED
        response = connection.query(cmd)
        return str(response.value.magnitude)
    
    # query RPM from OBD
    def rpm(self):
        cmd = obd.commands.RPM
        response = connection.query(cmd)
        return str(response.value.magnitude)
    
    # calculate estimated fuel range
    def distance(self):
        global gallons
        text = str(float(gallons) * 17.0)
        return text.split(".")[0]
    
    # query engine load from OBD
    def load(self):
        cmd = obd.commands.ENGINE_LOAD
        response = connection.query(cmd)
        return str(response.value)

    # turn screen off when engine is off to save battery
    def screen(self):
        global screen_state
        global connection
        if connection.status() == OBDStatus.OBD_CONNECTED:
            screen_state = 0
            os.system("xset dpms force off")
        else:
            os.system("xset dpms force on")

    
    # enter or exit fullscreen
    def fullscreen(self):
        sys.exit()

    # update all values
    def update(self):
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
        self.screen()

    # if connection is not working
    def not_connected(self):
        global gallons
        warning = self.warning()
        distance = self.distance()
        self.spedometer.setText("...")
        self.gal.setText(str(gallons))
        self.tachometer.setText(" ?")
        self.mi.setText(str(distance))
        self.load_meter.setText("? ")
        self.refill_button.setStyleSheet(warning)
        self.screen()

    # try connecting to a device
    def connect(self):
        global connection
        connection = obd.OBD()

    # car off mode but connected mode
    def car_off(self):
        global gallons
        global i
        if i > 7:
            i = 0
        else:
            pass
        options = ['-','\\','|','/','-','\\','|','/']
        warning = self.warning()
        distance = self.distance()
        self.spedometer.setText(options[i])
        self.gal.setText(str(gallons))
        self.tachometer.setText(options[i])
        self.mi.setText(str(distance))
        self.load_meter.setText(options[i])
        self.refill_button.setStyleSheet(warning)
        self.screen()
        i += 1


# call our main loop
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showFullScreen()
    # call the update function every 100 miliseconds
    if connection.status() == OBDStatus.CAR_CONNECTED:
        timer = QTimer()
        timer.timeout.connect(ui.update)
        timer.start(100)
    elif connection.status() == OBDStatus.OBD_CONNECTED or OBDStatus.ELM_CONNECTED:
        timer = QTimer()
        timer.timeout.connect(ui.car_off)
        timer.start(100)
    # try connecting to OBD every 3 seconds
    else: 
        timer = QTimer()
        timer.timeout.connect(ui.not_connected)
        timer.timeout.connect(ui.connect)
        timer.start(3000)
    sys.exit(app.exec_())