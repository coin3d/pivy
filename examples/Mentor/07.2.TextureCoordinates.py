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
# This is an example from the Inventor Mentor
# chapter 7, example 2.
#
# This example illustrates using texture coordindates on
# a Face Set.
#

from sogui import *
from pivy import *
import sys

# set this variable to 0 if you want to use the other method
IV_STRICT = 1

def main():
    # Initialize Inventor and Qt
    myWindow = SoGui.init(sys.argv[0])
    if myWindow == None: sys.exit(1)

    root = SoSeparator()
    root.ref()
    
    # Choose a texture
    brick = SoTexture2()
    root.addChild(brick)
    brick.filename.setValue("brick.1.rgb")

    if IV_STRICT:
        # This is the preferred code for Inventor 2.1 

        # Using the new SoVertexProperty node is more efficient
        myVertexProperty = SoVertexProperty()

        # Define the square's spatial coordinates
        myVertexProperty.vertex.set1Value(0, SbVec3f(-3, -3, 0))
        myVertexProperty.vertex.set1Value(1, SbVec3f( 3, -3, 0))
        myVertexProperty.vertex.set1Value(2, SbVec3f( 3,  3, 0))
        myVertexProperty.vertex.set1Value(3, SbVec3f(-3,  3, 0))

        # Define the square's normal
        myVertexProperty.normal.set1Value(0, SbVec3f(0, 0, 1))

        # Define the square's texture coordinates
        myVertexProperty.texCoord.set1Value(0, SbVec2f(0, 0))
        myVertexProperty.texCoord.set1Value(1, SbVec2f(1, 0))
        myVertexProperty.texCoord.set1Value(2, SbVec2f(1, 1))
        myVertexProperty.texCoord.set1Value(3, SbVec2f(0, 1))

        # SoTextureCoordinateBinding node is now obsolete--in Inventor 2.1,
        # texture coordinates will always be generated if none are 
        # provided.
        #
        # tBind = SoTextureCoordinateBinding()
        # root.addChild(tBind)
        # tBind.value(SoTextureCoordinateBinding.PER_VERTEX)
        #
        # Define normal binding
        myVertexProperty.normalBinding(SoNormalBinding.OVERALL)

        # Define a FaceSet
        myFaceSet = SoFaceSet()
        root.addChild(myFaceSet)
        myFaceSet.numVertices.set1Value(0, 4)

        myFaceSet.vertexProperty.setValue(myVertexProperty)

    else:
        # Define the square's spatial coordinates
        coord = SoCoordinate3()
        root.addChild(coord)
        coord.point.set1Value(0, SbVec3f(-3, -3, 0))
        coord.point.set1Value(1, SbVec3f( 3, -3, 0))
        coord.point.set1Value(2, SbVec3f( 3,  3, 0))
        coord.point.set1Value(3, SbVec3f(-3,  3, 0))

        # Define the square's normal
        normal = SoNormal()
        root.addChild(normal)
        normal.vector.set1Value(0, SbVec3f(0, 0, 1))

        # Define the square's texture coordinates
        texCoord = SoTextureCoordinate2()
        root.addChild(texCoord)
        texCoord.point.set1Value(0, SbVec2f(0, 0))
        texCoord.point.set1Value(1, SbVec2f(1, 0))
        texCoord.point.set1Value(2, SbVec2f(1, 1))
        texCoord.point.set1Value(3, SbVec2f(0, 1))

        # Define normal binding
        nBind = SoNormalBinding()
        root.addChild(nBind)
        nBind.value.setValue(SoNormalBinding.OVERALL)

        # SoTextureCoordinateBinding node is now obsolete--in Inventor 2.1,
        # texture coordinates will always be generated if none are 
        # provided.
        #
        # tBind = SoTextureCoordinateBinding()
        # root.addChild(tBind)
        # tBind.value.setValue(SoTextureCoordinateBinding.PER_VERTEX)
        #

        # Define a FaceSet
        myFaceSet = SoFaceSet()
        root.addChild(myFaceSet)
        myFaceSet.numVertices.set1Value(0, 4)

    myViewer = SoGuiExaminerViewer(myWindow)
    myViewer.setSceneGraph(root)
    myViewer.setTitle("Texture Coordinates")

    # In Inventor 2.1, if the machine does not have hardware texture
    # mapping, we must override the default drawStyle to display textures.
    myViewer.setDrawStyle(SoGuiViewer.STILL, SoGuiViewer.VIEW_AS_IS)

    myViewer.show()

    SoGui.show(myWindow)
    SoGui.mainLoop()

if __name__ == "__main__":
    main()

