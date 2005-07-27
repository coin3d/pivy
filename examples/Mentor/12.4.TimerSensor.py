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
# chapter 12, example 4.
#
# Timer sensors.  An object is rotated by a timer sensor.
# (called "rotatingSensor").  The interval between calls 
# controls how often it rotates.
# A second timer (called "schedulingSensor") goes off
# every 5 seconds and changes the interval of 
# "rotatingSensor".  The interval alternates between
# once per second and 10 times per second.
# This example could also be done using engines.
#

import sys

from pivy.coin import *
from pivy.sogui import *

###########################################################
# CODE FOR The Inventor Mentor STARTS HERE

# This function is called either 10 times/second or once every
# second the scheduling changes every 5 seconds (see below):
def rotatingSensorCallback(data, sensor):
    # Rotate an object...
    myRotation = cast(data, "SoRotation")
    currentRotation = myRotation.rotation.getValue()
    currentRotation *= SbRotation(SbVec3f(0,0,1), M_PI/90.0)
    myRotation.rotation.setValue(currentRotation)

# This function is called once every 5 seconds, and
# reschedules the other sensor.
def schedulingSensorCallback(data, sensor):
    rotatingSensor = cast(data, "SoTimerSensor")
    rotatingSensor.unschedule()
    if rotatingSensor.getInterval() == 1.0:
        rotatingSensor.setInterval(1.0/10.0)
    else: rotatingSensor.setInterval(1.0)
    rotatingSensor.schedule()

# CODE FOR The Inventor Mentor ENDS HERE
###########################################################

def main():
    if len(sys.argv) != 2:
        print >> sys.stderr, "Usage: %s filename.iv" % (sys.argv[0])
        sys.exit(1)

    myWindow = SoGui.init(sys.argv[0])
    if myWindow == None: sys.exit(1)

    root = SoSeparator()
    root.ref()
   
###########################################################   
# CODE FOR The Inventor Mentor STARTS HERE

    myRotation = SoRotation()
    root.addChild(myRotation)

    rotatingSensor = SoTimerSensor(rotatingSensorCallback, myRotation)
    rotatingSensor.setInterval(1.0) # scheduled once per second
    rotatingSensor.schedule()

    schedulingSensor = SoTimerSensor(schedulingSensorCallback, rotatingSensor)
    schedulingSensor.setInterval(5.0) # once per 5 seconds
    schedulingSensor.schedule()

# CODE FOR The Inventor Mentor ENDS HERE
###########################################################

    inputFile = SoInput()
    if inputFile.openFile(sys.argv[1]) == 0:
        print >> sys.stderr, "Could not open file %s" % (sys.argv[1])
        sys.exit(1)
        
    root.addChild(SoDB.readAll(inputFile))

    myViewer = SoGuiExaminerViewer(myWindow)
    myViewer.setSceneGraph(root)
    myViewer.setTitle("Two Timers")
    myViewer.show()

    SoGui.show(myWindow)  # Display main window
    SoGui.mainLoop()        # Main Inventor event loop

if __name__ == "__main__":
    main()
