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
# chapter 5, example 4.
#
# This example creates the St. Louis Arch using a QuadMesh.
#

from pivy import *
import sys

##############################################################
## CODE FOR The Inventor Mentor STARTS HERE

# Positions of all of the vertices:
vertexPositions = (
   # 1st row
   (-13.0,  0.0, 1.5), (-10.3, 13.7, 1.2), ( -7.6, 21.7, 1.0), 
   ( -5.0, 26.1, 0.8), ( -2.3, 28.2, 0.6), ( -0.3, 28.8, 0.5),
   (  0.3, 28.8, 0.5), (  2.3, 28.2, 0.6), (  5.0, 26.1, 0.8), 
   (  7.6, 21.7, 1.0), ( 10.3, 13.7, 1.2), ( 13.0,  0.0, 1.5),
   # 2nd row
   (-10.0,  0.0, 1.5), ( -7.9, 13.2, 1.2), ( -5.8, 20.8, 1.0), 
   ( -3.8, 25.0, 0.8), ( -1.7, 27.1, 0.6), ( -0.2, 27.6, 0.5),
   (  0.2, 27.6, 0.5), (  1.7, 27.1, 0.6), (  3.8, 25.0, 0.8), 
   (  5.8, 20.8, 1.0), (  7.9, 13.2, 1.2), ( 10.0,  0.0, 1.5),
   # 3rd row
   (-10.0,  0.0,-1.5), ( -7.9, 13.2,-1.2), ( -5.8, 20.8,-1.0), 
   ( -3.8, 25.0,-0.8), ( -1.7, 27.1,-0.6), ( -0.2, 27.6,-0.5),
   (  0.2, 27.6,-0.5), (  1.7, 27.1,-0.6), (  3.8, 25.0,-0.8), 
   (  5.8, 20.8,-1.0), (  7.9, 13.2,-1.2), ( 10.0,  0.0,-1.5),
   # 4th row 
   (-13.0,  0.0,-1.5), (-10.3, 13.7,-1.2), ( -7.6, 21.7,-1.0), 
   ( -5.0, 26.1,-0.8), ( -2.3, 28.2,-0.6), ( -0.3, 28.8,-0.5),
   (  0.3, 28.8,-0.5), (  2.3, 28.2,-0.6), (  5.0, 26.1,-0.8), 
   (  7.6, 21.7,-1.0), ( 10.3, 13.7,-1.2), ( 13.0,  0.0,-1.5),
   # 5th row
   (-13.0,  0.0, 1.5), (-10.3, 13.7, 1.2), ( -7.6, 21.7, 1.0), 
   ( -5.0, 26.1, 0.8), ( -2.3, 28.2, 0.6), ( -0.3, 28.8, 0.5),
   (  0.3, 28.8, 0.5), (  2.3, 28.2, 0.6), (  5.0, 26.1, 0.8), 
   (  7.6, 21.7, 1.0), ( 10.3, 13.7, 1.2), ( 13.0,  0.0, 1.5)
)

# set this variable to 0 if you want to use the other method
IV_STRICT = 0

# Routine to create a scene graph representing an arch.
def makeArch():
   result = SoSeparator()
   result.ref()

   if IV_STRICT:
       # This is the preferred code for Inventor 2.1 

       # Using the new SoVertexProperty node is more efficient
       myVertexProperty = SoVertexProperty()

       # Define the material
       myVertexProperty.orderedRGBA.setValue(SbColor(.78, .57, .11).getPackedValue())

       # Define coordinates for vertices
       myVertexProperty.vertex.setValues(0, 60, vertexPositions)

       # Define the QuadMesh.
       myQuadMesh = SoQuadMesh()
       myQuadMesh.verticesPerRow(12)

       myQuadMesh.verticesPerColumn(5)

       myQuadMesh.vertexProperty.setValue(myVertexProperty)
       result.addChild(myQuadMesh)

   else:
       # Define the material
       myMaterial = SoMaterial()
       myMaterial.diffuseColor.setValue(.78, .57, .11)
       result.addChild(myMaterial)

       # Define coordinates for vertices
       myCoords = SoCoordinate3()
       myCoords.point.setValues(0, 60, vertexPositions)
       result.addChild(myCoords)

       # Define the QuadMesh.
       myQuadMesh = SoQuadMesh()
       myQuadMesh.verticesPerRow(12)

       myQuadMesh.verticesPerColumn(5)
       result.addChild(myQuadMesh)

   result.unrefNoDelete()
   return result

## CODE FOR The Inventor Mentor ENDS HERE
##############################################################

def main():
    # Initialize Inventor and Qt
    myWindow = SoQt_init(sys.argv[0])
    if myWindow == None: sys.exit(1)

    root = makeArch()
    root.ref()

    myViewer = SoQtExaminerViewer(myWindow)
    myViewer.setSceneGraph(root)
    myViewer.setTitle("Quad Mesh: Arch")
    myViewer.show()
    myViewer.viewAll()

    SoQt_show(myWindow)
    SoQt_mainLoop()

if __name__ == "__main__":
    main()
