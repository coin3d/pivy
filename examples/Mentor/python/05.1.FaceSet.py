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
# chapter 5, example 1.
#
# This example builds an obelisk using the Face Set node.
#

from pivy import *
import sys

##############################################################
## CODE FOR The Inventor Mentor STARTS HERE

##  Eight polygons. The first four are triangles 
##  The second four are quadrilaterals for the sides.
vertices = (
   ( 0, 30, 0), (-2,27, 2), ( 2,27, 2),            #front tri
   ( 0, 30, 0), (-2,27,-2), (-2,27, 2),            #left  tri
   ( 0, 30, 0), ( 2,27,-2), (-2,27,-2),            #rear  tri
   ( 0, 30, 0), ( 2,27, 2), ( 2,27,-2),            #right tri
   (-2, 27, 2), (-4,0, 4), ( 4,0, 4), ( 2,27, 2),  #front quad
   (-2, 27,-2), (-4,0,-4), (-4,0, 4), (-2,27, 2),  #left  quad
   ( 2, 27,-2), ( 4,0,-4), (-4,0,-4), (-2,27,-2),  #rear  quad
   ( 2, 27, 2), ( 4,0, 4), ( 4,0,-4), ( 2,27,-2)   #right quad
)

# Number of vertices in each polygon:
numvertices = (3, 3, 3, 3, 4, 4, 4, 4)

# Normals for each polygon:
norms = ( 
   (0, .555,  .832), (-.832, .555, 0), #front, left tris
   (0, .555, -.832), ( .832, .555, 0), #rear, right tris
   
   (0, .0739,  .9973), (-.9972, .0739, 0),#front, left quads
   (0, .0739, -.9973), ( .9972, .0739, 0),#rear, right quads
)

# set this variable to 0 if you want to use the other method
IV_STRICT = 1

def makeObeliskFaceSet():
   obelisk = SoSeparator()
   obelisk.ref()

   if IV_STRICT:
	   # This is the preferred code for Inventor 2.1
 
	   # Using the new SoVertexProperty node is more efficient
	   myVertexProperty = SoVertexProperty()

	   # Define the normals used:
	   myVertexProperty.normal.setValues(0, 8, norms)
	   myVertexProperty.normalBinding(SoNormalBinding.PER_FACE)

	   # Define material for obelisk
	   myVertexProperty.orderedRGBA.setValue(SbColor(.4,.4,.4).getPackedValue())

	   # Define coordinates for vertices
	   myVertexProperty.vertex.setValues(0, 28, vertices)

	   # Define the FaceSet
	   myFaceSet = SoFaceSet()
	   myFaceSet.numVertices.setValues(0, 8, numvertices)
 
	   myFaceSet.vertexProperty.setValue(myVertexProperty)
	   obelisk.addChild(myFaceSet)

   else:
	   # Define the normals used:
	   myNormals = SoNormal()
	   myNormals.vector.setValues(0, 8, norms)
	   obelisk.addChild(myNormals)
	   myNormalBinding = SoNormalBinding()
	   myNormalBinding.value(SoNormalBinding.PER_FACE)
	   obelisk.addChild(myNormalBinding)

	   # Define material for obelisk
	   myMaterial = SoMaterial()
	   myMaterial.diffuseColor.setValue(.4, .4, .4)
	   obelisk.addChild(myMaterial)

	   # Define coordinates for vertices
	   myCoords = SoCoordinate3()
	   myCoords.point.setValues(0, 28, vertices)
	   obelisk.addChild(myCoords)

	   # Define the FaceSet
	   myFaceSet = SoFaceSet()
	   myFaceSet.numVertices.setValues(0, 8, numvertices)
	   obelisk.addChild(myFaceSet)

   obelisk.unrefNoDelete()
   return obelisk

## CODE FOR The Inventor Mentor ENDS HERE
##############################################################

def main():
	# Initialize Inventor and Gtk
	myWindow = SoGtk_init(sys.argv[0])
	if myWindow == None: sys.exit(1)

	root = SoSeparator()
	root.ref()

	root.addChild(makeObeliskFaceSet())

	myViewer = SoGtkExaminerViewer(myWindow)
	myViewer.setSceneGraph(root)
	myViewer.setTitle("Face Set: Obelisk")
	myViewer.show()
	myViewer.viewAll()

	SoGtk_show(myWindow)
	SoGtk_mainLoop()

if __name__ == "__main__":
	main()
