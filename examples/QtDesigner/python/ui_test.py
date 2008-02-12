# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../test.ui'
#
# Created: Tue Feb 12 17:53:40 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,783,607).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        self.vboxlayout = QtGui.QVBoxLayout(self.centralWidget)
        self.vboxlayout.setObjectName("vboxlayout")

        self.examiner = QtGui.QWidget(self.centralWidget)
        self.examiner.setObjectName("examiner")
        self.vboxlayout.addWidget(self.examiner)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.buttonGroup = QtGui.QGroupBox(self.centralWidget)
        self.buttonGroup.setObjectName("buttonGroup")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.buttonGroup)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.button_x = QtGui.QPushButton(self.buttonGroup)
        self.button_x.setObjectName("button_x")
        self.hboxlayout1.addWidget(self.button_x)

        self.button_y = QtGui.QPushButton(self.buttonGroup)
        self.button_y.setObjectName("button_y")
        self.hboxlayout1.addWidget(self.button_y)

        self.button_z = QtGui.QPushButton(self.buttonGroup)
        self.button_z.setObjectName("button_z")
        self.hboxlayout1.addWidget(self.button_z)
        self.hboxlayout.addWidget(self.buttonGroup)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.checkbox = QtGui.QCheckBox(self.centralWidget)
        self.checkbox.setObjectName("checkbox")
        self.vboxlayout1.addWidget(self.checkbox)

        self.button = QtGui.QPushButton(self.centralWidget)
        self.button.setObjectName("button")
        self.vboxlayout1.addWidget(self.button)
        self.hboxlayout.addLayout(self.vboxlayout1)
        self.vboxlayout.addLayout(self.hboxlayout)
        MainWindow.setCentralWidget(self.centralWidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,783,22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea,self.toolBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonGroup.setTitle(QtGui.QApplication.translate("MainWindow", "GroupBox", None, QtGui.QApplication.UnicodeUTF8))
        self.button_x.setText(QtGui.QApplication.translate("MainWindow", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.button_y.setText(QtGui.QApplication.translate("MainWindow", "Y", None, QtGui.QApplication.UnicodeUTF8))
        self.button_z.setText(QtGui.QApplication.translate("MainWindow", "Z", None, QtGui.QApplication.UnicodeUTF8))
        self.checkbox.setText(QtGui.QApplication.translate("MainWindow", "CheckBox", None, QtGui.QApplication.UnicodeUTF8))
        self.button.setText(QtGui.QApplication.translate("MainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))

