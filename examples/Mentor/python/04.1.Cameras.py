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
# chapter 4, example 1.
#
# Camera example.  
# A blinker node is used to switch between three 
# different views of the same scene. The cameras are 
# switched once per second.
#

from pivy import *
import sys

def main():
    # Initialize Inventor and Qt
    myWindow = SoQt_init(sys.argv[0])
    if myWindow == None: sys.exit(1)

    root = SoSeparator()
    root.ref()

    # Create a blinker node and put it in the scene. A blinker
    # switches between its children at timed intervals.
    myBlinker = SoBlinker()
    root.addChild(myBlinker)

    # Create three cameras. Their positions will be set later.
    # This is because the viewAll method depends on the size
    # of the render area, which has not been created yet.
    orthoViewAll = SoOrthographicCamera()
    perspViewAll = SoPerspectiveCamera()
    perspOffCenter = SoPerspectiveCamera()
    myBlinker.addChild(orthoViewAll)
    myBlinker.addChild(perspViewAll)
    myBlinker.addChild(perspOffCenter)

    # Create a light
    root.addChild(SoDirectionalLight())

    # Read the object from a file and add to the scene
    myInput = SoInput()
    if not myInput.openFile("parkbench.iv"):
        sys.exit(1)

    fileContents = SoDB_readAll(myInput)
    if fileContents == None:
        sys.exit(1)

    myMaterial = SoMaterial()
    myMaterial.diffuseColor.setValue(0.8, 0.23, 0.03) 
    root.addChild(myMaterial)
    root.addChild(fileContents)

    myRenderArea = SoQtRenderArea(myWindow)

    # Establish camera positions. 
    # First do a viewAll on all three cameras.  
    # Then modify the position of the off-center camera.
    myRegion = SbViewportRegion(myRenderArea.getSize())
    orthoViewAll.viewAll(root, myRegion)
    perspViewAll.viewAll(root, myRegion)
    perspOffCenter.viewAll(root, myRegion)
    initialPos = perspOffCenter.position.getValue()
    x,y,z = initialPos.getValue()
    perspOffCenter.position.setValue(x+x/2., y+y/2., z+z/4.)

    myRenderArea.setSceneGraph(root)
    myRenderArea.setTitle("Cameras")
    myRenderArea.show()

    SoQt_show(myWindow)
    SoQt_mainLoop()

if __name__ == "__main__":
    main()
