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
# chapter 13, example 6.
#
# Boolean engine.  Derived from example 13.5.
# The smaller duck stays still while the bigger duck moves,
# and starts moving as soon as the bigger duck stops.
#

from pivy import *
import sys

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


def main():
    # Print out usage message
    print "Only one duck can move at a time."
    print "Click the left mouse button to toggle between the two ducks."

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
    pondTranslation = SoTranslation()
    pondTranslation.translation.setValue(0., -6.725, 0.)
    pond.addChild(pondTranslation)
    # water
    waterMaterial = SoMaterial()
    waterMaterial.diffuseColor.setValue(0., 0.3, 0.8)
    pond.addChild(waterMaterial)
    waterCylinder = SoCylinder()
    waterCylinder.radius.setValue(4.0)
    waterCylinder.height.setValue(0.5)
    pond.addChild(waterCylinder)
    # rock
    rockMaterial = SoMaterial()
    rockMaterial.diffuseColor.setValue(0.8, 0.23, 0.03)
    pond.addChild(rockMaterial)
    rockSphere = SoSphere()
    rockSphere.radius.setValue(0.9)
    pond.addChild(rockSphere)

    # Read the duck object from a file and add to the group
    myInput = SoInput()
    if not myInput.openFile("duck.iv"):
        sys.exit(1)
    duckObject = SoDB_readAll(myInput)
    if duckObject == None:
        sys.exit(1)

#############################################################
# CODE FOR The Inventor Mentor STARTS HERE  

    # Bigger duck group
    bigDuck = SoSeparator()
    root.addChild(bigDuck)
    bigDuckRotXYZ = SoRotationXYZ()
    bigDuck.addChild(bigDuckRotXYZ)
    bigInitialTransform = SoTransform()
    bigInitialTransform.translation.setValue(0., 0., 3.5)
    bigInitialTransform.scaleFactor.setValue(6., 6., 6.)
    bigDuck.addChild(bigInitialTransform)
    bigDuck.addChild(duckObject)

    # Smaller duck group
    smallDuck = SoSeparator()
    root.addChild(smallDuck)
    smallDuckRotXYZ = SoRotationXYZ()
    smallDuck.addChild(smallDuckRotXYZ)
    smallInitialTransform = SoTransform()
    smallInitialTransform.translation.setValue(0., -2.24, 1.5)
    smallInitialTransform.scaleFactor.setValue(4., 4., 4.)
    smallDuck.addChild(smallInitialTransform)
    smallDuck.addChild(duckObject)

    # Use a gate engine to start/stop the rotation of 
    # the bigger duck.
    bigDuckGate = SoGate(SoMFFloat_getClassTypeId())
    bigDuckTime = SoElapsedTime()
    bigDuckGate.input.connectFrom(bigDuckTime.timeOut) 
    bigDuckRotXYZ.axis(SoRotationXYZ.Y)  # Y axis
    bigDuckRotXYZ.angle.connectFrom(bigDuckGate.output)

    # Each mouse button press will enable/disable the gate 
    # controlling the bigger duck.
    myEventCB = SoEventCallback()
    myEventCB.addEventCallback(SoMouseButtonEvent_getClassTypeId(),
                               myMousePressCB, bigDuckGate)
    root.addChild(myEventCB)

    # Use a Boolean engine to make the rotation of the smaller
    # duck depend on the bigger duck.  The smaller duck moves
    # only when the bigger duck is still.
    myBoolean = SoBoolOperation()
    myBoolean.a.connectFrom(bigDuckGate.enable)
    myBoolean.operation.setValue(SoBoolOperation.NOT_A)

    smallDuckGate = SoGate(SoMFFloat_getClassTypeId())
    smallDuckTime = SoElapsedTime()
    smallDuckGate.input.connectFrom(smallDuckTime.timeOut) 
    smallDuckGate.enable.connectFrom(myBoolean.output) 
    smallDuckRotXYZ.axis(SoRotationXYZ.Y)  # Y axis
    smallDuckRotXYZ.angle.connectFrom(smallDuckGate.output)

# CODE FOR The Inventor Mentor ENDS HERE
#############################################################

    myRenderArea = SoQtRenderArea(myWindow)
    myRenderArea.setSceneGraph(root)
    myRenderArea.setTitle("Duck and Duckling")
    myRenderArea.show()

    SoQt_show(myWindow)
    SoQt_mainLoop()

if __name__ == "__main__":
    main()
