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
# chapter 12, example 2.
#
# Using getTriggerNode/getTriggerField methods of the data
# sensor.
#

from pivy import *
import sys

# Sensor callback function:
def rootChangedCB(void, s):
    # We know the sensor is really a data sensor:
    mySensor = cast(s, "SoDataSensor")

    changedNode = mySensor.getTriggerNode()
    changedField = mySensor.getTriggerField()
    
    print "The node named '%s' changed" % (changedNode.getName().getString())

    if changedField:
        # the getFieldName() method returns a tuple with 2 values in pivy.
        # first argument is an integer (representing the SbBool) and the
        # second is a SbName instance.
        fieldName = changedNode.getFieldName(changedField)[1]
        print " (field %s)" % (fieldName.getString())
    else:
        print " (no fields changed)"

def main():
    SoDB_init()

    root = SoSeparator()
    root.ref()
    root.setName("Root")

    myCube = SoCube()
    root.addChild(myCube)
    myCube.setName("MyCube")

    mySphere = SoSphere()
    root.addChild(mySphere)
    mySphere.setName("MySphere")

    mySensor = SoNodeSensor(rootChangedCB, None)
    mySensor.setPriority(0)
    # mySensor.setFunction(rootChangedCB)
    mySensor.attach(root)

    # Now, make a few changes to the scene graph the sensor's
    # callback function will be called immediately after each
    # change.
    myCube.width(1.0)
    myCube.height(2.0)
    mySphere.radius(3.0)
    root.removeChild(mySphere)

if __name__ == "__main__":
    main()
