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
# This is an example from the Inventor Mentor,
# chapter 14, example 3.
#
# This example illustrates the creation of motion hierarchies
# using nodekits by creating a model of a balance-style scale.
#
# It adds an SoEventCallback to the "callback" list in the 
#     nodekit called 'support.'
# The callback will have the following response to events:
# Pressing right arrow key == lower the right pan
# Pressing left arrow key  == lower the left pan
# The pans are lowered by animating three rotations in the 
#     motion hierarchy.
# Use an SoText2Kit to print instructions to the user as part
#     of the scene.
#

from pivy import *
import sys

# Callback Function for Animating the Balance Scale.
# -- used to make the balance tip back and forth
# -- Note: this routine is only called in response to KeyPress
#    events since the call 'setEventInterest(KeyPressMask)' is
#    made on the SoEventCallback node that uses it.
# -- The routine checks if the key pressed was left arrow (which
#    is XK_Left in X-windows talk), or right arrow (which is
#    XK_Right)
# -- The balance is made to tip by rotating the beam part of the
#    scale (to tip it) and then compensating (making the strings
#    vertical again) by rotating the string parts in the opposite
#    direction.
def tipTheBalance(userData, # The nodekit representing 'support', the
                  # fulcrum of the balance. Passed in during
                  # main routine, below. 
                  eventCB):

    ev = eventCB.getEvent()

    # Which Key was pressed?
    # If Right or Left Arrow key, then continue...
    if SoKeyboardEvent_isKeyPressEvent(ev, SoKeyboardEvent.RIGHT_ARROW) or \
       SoKeyboardEvent_isKeyPressEvent(ev, SoKeyboardEvent.LEFT_ARROW):
        startRot, beamIncrement, stringIncrement = SbRotation(), SbRotation(), SbRotation()
        
        # Get the different nodekits from the userData.
        support = cast(userData, "SoShapeKit")

        # These three parts are extracted based on knowledge of the
        # motion hierarchy (see the diagram in the main routine.
        beam1   = cast(support.getPart("childList[0]",TRUE), "SoShapeKit")
        string1 = cast(beam1.getPart("childList[0]",TRUE), "SoShapeKit")
        string2 = cast(beam1.getPart("childList[1]",TRUE), "SoShapeKit")

        # Set angular increments to be .1 Radians about the Z-Axis
        # The strings rotate opposite the beam, and the two types
        # of key press produce opposite effects.
        if SoKeyboardEvent_isKeyPressEvent(ev, SoKeyboardEvent.RIGHT_ARROW):
            beamIncrement.setValue(SbVec3f(0, 0, 1), -.1)
            stringIncrement.setValue(SbVec3f(0, 0, 1), .1)
        else:
            beamIncrement.setValue(SbVec3f(0, 0, 1), .1)
            stringIncrement.setValue(SbVec3f(0, 0, 1), -.1)

        # Use SO_GET_PART to find the transform for each of the 
        # rotating parts and modify their rotations.

        xf = cast(beam1.getPart("transform", TRUE), "SoTransform")
        startRot = xf.rotation.getValue()
        startRot *= beamIncrement
        xf.rotation.setValue(startRot)

        xf = cast(string1.getPart("transform", TRUE), "SoTransform")
        startRot = xf.rotation.getValue()
        startRot *= stringIncrement
        xf.rotation.setValue(startRot)

        xf = cast(string2.getPart("transform", TRUE), "SoTransform")
        startRot = xf.rotation.getValue()
        startRot *= stringIncrement     
        xf.rotation.setValue(startRot)

        eventCB.setHandled()

def main():
    # Initialize Inventor and Qt
    myWindow = SoQt_init(sys.argv[0])  
    if myWindow == None: sys.exit(1)     

    myScene = SoSceneKit()
    myScene.ref()

    myScene.setPart("lightList[0]", SoLightKit())
    myScene.setPart("cameraList[0]", SoCameraKit())
    myScene.setCameraNumber(0)

    # Create the Balance Scale -- put each part in the 
    # childList of its parent, to build up this hierarchy:
    #
    #                    myScene
    #                       |
    #                     support
    #                       |
    #                     beam
    #                       |
    #                   --------
    #                   |       |
    #                string1  string2
    #                   |       |
    #                tray1     tray2

    support = SoShapeKit()
    support.setPart("shape", SoCone())
    support.set("shape { height 3 bottomRadius .3 }")
    myScene.setPart("childList[0]", support)

    beam = SoShapeKit()
    beam.setPart("shape", SoCube())
    beam.set("shape { width 3 height .2 depth .2 }")
    beam.set("transform { translation 0 1.5 0 } ")
    support.setPart("childList[0]", beam)

    string1 = SoShapeKit()
    string1.setPart("shape", SoCylinder())
    string1.set("shape { radius .05 height 2}")
    string1.set("transform { translation -1.5 -1 0 }")
    string1.set("transform { center 0 1 0 }")
    beam.setPart("childList[0]", string1)

    string2 = SoShapeKit()
    string2.setPart("shape", SoCylinder())
    string2.set("shape { radius .05 height 2}")
    string2.set("transform { translation 1.5 -1 0 } ")
    string2.set("transform { center 0 1 0 } ")
    beam.setPart("childList[1]", string2)

    tray1 = SoShapeKit()
    tray1.setPart("shape", SoCylinder())
    tray1.set("shape { radius .75 height .1 }")
    tray1.set("transform { translation 0 -1 0 } ")
    string1.setPart("childList[0]", tray1)

    tray2 = SoShapeKit()
    tray2.setPart("shape", SoCylinder())
    tray2.set("shape { radius .75 height .1 }")
    tray2.set("transform { translation 0 -1 0 } ")
    string2.setPart("childList[0]", tray2)

    # Add EventCallback so Balance Responds to Events
    myCallbackNode = SoEventCallback()
    myCallbackNode.addPythonEventCallback(SoKeyboardEvent_getClassTypeId(),
                                          tipTheBalance, support)
    support.setPart("callbackList[0]", myCallbackNode)

    # Add Instructions as Text in the Scene...
    myText = SoShapeKit()
    myText.setPart("shape", SoText2())
    myText.set("shape { string \"Press Left or Right Arrow Key\" }")
    myText.set("shape { justification CENTER }")
    myText.set("font { name \"Helvetica-Bold\" }")
    myText.set("font { size 16.0 }")
    myText.set("transform { translation 0 -2 0 }")
    myScene.setPart("childList[1]", myText)

    myRenderArea = SoQtRenderArea(myWindow)

    # Get camera from scene and tell it to viewAll...
    myCamera = cast(myScene.getPart("cameraList[0].camera", TRUE), "SoPerspectiveCamera")
    myCamera.viewAll(myScene, myRenderArea.getViewportRegion())

    myRenderArea.setSceneGraph(myScene)
    myRenderArea.setTitle("Balance Scale Made of Nodekits")
    myRenderArea.show()

    SoQt_show(myWindow)
    SoQt_mainLoop()

if __name__ == "__main__":
    main()
