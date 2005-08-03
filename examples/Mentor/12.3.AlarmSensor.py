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
# chapter 12, example 3.
#
# Alarm sensor that raises a flag after 10 minutes
#

import sys

from pivy.coin import *
from pivy.sogui import *

###########################################################
# CODE FOR The Inventor Mentor STARTS HERE

def raiseFlagCallback(data, sensor):
    # We know data is really a SoTransform node:
    flagAngleXform = cast(data, "SoTransform")

    # Rotate flag by 90 degrees about the Z axis:
    flagAngleXform.rotation.setValue(SbVec3f(0,0,1), M_PI/2)

# CODE FOR The Inventor Mentor ENDS HERE
###########################################################


def main():
    myWindow = SoGui.init(sys.argv[0]) # pass the app name
    if myWindow == None: sys.exit(1)

###########################################################
# CODE FOR The Inventor Mentor STARTS HERE

    flagXform = SoTransform()

    # Create an alarm that will call the flag-raising callback:
    myAlarm = SoAlarmSensor(raiseFlagCallback, flagXform)
    myAlarm.setTimeFromNow(12.0)  # 12 seconds
    myAlarm.schedule()

# CODE FOR The Inventor Mentor ENDS HERE
###########################################################

    root = SoSeparator()
    root.ref()
    root.addChild(flagXform)
    myCone = SoCone()
    myCone.bottomRadius = 0.1
    root.addChild(myCone)

    myViewer = SoGuiExaminerViewer(myWindow)

    # Put our scene in myViewer, change the title
    myViewer.setSceneGraph(root)
    myViewer.setTitle("Raise The Cone")
    myViewer.show()

    SoGui.show(myWindow)  # Display main window
    SoGui.mainLoop()      # Main Inventor event loop

if __name__ == "__main__":
    main()
