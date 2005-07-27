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
# chapter 9, example 3.
#
# Search Action example.
# Read in a scene from a file.
# Search through the scene looking for a light.
# If none exists, add a directional light to the scene
# and print out the modified scene.
#

import sys

from pivy.coin import *

def main():
    # Initialize Inventor
    SoDB.init()
    
    # Open and read input scene graph
    sceneInput = SoInput()
    if not sceneInput.openFile("bird.iv"):
        return 1

    root = SoDB.readAll(sceneInput)
    if root == None:
        return 1
    root.ref()

##############################################################
# CODE FOR The Inventor Mentor STARTS HERE

    mySearchAction = SoSearchAction()

    # Look for first existing light derived from class SoLight
    mySearchAction.setType(SoLight.getClassTypeId())
    mySearchAction.setInterest(SoSearchAction.FIRST)
    
    mySearchAction.apply(root)
    if mySearchAction.getPath() == None: # No lights found
        # Add a default directional light to the scene
        myLight = SoDirectionalLight()
        root.insertChild(myLight, 0)

# CODE FOR The Inventor Mentor ENDS HERE
##############################################################

    myWriteAction = SoWriteAction()
    myWriteAction.apply(root)

    root.unref()
    return 0

if __name__ == "__main__":
    sys.exit(main())
