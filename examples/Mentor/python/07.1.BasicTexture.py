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
#     the documentation and#or other materials provided with the
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
# chapter 7, example 1.
#
# This example displays a textured cube (default 
# texture coords).
#

from pivy import *
import sys

def main():
    # Initialize Inventor and Qt
    myWindow = SoQt_init(sys.argv[0])
    if myWindow == None: sys.exit(1)

    root = SoSeparator()
    root.ref()

    # Choose a texture 
    rock = SoTexture2()
    root.addChild(rock)
    rock.filename.setValue("brick.1.rgb")

    # Make a cube
    root.addChild(SoCube())

    myViewer = SoQtExaminerViewer(myWindow)
    myViewer.setSceneGraph(root)
    myViewer.setTitle("Default Texture Coords")

    # In Inventor 2.1, if the machine does not have hardware texture
    # mapping, we must override the default drawStyle to display textures.
    myViewer.setDrawStyle(SoQtViewer.STILL, SoQtViewer.VIEW_AS_IS)
    
    myViewer.show()
    myViewer.viewAll()
    
    SoQt_show(myWindow)
    SoQt_mainLoop()

if __name__ == "__main__":
    main()
