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
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES LOSS OF USE,
# DATA, OR PROFITS OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

###
# This is an example from the Inventor Mentor,
# chapter 6, example 1.
#
# This example renders a globe and uses 2D text to label the
# continents Africa and Asia.
#

import sys

from pivy.coin import *
from pivy.sogui import *

def main():
    # Initialize Inventor and Qt
    myWindow = SoGui.init(sys.argv[0])
    if myWindow == None: sys.exit(1)

    root = SoGroup()
    root.ref()

    # Choose a font
    myFont = SoFont()
    myFont.name = "Times-Roman"
    myFont.size = 24.0
    root.addChild(myFont)

    # Add the globe, a sphere with a texture map.
    # Put it within a separator.
    sphereSep = SoSeparator()
    myTexture2 = SoTexture2()
    sphereComplexity = SoComplexity()
    sphereComplexity.value = 0.55
    root.addChild(sphereSep)
    sphereSep.addChild(myTexture2)
    sphereSep.addChild(sphereComplexity)
    sphereSep.addChild(SoSphere())
    myTexture2.filename = "globe.rgb"

    # Add Text2 for AFRICA, translated to proper location.
    africaSep = SoSeparator()
    africaTranslate = SoTranslation()
    africaText = SoText2()
    africaTranslate.translation = (.25,.0,1.25)
    africaText.string = "AFRICA"
    root.addChild(africaSep)
    africaSep.addChild(africaTranslate)
    africaSep.addChild(africaText)

    # Add Text2 for ASIA, translated to proper location.
    asiaSep = SoSeparator()
    asiaTranslate = SoTranslation()
    asiaText = SoText2()
    asiaTranslate.translation = (.8,.8,0)
    asiaText.string = "ASIA"
    root.addChild(asiaSep)
    asiaSep.addChild(asiaTranslate)
    asiaSep.addChild(asiaText)

    myViewer = SoGuiExaminerViewer(myWindow)
    myViewer.setSceneGraph(root)
    myViewer.setTitle("2D Text")

    # In Inventor 2.1, if the machine does not have hardware texture
    # mapping, we must override the default drawStyle to display textures.
    myViewer.setDrawStyle(SoGuiViewer.STILL, SoGuiViewer.VIEW_AS_IS)

    myViewer.show()
    myViewer.viewAll()

    SoGui.show(myWindow)
    SoGui.mainLoop()

if __name__ == "__main__":
    main()
