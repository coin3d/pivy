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
# chapter 16, example 1.
#
# This example shows how to use the overlay planes with the
# viewer components. By default color 0 is used for the
# overlay planes background color (clear color), so we use
# color 1 for the object. This example also shows how to
# load the overlay color map with the wanted color.
#

from sogui import *
from pivy import *
import sys

overlayScene = """
#Inventor V2.0 ascii

Separator {
   OrthographicCamera {
      position 0 0 5
      nearDistance 1.0
      farDistance 10.0
      height 1
   }
   LightModel { model BASE_COLOR }
   ColorIndex { index 1 }
   Coordinate3 { point [ -1 -1 0, -1 1 0, 1 1 0, 1 -1 0] }
   FaceSet {}
}"""

def main():
    # Initialize Inventor and Qt
    myWindow = SoGui.init(sys.argv[0])  
    if myWindow == None: sys.exit(1)     

    # read the scene graph in
    input = SoInput()
    input.setBuffer(overlayScene)
    scene = SoDB_readAll(input)
    if scene == None:
        print "Couldn't read scene"
        sys.exit(1)

    # Allocate the viewer, set the overlay scene and
    # load the overlay color map with the wanted color.
    color = SbColor(.5, 1, .5)
    myViewer = SoGuiExaminerViewer(myWindow)
    myViewer.setSceneGraph(SoCone())
    myViewer.setOverlaySceneGraph(scene)
    myViewer.setOverlayColorMap(1, 1, color)
    myViewer.setTitle("Overlay Plane")
   
    # Show the viewer and loop forever
    myViewer.show()
    # QtRealizeWidget(myWindow)
    SoGui.mainLoop()

if __name__ == "__main__":
    main()
