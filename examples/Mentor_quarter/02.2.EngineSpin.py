#!/usr/bin/env python

###
# Copyright (c) 2002-2007 Systems in Motion
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

###
# This is an example from the Inventor Mentor
# chapter 2, example 2.
#
# Use an engine to make the cone spin.
#

import sys

from PySide import QtGui
from pivy import coin, quarter

def main():
    # Initialize Inventor and Qt

    app = QtGui.QApplication(sys.argv)
    viewer = quarter.QuarterWidget()

    root = coin.SoSeparator()
    myCamera = coin.SoPerspectiveCamera()
    root.addChild(myCamera)
    root.addChild(coin.SoDirectionalLight())

    # This transformation is modified to rotate the cone
    myRotXYZ = coin.SoRotationXYZ()
    root.addChild(myRotXYZ)

    myMaterial = coin.SoMaterial()
    myMaterial.diffuseColor = (1.0, 0.0, 0.0)   # Red
    root.addChild(myMaterial)
    root.addChild(coin.SoCone())

    # An engine rotates the object. The output of myCounter 
    # is the time in seconds since the program started.
    # Connect this output to the angle field of myRotXYZ
    myRotXYZ.axis = coin.SoRotationXYZ.X     # rotate about X axis
    myCounter = coin.SoElapsedTime()
    myRotXYZ.angle.connectFrom(myCounter.timeOut)

    myCamera.viewAll(root, viewer.getSoRenderManager().getViewportRegion())

    viewer.setSceneGraph(root)
    viewer.setWindowTitle("Engine Spin")

    viewer.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
