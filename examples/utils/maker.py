#!/usr/bin/env python

###
# Copyright (c) 2002-2007 Systems in Motion
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

###
# This is an example from the Inventor Mentor,
# chapter 2, example 1.
#
# Hello Cone example program; draws a red cone in a window.
#

import sys

from pivy.sogui import *
from pivy.coin import *

def main():
    # Initialize Inventor. This returns a main window to use.
    # If unsuccessful, exit.

    myWindow = SoGui.init(sys.argv[0])
    if myWindow == None: sys.exit(1)

    # Make a scene containing a red cone
    root = SoSeparator()

    SoMarkerSet.CUSTOM_BIT_MAP = 99
    bitmap = b'O'
    SoMarkerSet.addMarker(SoMarkerSet.CUSTOM_BIT_MAP, SbVec2s([20,20]), bitmap)
    color = SoMaterial()
    color.diffuseColor = (1., 0., 0.)

    marker = SoMarkerSet()
    marker.markerIndex = SoMarkerSet.CUSTOM_BIT_MAP
    data = SoCoordinate3()
    data.point.setValue(0, 0, 0)
    data.point.setValues(0, 1, [[5., 5., 0.]])

    myCamera = SoPerspectiveCamera()
    root.addChild(myCamera)
    root.addChild(SoDirectionalLight())
    root.addChild(color)
    root.addChild(data)
    root.addChild(marker)
    root.addChild(SoCone())

    myRenderArea = SoGuiRenderArea(myWindow)

    myCamera.viewAll(root, myRenderArea.getViewportRegion())

    myRenderArea.setSceneGraph(root)
    myRenderArea.setTitle("Hello Cone")
    myRenderArea.show()

    SoGui.show(myWindow)
    SoGui.mainLoop()

if __name__ == "__main__":
    main()