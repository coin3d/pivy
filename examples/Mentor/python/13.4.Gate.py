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
# This is an example from the Inventor Mentor
# chapter 13, example 5.
#
# Gate engine.
# Mouse button presses enable and disable a gate engine.
# The gate engine controls an elapsed time engine that
# controls the motion of the duck.
#

from pivy import *
import sys

#############################################################
# CODE FOR The Inventor Mentor STARTS HERE  (part 2)

# This routine is called for every mouse button event.
def myMousePressCB(userData, eventCB):
    gate = cast(userData, "SoGate")
    event = eventCB.getEvent()

    # Check for mouse button being pressed
    if SoMouseButtonEvent_isButtonPressEvent(event, SoMouseButtonEvent.ANY):

        # Toggle the gate that controls the duck motion
        if gate.enable.getValue():
            gate.enable.setValue(FALSE)
        else:
            gate.enable.setValue(TRUE)

        eventCB.setHandled()

# CODE FOR The Inventor Mentor ENDS HERE
#############################################################


def main():
    # Print out usage message
    print "Click the left mouse button to enable/disable the duck motion"

    # Initialize Inventor and Qt
    myWindow = SoQt_init(sys.argv[0])  
    if myWindow == None: sys.exit(1)     

    root = SoSeparator()
    root.ref()

    # Add a camera and light
    myCamera = SoPerspectiveCamera()
    myCamera.position.setValue(0., -4., 8.0)
    myCamera.heightAngle(M_PI/2.5)
    myCamera.nearDistance(1.0)
    myCamera.farDistance(15.0)
    root.addChild(myCamera)
    root.addChild(SoDirectionalLight())

    # Rotate scene slightly to get better view
    globalRotXYZ = SoRotationXYZ()
    globalRotXYZ.axis(SoRotationXYZ.X)
    globalRotXYZ.angle(M_PI/9)
    root.addChild(globalRotXYZ)

    # Pond group
    pond = SoSeparator()
    root.addChild(pond)
    cylMaterial = SoMaterial()
    cylMaterial.diffuseColor.setValue(0., 0.3, 0.8)
    pond.addChild(cylMaterial)
    cylTranslation = SoTranslation()
    cylTranslation.translation.setValue(0., -6.725, 0.)
    pond.addChild(cylTranslation)
    myCylinder = SoCylinder()
    myCylinder.radius.setValue(4.0)
    myCylinder.height.setValue(0.5)
    pond.addChild(myCylinder)

#############################################################
# CODE FOR The Inventor Mentor STARTS HERE  (part 1)

    # Duck group
    duck = SoSeparator()
    root.addChild(duck)

    # Read the duck object from a file and add to the group
    myInput = SoInput()
    if not myInput.openFile("duck.iv"):
        sys.exit(1)
    duckObject = SoDB_readAll(myInput)
    if duckObject == None:
        sys.exit(1)

    # Set up the duck transformations
    duckRotXYZ = SoRotationXYZ()
    duck.addChild(duckRotXYZ)
    initialTransform = SoTransform()
    initialTransform.translation.setValue(0., 0., 3.)
    initialTransform.scaleFactor.setValue(6., 6., 6.)
    duck.addChild(initialTransform)

    duck.addChild(duckObject)

    # Update the rotation value if the gate is enabled.
    myGate = SoGate(SoMFFloat_getClassTypeId())
    myCounter = SoElapsedTime()
    myGate.input.connectFrom(myCounter.timeOut) 
    duckRotXYZ.axis(SoRotationXYZ.Y)  # rotate about Y axis
    duckRotXYZ.angle.connectFrom(myGate.output)

    # Add an event callback to catch mouse button presses.
    # Each button press will enable or disable the duck motion.
    myEventCB = SoEventCallback()
    myEventCB.addPythonEventCallback(SoMouseButtonEvent_getClassTypeId(),
                                     myMousePressCB, myGate)
    root.addChild(myEventCB)

# CODE FOR The Inventor Mentor ENDS HERE
#############################################################

    myRenderArea = SoQtRenderArea(myWindow)
    myRenderArea.setSceneGraph(root)
    myRenderArea.setTitle("Duck Pond")
    myRenderArea.show()

    SoQt_show(myWindow)
    SoQt_mainLoop()

if __name__ == "__main__":
    main()
