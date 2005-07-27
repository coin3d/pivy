#!/usr/bin/env python

###
# Copyright (c) 2002, Tamer Fahmy <tamer@tammura.at>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#   * Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived
#     from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

##
# Demonstrates embedding of an SoQtExaminerViewer within a simple widget
# hierarchy.

import sys
from random import random

from pivy.coin import *
from pivy.gui.soqt import *

from qt import *

class EmbeddedWindow(QMainWindow):
    def __init__(self, *args):
        apply(QMainWindow.__init__, (self,) + args)

        # dummy widget needed for the PyQt stuff
        self.mainWidget = QWidget(self)
        self.setCentralWidget(self.mainWidget)

        self.mainLayout = QVBoxLayout(self.mainWidget, 10, 5)
        self.checkbox = QCheckBox("Enable &rotation", self.mainWidget)
        self.checkbox.setDown(False)

        self.examiner = QWidget(self.mainWidget)
        self.button = QPushButton("&Change cone color", self.mainWidget)

        self.buttonGroup = QHButtonGroup("Choose axis", self.mainWidget)
        self.radio_x = QRadioButton("&X", self.buttonGroup)
        self.radio_y = QRadioButton("&Y", self.buttonGroup)
        self.radio_z = QRadioButton("&Z", self.buttonGroup)
        self.radio_x.setChecked(True)
        
        self.mainLayout.addWidget(self.examiner)

        # construct a simple scenegraph
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

        # N.B.: keep in mind that it is important to keep the examiner
        # viewer as an instance variable by prefixing it with 'self.' 
        # otherwise it will fall out of scope and gets deallocated ->
        # no redraws and crashes. 20050727 tamer.

        # add the examinerviewer
        self.exam = SoQtExaminerViewer(self.examiner)
        self.exam.setSceneGraph(root)
        self.exam.setTitle("Embedded viewer")
        self.exam.show()

        self.hLayout = QHBoxLayout(self.mainLayout, 5)
        self.hLayout.addWidget(self.buttonGroup)

        self.controlLayout = QVBoxLayout(self.hLayout, 5)
        self.controlLayout.addWidget(self.checkbox)
        self.controlLayout.addWidget(self.button)

        self.connect(self.buttonGroup, SIGNAL("clicked(int)"), self.change_axis)
        self.connect(self.button, SIGNAL("clicked()"), self.change_color)
        self.connect(self.checkbox, SIGNAL("clicked()"), self.rotate)

    def change_axis(self, axis):
        self.rotxyz.axis = axis

    def change_color(self):
        self.material.diffuseColor = (random(), random(), random())

    def rotate(self):
        self.gate.enable = not self.gate.enable.getValue()

def main():
    # initialize Qt and SoQt
    SoQt.init(None)

    # set up scrollview window
    vp = EmbeddedWindow()
    # map window
    vp.resize(640, 480)

    # set termination condition
    QObject.connect(qApp, SIGNAL("lastWindowClosed()"), qApp, SLOT("quit()"))

    # start event loop
    SoQt.mainLoop()

if __name__ == '__main__':
    main()
