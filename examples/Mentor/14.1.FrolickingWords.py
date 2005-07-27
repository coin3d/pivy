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
# This is an example from the Inventor Mentor.
# chapter 14, example 1.
#
# Use SoShapeKits to create two 3-D words, "NICE" and "HAPPY"
# Use nodekit methods to access the fields of the "material"
# and "transform" parts.
# Use a calculator engine and an elapsed time engine to make
# the words change color and fly about the screen.
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

    # Create shape kits with the words "HAPPY" and "NICE"
    happyKit = SoShapeKit()
    root.addChild(happyKit)
    happyKit.setPart("shape", SoText3())
    happyKit.set("shape { parts ALL string \"HAPPY\"}")
    happyKit.set("font { size 2}")

    niceKit = SoShapeKit()
    root.addChild(niceKit)
    niceKit.setPart("shape", SoText3())
    niceKit.set("shape { parts ALL string \"NICE\"}")
    niceKit.set("font { size 2}")

    # Create the Elapsed Time engine
    myTimer = SoElapsedTime()
    myTimer.ref()

    # Create two calculator - one for HAPPY, one for NICE.
    happyCalc = SoCalculator()
    happyCalc.ref()
    happyCalc.a.connectFrom(myTimer.timeOut)
    happyCalc.expression("ta=cos(2*a); tb=sin(2*a);"
                         "oA = vec3f(3*pow(ta,3),3*pow(tb,3),1);"
                         "oB = vec3f(fabs(ta)+.1,fabs(.5*fabs(tb))+.1,1);"
                         "oC = vec3f(fabs(ta),fabs(tb),.5)")

    # The second calculator uses different arguments to
    # sin() and cos(), so it moves out of phase.
    niceCalc = SoCalculator()
    niceCalc.ref()
    niceCalc.a.connectFrom(myTimer.timeOut)
    niceCalc.expression("ta=cos(2*a+2); tb=sin(2*a+2);"
                        "oA = vec3f(3*pow(ta,3),3*pow(tb,3),1);"
                        "oB = vec3f(fabs(ta)+.1,fabs(.5*fabs(tb))+.1,1);"
                        "oC = vec3f(fabs(ta),fabs(tb),.5)")

    # Connect the transforms from the calculators...
    happyXf = happyKit.getPart("transform",TRUE)
    happyXf.translation.connectFrom(happyCalc.oA)
    happyXf.scaleFactor.connectFrom(happyCalc.oB)
    niceXf = niceKit.getPart("transform",TRUE)
    niceXf.translation.connectFrom(niceCalc.oA)
    niceXf.scaleFactor.connectFrom(niceCalc.oB)

    # Connect the materials from the calculators...
    happyMtl = happyKit.getPart("material",TRUE)
    happyMtl.diffuseColor.connectFrom(happyCalc.oC)
    niceMtl = niceKit.getPart("material",TRUE)
    niceMtl.diffuseColor.connectFrom(niceCalc.oC)

    myViewer = SoGuiExaminerViewer(myWindow)
    myViewer.setSceneGraph(root)
    myViewer.setTitle("Frolicking Words")
    myViewer.viewAll()
    myViewer.show()

    SoGui.show(myWindow)
    SoGui.mainLoop()

if __name__ == "__main__":
    main()
