# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E000F.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(282, 324)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(QFont('Arial', 24))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setFont(QFont('Arial', 24))
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.lcdTemperatura = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdTemperatura.setObjectName("lcdTemperatura")
        self.gridLayout.addWidget(self.lcdTemperatura, 2, 0, 1, 1)
        self.lcdUmidade = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdUmidade.setObjectName("lcdUmidade")
        self.gridLayout.addWidget(self.lcdUmidade, 5, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Câmara E00XF"))
        self.label_2.setText(_translate("MainWindow", "Temperatura"))
        self.label.setText(_translate("MainWindow", "Umidade"))
