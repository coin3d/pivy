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
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES LOSS OF USE,
# DATA, OR PROFITS OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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

from pivy.coin import *
from pivy.sogui import *

def main():
    # Initialize Inventor and Qt
    myWindow = SoGui.init(sys.argv[0])
    if myWindow == None: sys.exit(1)

    root = SoSeparator()
    root.ref()

    # Create two separators, for left and right objects.
    leftSep = SoSeparator()
    rightSep = SoSeparator()
    root.addChild(leftSep)
    root.addChild(rightSep)

    # Create the transformation nodes
    leftTranslation  = SoTranslation()
    rightTranslation = SoTranslation()
    myRotation = SoRotationXYZ()
    myScale = SoScale()

    # Fill in the values
    leftTranslation.translation.setValue(-1.0, 0.0, 0.0)
    rightTranslation.translation.setValue(1.0, 0.0, 0.0)
    myRotation.angle(M_PI/2)   # 90 degrees
    myRotation.axis(SoRotationXYZ.X)
    myScale.scaleFactor.setValue(2., 1., 3.)

    # Add transforms to the scene.
    leftSep.addChild(leftTranslation)   # left graph
    leftSep.addChild(myRotation)        # then rotated
    leftSep.addChild(myScale)           # first scaled

    rightSep.addChild(rightTranslation) # right graph
    rightSep.addChild(myScale)          # then scaled
    rightSep.addChild(myRotation)       # first rotated

    # Read an object from file. (as in example 4.2.Lights)
    myInput = SoInput()
    if not myInput.openFile("temple.iv"):
        sys.exit(1)

    fileContents = SoDB.readAll(myInput)
    if fileContents == None: 
        sys.exit(1)

    # Add an instance of the object under each separator.
    leftSep.addChild(fileContents)
    rightSep.addChild(fileContents)

    # Construct a renderArea and display the scene.
    myViewer = SoGuiExaminerViewer(myWindow)
    myViewer.setSceneGraph(root)
    myViewer.setTitle("Transform Ordering")
    myViewer.show()
    myViewer.viewAll()

    SoGui.show(myWindow)
    SoGui.mainLoop()

if __name__ == "__main__":
    main()
