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
# chapter 13, example 7.
#
# A calculator engine computes a closed, planar curve.
# The output from the engine is connected to the translation
# applied to a flower object, which consequently moves
# along the path of the curve.
#

from sogui import *
from pivy import *
import sys

def main():
    # Initialize Inventor and Qt
    myWindow = SoGui.init(sys.argv[0])  
    if myWindow == None: sys.exit(1)     

    root = SoSeparator()
    root.ref()

    # Add a camera and light
    myCamera = SoPerspectiveCamera()
    myCamera.position.setValue(-0.5, -3.0, 19.0)
    myCamera.nearDistance(10.0)
    myCamera.farDistance(26.0)
    root.addChild(myCamera)
    root.addChild(SoDirectionalLight())

    # Rotate scene slightly to get better view
    globalRotXYZ = SoRotationXYZ()
    globalRotXYZ.axis(SoRotationXYZ.X)
    globalRotXYZ.angle(M_PI/7)
    root.addChild(globalRotXYZ)

    # Read the background path from a file and add to the group
    myInput = SoInput()
    if not myInput.openFile("flowerPath.iv"):
        sys.exit(1)
    flowerPath = SoDB.readAll(myInput)
    if flowerPath == None: sys.exit(1)
    root.addChild(flowerPath)

#############################################################
# CODE FOR The Inventor Mentor STARTS HERE  

    # Flower group
    flowerGroup = SoSeparator()
    root.addChild(flowerGroup)

    # Read the flower object from a file and add to the group
    if not myInput.openFile("flower.iv"):
        sys.exit(1)
    flower= SoDB.readAll(myInput)
    if flower == None: sys.exit(1)

    # Set up the flower transformations
    danceTranslation = SoTranslation()
    initialTransform = SoTransform()
    flowerGroup.addChild(danceTranslation)
    initialTransform.scaleFactor.setValue(10., 10., 10.)
    initialTransform.translation.setValue(0., 0., 5.)
    flowerGroup.addChild(initialTransform)
    flowerGroup.addChild(flower)

    # Set up an engine to calculate the motion path:
    # r = 5*cos(5*theta) x = r*cos(theta) z = r*sin(theta)
    # Theta is incremented using a time counter engine,
    # and converted to radians using an expression in
    # the calculator engine.
    calcXZ = SoCalculator()
    thetaCounter = SoTimeCounter()

    thetaCounter.max(360)
    thetaCounter.step(4)
    thetaCounter.frequency(0.075)

    calcXZ.a.connectFrom(thetaCounter.output)    
    calcXZ.expression.set1Value(0, "ta=a*M_PI/180") # theta
    calcXZ.expression.set1Value(1, "tb=5*cos(5*ta)") # r
    calcXZ.expression.set1Value(2, "td=tb*cos(ta)") # x 
    calcXZ.expression.set1Value(3, "te=tb*sin(ta)") # z 
    calcXZ.expression.set1Value(4, "oA=vec3f(td,0,te)") 
    danceTranslation.translation.connectFrom(calcXZ.oA)

# CODE FOR The Inventor Mentor ENDS HERE
#############################################################

    myRenderArea = SoGuiRenderArea(myWindow)
    myRenderArea.setSceneGraph(root)
    myRenderArea.setTitle("Flower Dance")
    myRenderArea.show()

    SoGui.show(myWindow)
    SoGui.mainLoop()

if __name__ == "__main__":
    main()
