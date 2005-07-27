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
# chapter 14, example 2.
#
# Use nodekits to create a scene with a desk into an 
# SoWrapperKit.  Then, add a material editor for the desk and 
# a light editor on the light.
# 
# The scene is organized using an SoSceneKit, which contains
# lists for grouping lights (lightList), cameras (cameraList), 
# and objects (childList) in a scene.
# 
# Once the scene is created, a material editor is attached to 
# the wrapperKit's 'material' part, and a directional light editor
# is attached to the light's 'directionalLight' part.
#

import sys

from pivy.coin import *
from pivy.sogui import *

def main():
    # Initialize Inventor and Qt
    myWindow = SoGui.init(sys.argv[0])  
    if myWindow == None: sys.exit(1)     

    # SCENE!
    myScene = SoSceneKit()
    myScene.ref()

    # LIGHTS! Add an SoLightKit to the "lightList." The 
    # SoLightKit creates an SoDirectionalLight by default.
    myScene.setPart("lightList[0]", SoLightKit())

    # CAMERA!! Add an SoCameraKit to the "cameraList." The 
    # SoCameraKit creates an SoPerspectiveCamera by default.
    myScene.setPart("cameraList[0]", SoCameraKit())
    myScene.setCameraNumber(0)

    # Read an object from file. 
    myInput = SoInput()
    if not myInput.openFile("desk.iv"):
        sys.exit(1)
    fileContents = SoDB.readAll(myInput)
    if fileContents == None: 
        sys.exit(1)

    # OBJECT!! Create an SoWrapperKit and set its contents to
    # be what you read from file.
    myDesk =SoWrapperKit()
    myDesk.setPart("contents", fileContents)
    myScene.setPart("childList[0]", myDesk)

    # Give the desk a good starting color
    myDesk.set("material { diffuseColor .8 .3 .1 }")

    # MATERIAL EDITOR!!  Attach it to myDesk's material node.
    # Use the SO_GET_PART macro to get this part from myDesk.
    try:
        mtlEditor = SoGuiMaterialEditor()
    except:
        print "The SoGuiMaterialEditor node has not been implemented in the " + \
              "SoGui bindings of Coin!"
        sys.exit(1)
    mtl = SO_GET_PART(myDesk,"material",SoMaterial())
    mtlEditor.attach(mtl)
    mtlEditor.setTitle("Material of Desk")
    mtlEditor.show()

    # DIRECTIONAL LIGHT EDITOR!! Attach it to the 
    # SoDirectionalLight node within the SoLightKit we made.
    try:
        ltEditor = SoGuiDirectionalLightEditor()
    except:
        print "The SoGuiDirectionalLightEditor node has not been implemented in the " + \
              "SoGui bindings of Coin!"
        sys.exit(1)        
    ltPath = myScene.createPathToPart("lightList[0].light", TRUE)
    ltEditor.attach(ltPath)
    ltEditor.setTitle("Lighting of Desk")
    ltEditor.show()
   
    myRenderArea = SoGuiRenderArea(myWindow)

    # Set up Camera with ViewAll...
    # -- use the SO_GET_PART macro to get the camera node.
    # -- viewall is a method on the 'camera' part of 
    #    the cameraKit, not on the cameraKit itself.  So the part
    #    we ask for is not 'cameraList[0]' (which is of type 
    #    SoPerspectiveCameraKit), but 
    #    'cameraList[0].camera' (which is of type 
    #    SoPerspectiveCamera).
    myCamera = SO_GET_PART(myScene, "cameraList[0].camera", SoPerspectiveCamera())
    myRegion = SbViewportRegion(myRenderArea.getSize())
    myCamera.viewAll(myScene, myRegion)

    myRenderArea.setSceneGraph(myScene)
    myRenderArea.setTitle("Main Window: Desk In A Scene Kit")
    myRenderArea.show()

    SoGui.show(myWindow)
    SoGui.mainLoop()

if __name__ == "__main__":
    main()
