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
# chapter 7, example 3.
#
# This example illustrates using texture functions to
# generate texture coordinates on a sphere.
# It draws three texture mapped spheres, each with a 
# different repeat frequency as defined by the fields of the 
# SoTextureCoordinatePlane node.
#

from pivy import *
import sys

def main():
    # Initialize Inventor and Qt
    myWindow = SoQt_init(sys.argv[0])
    if myWindow == None: sys.exit(1)

    root = SoSeparator()
    root.ref()

    # Choose a texture.
    faceTexture = SoTexture2()
    root.addChild(faceTexture)
    faceTexture.filename.setValue("sillyFace.rgb")

    # Make the diffuse color pure white
    myMaterial = SoMaterial()
    myMaterial.diffuseColor.setValue(1,1,1)
    root.addChild(myMaterial)

    # This texture2Transform centers the texture about (0,0,0) 
    myTexXf = SoTexture2Transform()
    myTexXf.translation.setValue(.5,.5)
    root.addChild(myTexXf)

    # Define a texture coordinate plane node.  This one will 
    # repeat with a frequency of two times per unit length.
    # Add a sphere for it to affect.
    texPlane1 = SoTextureCoordinatePlane()
    texPlane1.directionS.setValue(SbVec3f(2,0,0))
    texPlane1.directionT.setValue(SbVec3f(0,2,0))
    root.addChild(texPlane1)
    root.addChild(SoSphere())

    # A translation node for spacing the three spheres.
    myTranslation = SoTranslation()
    myTranslation.translation.setValue(2.5,0,0)

    # Create a second sphere with a repeat frequency of 1.
    texPlane2 = SoTextureCoordinatePlane()
    texPlane2.directionS.setValue(SbVec3f(1,0,0))
    texPlane2.directionT.setValue(SbVec3f(0,1,0))
    root.addChild(myTranslation)
    root.addChild(texPlane2)
    root.addChild(SoSphere())

    # The third sphere has a repeat frequency of .5
    texPlane3 = SoTextureCoordinatePlane()
    texPlane3.directionS.setValue(SbVec3f(.5,0,0))
    texPlane3.directionT.setValue(SbVec3f(0,.5,0))
    root.addChild(myTranslation)
    root.addChild(texPlane3)
    root.addChild(SoSphere())

    myViewer = SoQtExaminerViewer(myWindow)
    myViewer.setSceneGraph(root)
    myViewer.setTitle("Texture Coordinate Plane")

    # In Inventor 2.1, if the machine does not have hardware texture
    # mapping, we must override the default drawStyle to display textures.
    myViewer.setDrawStyle(SoQtViewer.STILL, SoQtViewer.VIEW_AS_IS)
    
    myViewer.show()
    myViewer.viewAll()
    
    SoQt_show(myWindow)
    SoQt_mainLoop()

if __name__ == "__main__":
    main()
