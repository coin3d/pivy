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
# chapter 13, example 9.
#
# Blinker node.
# Use a blinker node to flash a neon ad sign on and off
#

from sogui import *
from pivy import *
import sys

def main():
    # Initialize Inventor and Qt
    myWindow = SoGui.init(sys.argv[0])  
    if myWindow == None: sys.exit(1)     

    # Set up camera and light
    root = SoSeparator()
    root.ref()
    myCamera = SoPerspectiveCamera()
    root.addChild(myCamera)
    root.addChild(SoDirectionalLight())

    # Read in the parts of the sign from a file
    myInput = SoInput()
    if not myInput.openFile("eatAtJosies.iv"):
        sys.exit(1)
    fileContents = SoDB.readAll(myInput)
    if fileContents == None:
        sys.exit(1)

    eatAt = SoNode.getByName("EatAt")
    josie = SoNode.getByName("Josies")
    frame = SoNode.getByName("Frame")

#############################################################
# CODE FOR The Inventor Mentor STARTS HERE

    # Add the non-blinking part of the sign to the root
    root.addChild(eatAt)
   
    # Add the fast-blinking part to a blinker node
    fastBlinker = SoBlinker()
    root.addChild(fastBlinker)
    fastBlinker.speed(2)  # blinks 2 times a second
    fastBlinker.addChild(josie)

    # Add the slow-blinking part to another blinker node
    slowBlinker = SoBlinker()
    root.addChild(slowBlinker)
    slowBlinker.speed(0.5)  # 2 secs per cycle 1 on, 1 off
    slowBlinker.addChild(frame)

# CODE FOR The Inventor Mentor ENDS HERE
#############################################################

    # Set up and display render area 
    myRenderArea = SoGuiRenderArea(myWindow)
    myRegion = SbViewportRegion(myRenderArea.getSize()) 
    myCamera.viewAll(root, myRegion)

    myRenderArea.setSceneGraph(root)
    myRenderArea.setTitle("Neon")
    myRenderArea.show()
    SoGui.show(myWindow)
    SoGui.mainLoop()

if __name__ == "__main__":
    main()
