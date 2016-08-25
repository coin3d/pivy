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
# This is an example from The Inventor Mentor,
# chapter 9, example 4.
#
# Example of setting up pick actions and using the pick path.
# A couple of objects are displayed.  The program catches
# mouse button events and determines the mouse position.
# A pick action is applied and if an object is picked the
# pick path is printed to stdout.
#

import sys

from PySide import QtGui
from pivy import coin, quarter

###############################################################
# CODE FOR The Inventor Mentor STARTS HERE


def writePickedPath(root, viewport, cursorPosition):
    myPickAction = coin.SoRayPickAction(viewport)

    # Set an 8-pixel wide region around the pixel
    myPickAction.setPoint(cursorPosition)
    myPickAction.setRadius(8.0)

    # Start a pick traversal
    myPickAction.apply(root)
    myPickedPoint = myPickAction.getPickedPoint()
    if myPickedPoint == None:
        return False

    # Write out the path to the picked object
    myWriteAction = coin.SoWriteAction()
    myWriteAction.apply(myPickedPoint.getPath())

    return True

# CODE FOR The Inventor Mentor ENDS HERE
###############################################################

# This routine is called for every mouse button event.


def myMousePressCB(userData, eventCB):
    root = userData
    event = eventCB.getEvent()

    # Check for mouse button being pressed
    if coin.SoMouseButtonEvent.isButtonPressEvent(event, coin.SoMouseButtonEvent.ANY):
        myRegion = eventCB.getAction().getViewportRegion()
        writePickedPath(root, myRegion, event.getPosition(myRegion))
        eventCB.setHandled()


def main():
    myMouseEvent = coin.SoMouseButtonEvent()

    # Initialize Inventor and Qt
    app = QtGui.QApplication([])
    viewer = quarter.QuarterWidget()

    root = coin.SoSeparator()

    # Add an event callback to catch mouse button presses.
    # The callback is set up later on.
    myEventCB = coin.SoEventCallback()
    root += myEventCB

    # Read object data from a file
    mySceneInput = coin.SoInput()
    if not mySceneInput.openFile("star.iv"):
        sys.exit(1)
    starObject = coin.SoDB.readAll(mySceneInput)
    if starObject == None:
        sys.exit(1)
    mySceneInput.closeFile()

    # Add two copies of the star object, one white and one red
    myRotation = coin.SoRotationXYZ()
    myRotation.axis = coin.SoRotationXYZ.X
    myRotation.angle = coin.M_PI / 2.2  # almost 90 degrees
    myMaterial = coin.SoMaterial()
    myMaterial.diffuseColor = (1.0, 0.0, 0.0)   # red
    myTranslation = coin.SoTranslation()
    myTranslation.translation = (1.0, 0.0, 1.0)

    root += (myRotation, starObject, myMaterial, myTranslation, starObject)

    # Turn off viewing to allow picking ?
    # viewer.setViewing(0)

    viewer.sceneGraph = root
    viewer.setWindowTitle("Pick Actions & Paths")
    viewer.show()
    viewer.viewAll()

    # Set up the event callback. We want to pass the root of the
    # entire scene graph (including the camera) as the userData,
    # so we get the scene manager's version of the scene graph
    # root.
    myEventCB.addEventCallback(coin.SoMouseButtonEvent.getClassTypeId(),
                               myMousePressCB,
                               viewer.sceneGraph)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
