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

from pivy.coin import *
from pivy.sogui import *

###############################################################
# CODE FOR The Inventor Mentor STARTS HERE

def writePickedPath(root, viewport, cursorPosition):
    myPickAction = SoRayPickAction(viewport)

    # Set an 8-pixel wide region around the pixel
    myPickAction.setPoint(cursorPosition)
    myPickAction.setRadius(8.0)

    # Start a pick traversal
    myPickAction.apply(root)
    myPickedPoint = myPickAction.getPickedPoint()
    if myPickedPoint == None: return FALSE

    # Write out the path to the picked object
    myWriteAction = SoWriteAction()
    myWriteAction.apply(myPickedPoint.getPath())

    return TRUE

# CODE FOR The Inventor Mentor ENDS HERE
###############################################################

# This routine is called for every mouse button event.
def myMousePressCB(userData, eventCB):
    root = userData
    event = eventCB.getEvent()

    # Check for mouse button being pressed  
    if SoMouseButtonEvent.isButtonPressEvent(event, SoMouseButtonEvent.ANY):
        myRegion = eventCB.getAction().getViewportRegion()
        writePickedPath(root, myRegion, event.getPosition(myRegion))
        eventCB.setHandled()

def main():
    myMouseEvent = SoMouseButtonEvent()

    # Initialize Inventor and Qt
    myWindow = SoGui.init(sys.argv[0])
    if myWindow == None:
        sys.exit(1)
    
    root = SoSeparator()
    root.ref()

    # Add an event callback to catch mouse button presses.
    # The callback is set up later on.
    myEventCB = SoEventCallback()
    root.addChild(myEventCB)

    # Read object data from a file
    mySceneInput = SoInput()
    if not mySceneInput.openFile("star.iv"):
        sys.exit(1)
    starObject = SoDB.readAll(mySceneInput)
    if starObject == None: sys.exit(1)
    mySceneInput.closeFile()

    # Add two copies of the star object, one white and one red
    myRotation = SoRotationXYZ()
    myRotation.axis = SoRotationXYZ.X
    myRotation.angle = M_PI/2.2  # almost 90 degrees
    root.addChild(myRotation)

    root.addChild(starObject)  # first star object

    myMaterial = SoMaterial()
    myMaterial.diffuseColor = (1.0, 0.0, 0.0)   # red
    root.addChild(myMaterial)
    myTranslation = SoTranslation()
    myTranslation.translation = (1.0, 0.0, 1.0)
    root.addChild(myTranslation)
    root.addChild(starObject)  # second star object

    # Create a render area in which to see our scene graph.
    myViewer = SoGuiExaminerViewer(myWindow)

    # Turn off viewing to allow picking
    myViewer.setViewing(0)

    myViewer.setSceneGraph(root)
    myViewer.setTitle("Pick Actions & Paths")
    myViewer.show()

    # Set up the event callback. We want to pass the root of the
    # entire scene graph (including the camera) as the userData,
    # so we get the scene manager's version of the scene graph
    # root.
    myEventCB.addEventCallback(SoMouseButtonEvent.getClassTypeId(),
                               myMousePressCB,
                               myViewer.getSceneManager().getSceneGraph())

    SoGui.show(myWindow)
    SoGui.mainLoop()

if __name__ == "__main__":
    main()
