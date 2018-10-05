import sys
import os
import platform
import subprocess
import threading
import usb.core
import usb.util
import serial
import time
from time import sleep
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
#from PyQt5 import QtCore, QtGui, QtWidgets


class DownloadWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AiVA-96 테스트 프로그램 v1.0.0")
        self.setGeometry(300, 300, 290, 320)

        self.editTestUart = QLineEdit("", self)
        self.editTestUart.resize(250, 30)
        self.editTestUart.move(20, 200)

        btnGetSerial = QPushButton("시리얼 넘버 읽기", self)
        btnGetSerial.resize(250, 30)
        btnGetSerial.move(20, 20)
        btnGetSerial.clicked.connect(self.btnGetSerial_clicked)        

        btnTestSpeaker = QPushButton("스피커 테스트", self)
        btnTestSpeaker.resize(250, 30)
        btnTestSpeaker.move(20, 60)
        btnTestSpeaker.clicked.connect(self.btnTestSpeaker_clicked)

        btnTestUart = QPushButton("UART 테스트", self)
        btnTestUart.resize(250, 30)
        btnTestUart.move(20, 100)
        btnTestUart.clicked.connect(self.btnTestUart_clicked)        

        self.labelSerial = QLabel("시리얼번호: ", self)
        newfont = QFont("Times", 17, QFont.Bold)
        self.labelSerial.setFont(newfont)
        self.labelSerial.resize(380, 30)   
        self.labelSerial.move(20, 240) 

        self.labelSWVersion = QLabel("SW버전: ", self)
        newfont = QFont("Times", 17, QFont.Bold)
        self.labelSWVersion.setFont(newfont)
        self.labelSWVersion.resize(380, 30)   
        self.labelSWVersion.move(20, 280)             

        if platform.system().upper() == "LINUX":
            print("LINUX")
            self.os = "linux"
        elif platform.system().upper() == "WINDOWS":
            print("WINDOWS")
            self.os = "windows"
        elif platform.system().upper() == "DARWIN":
            print("MacOS")
            self.os = "mac"
        else:
            print("Error: Unknown OS")
            exit(1)

    def btnGetSerial_clicked(self):
        VID = 0x20B1
        PID = 0x0011

        dev = usb.core.find(idVendor=VID, idProduct=PID)
        if dev is None:
            QMessageBox.about(self, "에러", "AiVA-96 장치를 찾지 못했습니다.")
            print("Cound not find AiVA device :(")
            exit(1)
        print("Yeeha! Found a AiVA device")

        swVersion = hex(dev.bcdDevice)
        print("Firmware version: " + swVersion)

        serialNumber = usb.util.get_string(dev, dev.iSerialNumber)
        print("Serial number: " + serialNumber)

        self.labelSerial.setText("시리얼번호: " + serialNumber)
        self.labelSWVersion.setText("SW버전: " + swVersion)

    def btnTestSpeaker_clicked(self):
        return_code = subprocess.call("mpg123 sample.mp3", shell=True)
        if return_code == 1:
            QMessageBox.about(self, "에러", "음원을 재생하는데 실패하였습니다.")

        buttonReply = QMessageBox.question(self, '질문', "소리가 정상적으로 출력이 되나요 ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if buttonReply == QMessageBox.No:
            QMessageBox.about(self, "정보", "스피커 또는 스피커 단자에\n문제가 있는지 확인해 보세요.")
            return

    def btnTestUart_clicked(self):
        ser = serial.Serial("/dev/ttyUSB0", 9600)
        ser.close()
        ser.open()

        print("testing start")

        try:
            ser.write(bytes('Pass', encoding='ascii'))
            time.sleep(0.3)
            response = ser.read(ser.inWaiting())
            self.editTestUart.setText(str(response))
            print(response)		
        except KeyboardInterrupt:
            ser.close()

        buttonReply = QMessageBox.question(self, '질문', "b'Pass'가 정상적으로 출력이 되나요 ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if buttonReply == QMessageBox.No:
            QMessageBox.about(self, "정보", "UART에 문제가 있는지 확인해 보세요.")
            return                

if __name__ == "__main__":
    app = QApplication(sys.argv)
    downloadWindow = DownloadWindow()
    downloadWindow.show()
    app.exec_()
