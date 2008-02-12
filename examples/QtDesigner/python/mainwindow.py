#!/usr/bin/env python

from pivy.coin import *
from pivy.gui.soqt import SoQtExaminerViewer
from ui_test import Ui_MainWindow
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QMainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setupSoQt()

    def setupSoQt(self):
        root = SoSeparator()
        self.rotxyz = SoRotationXYZ()
        self.gate = SoGate(SoMFFloat.getClassTypeId())
        self.elapsedTime = SoElapsedTime()
        self.gate.enable = False
        self.gate.input.connectFrom(self.elapsedTime.timeOut)
        self.rotxyz.angle.connectFrom(self.gate.output)        
        self.material = SoMaterial()
        self.material.diffuseColor = (0.0, 1.0, 1.0)
        self.cone = SoCone()
        root.addChild(self.rotxyz)
        root.addChild(self.material)
        root.addChild(self.cone)

        self.exam = SoQtExaminerViewer(self.examiner)
        self.exam.setSceneGraph(root)
        #self.exam.show()
