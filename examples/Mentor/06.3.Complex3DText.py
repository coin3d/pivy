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
# chapter 6, example 3.
#
# This example renders arguments as text within an
# SoXTExaminerViewer.  It is a little fancier than 6.2.
#

import sys

from pivy.coin import *
from pivy.sogui import *

def main():
    # Initialize Inventor and Qt
    myWindow = SoGui.init(sys.argv[0])
    if myWindow == None: sys.exit(1)

    root = SoGroup()

    # Set up camera 
    myCamera = SoPerspectiveCamera()
    myCamera.position = (0, -(len(sys.argv) - 1) / 2, 10)
    myCamera.nearDistance = 5.0
    myCamera.farDistance = 15.0
    root.addChild(myCamera)

    # Let's make the front of the text white, 
    # and the sides and back shiny yellow
    myMaterial = SoMaterial()
    colors = [SbColor()]*3
    # diffuse
    colors[0].setValue(1, 1, 1)
    colors[1].setValue(1, 1, 0)
    colors[2].setValue(1, 1, 0)
    myMaterial.diffuseColor.setValues(0, 3, colors)

    # specular
    colors[0].setValue(1, 1, 1)
    # Note: Inventor 2.1 doesn't support multiple specular colors.
    # myMaterial.specularColor = colors[0]
    colors[1].setValue(1, 1, 0)
    colors[2].setValue(1, 1, 0)
    myMaterial.specularColor.setValues(0, 3, colors)
    myMaterial.shininess.setValue(.1)
    root.addChild(myMaterial)

    # Choose a font likely to exist.
    myFont = SoFont()
    myFont.name = "Times-Roman"
    root.addChild(myFont)

    # Specify a beveled cross-section for the text
    myProfileCoords = SoProfileCoordinate2()
    coords = [SbVec2f()]*4
    coords[0].setValue( .00, .00)
    coords[1].setValue( .25, .25)
    coords[2].setValue(1.25, .25)
    coords[3].setValue(1.50, .00)
    myProfileCoords.point.setValues(0, 4, coords)
    root.addChild(myProfileCoords)

    myLinearProfile = SoLinearProfile()
    index = (0, 1, 2, 3)
    myLinearProfile.index.setValues(0, 4, index)
    root.addChild(myLinearProfile)

    # Set the material binding to PER_PART
    myMaterialBinding = SoMaterialBinding()
    myMaterialBinding.value = SoMaterialBinding.PER_PART
    root.addChild(myMaterialBinding)

    # Add the text
    myText3 = SoText3()
    myText3.string = "Beveled Text"
    myText3.justification = SoText3.CENTER
    myText3.parts = SoText3.ALL
   
    root.addChild(myText3)

    myViewer = SoGuiExaminerViewer(myWindow)
    myViewer.setSceneGraph(root)
    myViewer.setTitle("Complex 3D Text")
    myViewer.show()
    myViewer.viewAll()

    SoGui.show(myWindow)
    SoGui.mainLoop()

if __name__ == "__main__":
    main()
