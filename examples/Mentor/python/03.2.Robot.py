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
# chapter 3, example 2.
#
# This code shows how to create a robot out of various nodes.
# It introduces shared instancing of nodes to create two legs
# using two instances of the same subgraph.
#

from sogui import *
from pivy import *
import sys

def makeRobot():
##############################################################
# CODE FOR The Inventor Mentor STARTS HERE
    # Robot with legs

    # Construct parts for legs (thigh, calf and foot)
    thigh = SoCube()
    thigh.width(1.2)
    thigh.height(2.2)
    thigh.depth(1.1)
    
    calfTransform = SoTransform()
    calfTransform.translation.setValue(0, -2.25, 0.0)
    
    calf = SoCube()
    calf.width(1)
    calf.height(2.2)
    calf.depth(1)

    footTransform = SoTransform()
    footTransform.translation.setValue(0, -1.5, .5)

    foot = SoCube()
    foot.width(0.8)
    foot.height(0.8)
    foot.depth(2)

    # Put leg parts together
    leg = SoGroup()
    leg.addChild(thigh)
    leg.addChild(calfTransform)
    leg.addChild(calf)
    leg.addChild(footTransform)
    leg.addChild(foot)
    
    leftTransform = SoTransform()
    leftTransform.translation.setValue(1, -4.25, 0)
    
    # Left leg
    leftLeg = SoSeparator()
    leftLeg.addChild(leftTransform)
    leftLeg.addChild(leg)
    
    rightTransform = SoTransform()
    rightTransform.translation.setValue(-1, -4.25, 0)
    
    # Right leg
    rightLeg = SoSeparator()
    rightLeg.addChild(rightTransform)
    rightLeg.addChild(leg)
    
    # Parts for body
    bodyTransform = SoTransform()
    bodyTransform.translation.setValue(0.0, 3.0, 0.0)
    
    bronze = SoMaterial()
    bronze.ambientColor.setValue(.33, .22, .27)
    bronze.diffuseColor.setValue(.78, .57, .11)
    bronze.specularColor.setValue(.99, .94, .81)
    bronze.shininess(.28)
    
    bodyCylinder = SoCylinder()
    bodyCylinder.radius(2.5)
    bodyCylinder.height(6)
    
    # Construct body out of parts 
    body = SoSeparator()
    body.addChild(bodyTransform)      
    body.addChild(bronze)
    body.addChild(bodyCylinder)
    body.addChild(leftLeg)
    body.addChild(rightLeg)
    
    # Head parts
    headTransform = SoTransform()
    headTransform.translation.setValue(0, 7.5, 0)
    headTransform.scaleFactor.setValue(1.5, 1.5, 1.5)
    
    silver = SoMaterial()
    silver.ambientColor.setValue(.2, .2, .2)
    silver.diffuseColor.setValue(.6, .6, .6)
    silver.specularColor.setValue(.5, .5, .5)
    silver.shininess(.5)
    
    headSphere = SoSphere()
    
    # Construct head
    head = SoSeparator()
    head.addChild(headTransform)
    head.addChild(silver)
    head.addChild(headSphere)
    
    # Robot is just head and body
    robot = SoSeparator()
    robot.addChild(body)               
    robot.addChild(head)
    
# CODE FOR The Inventor Mentor ENDS HERE
##############################################################

    return robot


def main():
    # Initialize Inventor and Qt
    myWindow = SoGui.init(sys.argv[0])
    if myWindow == None: sys.exit(1)

    root = SoSeparator()
    root.ref()
    
    # This function contains our code fragment.
    root.addChild(makeRobot())
    
    myViewer = SoGuiExaminerViewer(myWindow)
    myViewer.setSceneGraph(root)
    myViewer.setTitle("Robot")
    myViewer.show()
    myViewer.viewAll()

    SoGui.show(myWindow)
    SoGui.mainLoop()

if __name__ == "__main__":
    main()



