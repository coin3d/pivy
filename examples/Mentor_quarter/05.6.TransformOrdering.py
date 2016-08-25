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
# This is an example from the Inventor Mentor,
# chapter 5, example 6.
#
# This example shows the effect of different order of
# operation of transforms.  The left object is first
# scaled, then rotated, and finally translated to the left.
# The right object is first rotated, then scaled, and finally
# translated to the right.
#

import sys

from PySide import QtGui
from pivy import coin, quarter


def main():
    # Initialize Inventor and Qt
    app = QtGui.QApplication([])
    viewer = quarter.QuarterWidget()

    root = coin.SoSeparator()

    # Create two separators, for left and right objects.
    leftSep = coin.SoSeparator()
    rightSep = coin.SoSeparator()
    root.addChild(leftSep)
    root.addChild(rightSep)

    # Create the transformation nodes
    leftTranslation = coin.SoTranslation()
    rightTranslation = coin.SoTranslation()
    myRotation = coin.SoRotationXYZ()
    myScale = coin.SoScale()

    # Fill in the values
    leftTranslation.translation = (-1.0, 0.0, 0.0)
    rightTranslation.translation = (1.0, 0.0, 0.0)
    myRotation.angle = coin.M_PI / 2   # 90 degrees
    myRotation.axis = coin.SoRotationXYZ.X
    myScale.scaleFactor = (2., 1., 3.)

    # Add transforms to the scene.
    leftSep += leftTranslation, myRotation, myScale
    rightSep += rightTranslation, myScale, myRotation

    # Read an object from file. (as in example 4.2.Lights)
    myInput = coin.SoInput()
    if not myInput.openFile("temple.iv"):
        sys.exit(1)

    fileContents = coin.SoDB.readAll(myInput)
    if fileContents is None:
        sys.exit(1)

    # Add an instance of the object under each separator.
    leftSep += fileContents
    rightSep += fileContents

    # Construct a renderArea and display the scene.
    viewer.setSceneGraph(root)
    viewer.setWindowTitle("Transform Ordering")
    viewer.show()
    viewer.viewAll()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
