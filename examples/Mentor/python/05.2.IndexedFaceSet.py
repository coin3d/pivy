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
# chapter 5, example 2.
#
# This example creates an IndexedFaceSet. It creates 
# the first stellation of the dodecahedron.
#

from pivy import *
import sys

##############################################################
## CODE FOR The Inventor Mentor STARTS HERE

#
# Positions of all of the vertices:
#
vertexPositions = (
   ( 0.0000,  1.2142,  0.7453),  # top

   ( 0.0000,  1.2142, -0.7453),  # points surrounding top
   (-1.2142,  0.7453,  0.0000),
   (-0.7453,  0.0000,  1.2142), 
   ( 0.7453,  0.0000,  1.2142), 
   ( 1.2142,  0.7453,  0.0000),

   ( 0.0000, -1.2142,  0.7453),  # points surrounding bottom
   (-1.2142, -0.7453,  0.0000), 
   (-0.7453,  0.0000, -1.2142),
   ( 0.7453,  0.0000, -1.2142), 
   ( 1.2142, -0.7453,  0.0000), 

   ( 0.0000, -1.2142, -0.7453), # bottom
)

#
# Connectivity, information 12 faces with 5 vertices each ),
# (plus the end-of-face indicator for each face):
#

indices = (
   1,  2,  3,  4, 5, SO_END_FACE_INDEX, # top face

   0,  1,  8,  7, 3, SO_END_FACE_INDEX, # 5 faces about top
   0,  2,  7,  6, 4, SO_END_FACE_INDEX,
   0,  3,  6, 10, 5, SO_END_FACE_INDEX,
   0,  4, 10,  9, 1, SO_END_FACE_INDEX,
   0,  5,  9,  8, 2, SO_END_FACE_INDEX, 

    9,  5, 4, 6, 11, SO_END_FACE_INDEX, # 5 faces about bottom
   10,  4, 3, 7, 11, SO_END_FACE_INDEX,
    6,  3, 2, 8, 11, SO_END_FACE_INDEX,
    7,  2, 1, 9, 11, SO_END_FACE_INDEX,
    8,  1, 5,10, 11, SO_END_FACE_INDEX,

    6,  7, 8, 9, 10, SO_END_FACE_INDEX, # bottom face
)
 
# Colors for the 12 faces
colors = (
   (1.0, .0, 0), ( .0,  .0, 1.0), (0, .7,  .7), ( .0, 1.0,  0),
   ( .7, .7, 0), ( .7,  .0,  .7), (0, .0, 1.0), ( .7,  .0, .7),
   ( .7, .7, 0), ( .0, 1.0,  .0), (0, .7,  .7), (1.0,  .0,  0)
)

# set this variable to 0 if you want to use the other method
IV_STRICT = 1

# Routine to create a scene graph representing a dodecahedron
def makeStellatedDodecahedron():
	result = SoSeparator()
	result.ref()

	if IV_STRICT:
		# This is the preferred code for Inventor 2.1

		# Using the new SoVertexProperty node is more efficient
		myVertexProperty = SoVertexProperty()

		# Define colors for the faces
		for i in range(12):
			myVertexProperty.orderedRGBA.set1Value(i, SbColor(colors[i]).getPackedValue())
			myVertexProperty.materialBinding(SoMaterialBinding.PER_FACE)

		# Define coordinates for vertices
		myVertexProperty.vertex.setValues(0, 12, vertexPositions)

		# Define the IndexedFaceSet, with indices into
		# the vertices:
		myFaceSet = SoIndexedFaceSet()
		myFaceSet.coordIndex.setValues(0, 72, indices)

		myFaceSet.vertexProperty.setValue(myVertexProperty)
		result.addChild(myFaceSet)

	else:
		# Define colors for the faces
		myMaterials = SoMaterial()
		myMaterials.diffuseColor.setValues(0, 12, colors)
		result.addChild(myMaterials)
		myMaterialBinding = SoMaterialBinding()
		myMaterialBinding.value(SoMaterialBinding.PER_FACE)
		result.addChild(myMaterialBinding)

		# Define coordinates for vertices
		myCoords = SoCoordinate3()
		myCoords.point.setValues(0, 12, vertexPositions)
		result.addChild(myCoords)

		# Define the IndexedFaceSet, with indices into
		# the vertices:
		myFaceSet = SoIndexedFaceSet()
		myFaceSet.coordIndex.setValues(0, 72, indices)
		result.addChild(myFaceSet)

	result.unrefNoDelete()
	return result

## CODE FOR The Inventor Mentor ENDS HERE
##############################################################

def main():
	# Initialize Inventor and Qt
	myWindow = SoQt_init(sys.argv[0])
	if myWindow == None: sys.exit(1)

	root = makeStellatedDodecahedron()
	root.ref()

	myViewer = SoQtExaminerViewer(myWindow)
	myViewer.setSceneGraph(root)
	myViewer.setTitle("Indexed Face Set: Stellated Dodecahedron")
	myViewer.show()
	myViewer.viewAll()

	SoQt_show(myWindow)
	SoQt_mainLoop()

if __name__ == "__main__":
	main()
