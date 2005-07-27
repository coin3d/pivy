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
# chapter 13, example 8.
#
# Rotor node example.  
# Read in the tower and vanes of a windmill from a file.
# Use a rotor node to rotate the vanes.
#

import sys

from pivy.coin import *
from pivy.sogui import *

def readFile(filename):
    # Open the input file
    mySceneInput = SoInput()
    if not mySceneInput.openFile(filename):
        print >> sys.stderr, "Cannot open file %s" % (filename)
        return None

    # Read the whole file into the database
    myGraph = SoDB.readAll(mySceneInput)
    if myGraph == None:
        print >> sys.stderr, "Problem reading file"
        return None

    mySceneInput.closeFile()
    return myGraph

def main():
    # Initialize Inventor and Qt
    myWindow = SoGui.init(sys.argv[0])  
    if myWindow == None: sys.exit(1)     

    root = SoSeparator()
    root.ref()

    # Read in the data for the windmill tower
    windmillTower = readFile("windmillTower.iv")
    root.addChild(windmillTower)

    # Add a rotor node to spin the vanes
    myRotor = SoRotor()
    myRotor.rotation.setValue(SbVec3f(0, 0, 1), 0) # z axis
    myRotor.speed(0.2)
    root.addChild(myRotor)

    # Read in the data for the windmill vanes
    windmillVanes = readFile("windmillVanes.iv")
    root.addChild(windmillVanes)

    # Create a viewer
    myViewer = SoGuiExaminerViewer(myWindow)

    # attach and show viewer
    myViewer.setSceneGraph(root)
    myViewer.setTitle("Windmill")
    myViewer.show()

    SoDB.setRealTimeInterval(1/120.0)
    
    # Loop forever
    SoGui.show(myWindow)
    SoGui.mainLoop()

if __name__ == "__main__":
    main()
