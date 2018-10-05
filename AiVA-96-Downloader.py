import sys
import os
import platform
import subprocess
import threading
import usb.core
import usb.util
from time import sleep
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
#from PyQt5 import QtCore, QtGui, QtWidgets


class DownloadWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AiVA 다운로더 v1.0.0")
        self.setGeometry(300, 300, 520, 220)

        # Label
        labelBinaryFileName = QLabel("바이너리 파일명", self)
        labelBinaryFileName.move(10, 20)

        labelBinaryPath = QLabel("바이너리 위치", self)
        labelBinaryPath.move(10, 60)

        labelLotNumber = QLabel("로트번호", self)
        labelLotNumber.move(10, 100)

        labelSerialNumber = QLabel("시작번호", self)
        labelSerialNumber.move(170, 100)

        labelSerialTotal = QLabel("갯수", self)
        labelSerialTotal.move(290, 100)

        self.labelProgress = QLabel("--------진행상황--------", self)
        newfont = QFont("Times", 17, QFont.Bold)
        self.labelProgress.setFont(newfont)
        self.labelProgress.move(60, 150)
        self.labelProgress.resize(380, 30)

        # editBinaryFileName
        self.editBinaryFileName = QLineEdit("", self)
        self.editBinaryFileName.resize(250, 30)
        self.editBinaryFileName.move(110, 20)
        self.editBinaryFileName.setText('app_vf_spk_base_1i6o2_AiVA_lin15')

        # editBinaryPath
        self.editBinaryPath = QLineEdit("", self)
        self.editBinaryPath.resize(250, 30)
        self.editBinaryPath.move(110, 60)

        self.editlotNumber = QLineEdit("", self)
        self.editlotNumber.resize(50, 30)
        self.editlotNumber.move(110, 100)        

        self.editSerialStart = QLineEdit("", self)
        self.editSerialStart.resize(50, 30)
        self.editSerialStart.move(230, 100)

        self.editSerialTotal = QLineEdit("", self)
        self.editSerialTotal.resize(50, 30)
        self.editSerialTotal.move(330, 100)

        # Path button
        btnPath = QPushButton("...", self)
        btnPath.resize(30, 30)
        btnPath.move(360, 60)
        btnPath.clicked.connect(self.btnPath_clicked)

        # Download button
        btnDownload = QPushButton("다운로드 실행", self)
        btnDownload.move(400, 20)
        btnDownload.clicked.connect(self.btnDownload_clicked)

        # Download button
        btnExit = QPushButton("종료", self)
        btnExit.move(400, 60)
        btnExit.clicked.connect(self.btnExit_clicked)        

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

    def btnPath_clicked(self):
        fname = QFileDialog.getExistingDirectory(self)
        print(fname)
        self.editBinaryPath.setText(fname)

    def btnExit_clicked(self):
        QMessageBox.about(self, "정보", "AiVA 다운로더를 종료합니다.")
        exit(1)

    def download_on_windows(self):
        print("download_on_windows")
        currentDirectory = os.getcwd()
        f = open("tmpDownload.bat","w")
        f.writelines("C:\n")
        f.writelines("cd C:\\Program Files (x86)\\XMOS\\xTIMEcomposer\\Community_14.3.3\\\n")
        f.writelines("call SetEnv.bat\n")
        f.writelines("cd " + currentDirectory + "\n")
        f.writelines("xflash -l\n")
        f.writelines("xflash --no-compression " + self.checkBinaryFileName + "\n")
        f.close()
        return_code = subprocess.call("tmpDownload.bat", shell=True)
        print(return_code)
        if return_code == 1:
            QMessageBox.about(self, "Error", "Image download failed.")
            print("Error: download failed.")
            exit(1)

    def download_on_linux(self, serialString):
        print("download_on_linux: " + serialString)
        f = open("tmpDownload.sh","w")
        #f.writelines("#!/bin/bash\n")
        f.writelines("xflash --no-compression " + self.checkBinaryFileName + "\n")
        f.close()
        return_code = subprocess.call("bash tmpDownload.sh", shell=True)
        print(return_code)
        if return_code == 1:
            QMessageBox.about(self, "에러", "이미지 다운로드를 실패하였습니다.")
            print("Error: download failed.")
        #    exit(1)

        QMessageBox.about(self, "검사", "이미지 다운로드가 완료되었습니다.\n시리얼 번호를 검사합니다..")

        VID = 0x20B1
        PID = 0x0011

        dev = usb.core.find(idVendor=VID, idProduct=PID)
        if dev is None:
            QMessageBox.about(self, "에러", "AiVA-96 장치를 찾지 못했습니다.")
            print("Cound not find AiVA device :(")
            exit(1)
        print("Yeeha! Found a AiVA device")

        print("Firmware version: " + hex(dev.bcdDevice))

        serialNumber = usb.util.get_string(dev, dev.iSerialNumber)
        print("Serial number: " + serialNumber)

        if serialString != serialNumber:
            QMessageBox.about(self, "에러", "다운로드한 이미지의 시리얼번호와\n 보드의 시리얼 번호가 일치하지 않습니다.")
            print("Cound not find AiVA device :(")            
            exit(1)

    def progressUpdate(self):
        self.labelProgress.setText(self.message)

    def btnDownload_clicked(self):

        buttonReply = QMessageBox.question(self, '정보', "이미지 다운로드를 시작할까요?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if buttonReply == QMessageBox.No:
            QMessageBox.about(self, "정보", "이미지 다운로드 작업을 취소합니다.")
            return

        self.binaryFileName = self.editBinaryFileName.text()
        self.binaryPath = self.editBinaryPath.text()
        self.lotNumber = self.editlotNumber.text()
        self.serialStart = self.editSerialStart.text()
        self.serialTotal = self.editSerialTotal.text()

        if not os.path.isdir(self.binaryPath):
            print(self.binaryPath + " doesn't exist.")
            exit(1)

        start = int(self.serialStart)
        end = int(self.serialTotal) + start
        binaryFileName = self.binaryFileName
        for serialIndex in range(start, end):
            self.message = "시리얼넘버: " + "%04d-" % int(self.lotNumber) + "%05d" % serialIndex + " 다운로드 중.."
            update = threading.Thread(target=self.progressUpdate)
            update.daemon = True
            update.start()

            msg = "시리얼넘버 " + "%05d" % serialIndex + "번째 보드를 연결 후, [확인]을 누르세요."
            QMessageBox.about(self, "정보", msg)

            serialString = "%04d-" % int(self.lotNumber) + "%05d" % serialIndex
            if self.os == "windows":
                self.checkBinaryFileName = self.binaryPath + "\\" + binaryFileName + "_" + serialString + ".xe"
            elif self.os == "linux" or self.os == "mac":
                self.checkBinaryFileName = self.binaryPath + "/" + binaryFileName + "_" + serialString + ".xe"

            print(self.checkBinaryFileName)
            if not os.path.isfile(self.checkBinaryFileName):
                print(self.checkBinaryFileName + " 파일이 존재하지 않습니다.\n파일 경로를 확인하세요.")
                exit(1)

            if self.os == "windows":
                self.download_on_windows()
            elif self.os == "linux" or self.os == "mac":
                self.download_on_linux(serialString)

        QMessageBox.about(self, "완료", "이미지 다운로드 작업을 완료하였습니다.")
        exit(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    downloadWindow = DownloadWindow()
    downloadWindow.show()
    app.exec_()
