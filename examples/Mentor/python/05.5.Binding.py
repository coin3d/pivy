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
# chapter 5, example 5.
#
# This example illustrates a variety of ways to bind 
# materials to a polygon object.
# Three cases of a switch statement show various ways of 
# binding materials to objects.  
# The object used for all three examples is the stellated 
# dodecahedron from an earlier example in this chapter.  
#

from pivy import *
import sys

# Positions of all of the vertices:
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

# Connectivity, information 12 faces with 5 vertices each ),
# (plus the end-of-face indicator for each face):

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
   (1.0, .0, 0), (.0,  .0, 1.0), (0, .7,  .7), ( .0, 1.0,  0),
   ( .7, .7, 0), (.7,  .0,  .7), (0, .0, 1.0), ( .7,  .0, .7),
   ( .7, .7, 0), (.0, 1.0,  .0), (0, .7,  .7), (1.0,  .0,  0)
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

		# The material binding.
		myVertexProperty.materialBinding(SoMaterialBinding.PER_FACE)

		# Define colors for the faces
		for i in range(12):
			myVertexProperty.orderedRGBA.set1Value(i, SbColor(colors[i]).getPackedValue())

		# Define coordinates for vertices
		myVertexProperty.vertex.setValues(0, 12, vertexPositions)

		# Define the IndexedFaceSet, with indices into
		# the vertices:
		myFaceSet = SoIndexedFaceSet()
		myFaceSet.coordIndex.setValues(0, 72, indices)

		myFaceSet.vertexProperty.setValue(myVertexProperty)
		result.addChild(myFaceSet)

	else:
		# The material binding node.
		myBinding = SoMaterialBinding()
		myBinding.value(SoMaterialBinding.PER_FACE)
		result.addChild(myBinding)

		# Define colors for the faces
		myMaterials = SoMaterial()
		myMaterials.diffuseColor.setValues(0, 12, colors)
		result.addChild(myMaterials)

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


def main():
	whichBinding = 0

	if len(sys.argv) > 1: whichBinding = int(sys.argv[1])

	if whichBinding > 2 or whichBinding < 0 or len(sys.argv) == 1:
		sys.stderr.write("Argument must be 0, 1, or 2\n")
		sys.stderr.write("\t0 = PER_FACE\n")
		sys.stderr.write("\t1 = PER_VERTEX_INDEXED\n")
		sys.stderr.write("\t2 = PER_FACE_INDEXED\n")
		sys.exit(1)

	# Initialize Inventor and Gtk
	myWindow = SoGtk_init(sys.argv[0])
	if myWindow == None: sys.exit(1)

	root = makeStellatedDodecahedron()
	root.ref()

	if IV_STRICT:
		# Get the indexed face set for editing
		myIndexedFaceSet = root.getChild(0) # (SoIndexedFaceSet *) root.getChild(0)

		# Get the SoVertexProperty node for editing the material binding
		myVertexProperty = myIndexedFaceSet.vertexProperty.getValue() # (SoVertexProperty *) myIndexedFaceSet.vertexProperty.getValue()

##############################################################
## CODE FOR The Inventor Mentor STARTS HERE (Inventor 2.1)

		# Which material to use to color the faces 
		# half red & half blue
		materialIndices = (
			0, 0, 0, 0, 0, 0,
			1, 1, 1, 1, 1, 1
			)

		if whichBinding == 0:
			# Set up binding to use a different color for each face 
			myVertexProperty.materialBinding(SoMaterialBinding.PER_FACE)
		elif whichBinding == 1:
			# Set up binding to use a different color at each 
			# vertex, BUT, vertices shared between faces will 
			# have the same color.
			myVertexProperty.materialBinding(SoMaterialBinding.PER_VERTEX_INDEXED)
		elif whichBinding == 2:
			myVertexProperty.materialBinding(SoMaterialBinding.PER_FACE_INDEXED)
			myIndexedFaceSet.materialIndex.setValues(0, 12, materialIndices)

## CODE FOR The Inventor Mentor ENDS HERE
##############################################################

	else:   # old style
		# Get the material binding node for editing
		myBinding = root.getChild(0) # (SoMaterialBinding *) root.getChild(0)

		# Get the indexed face set for editing
		myIndexedFaceSet = root.getChild(3) # (SoIndexedFaceSet *) root.getChild(3)

##############################################################
## CODE FOR The Inventor Mentor STARTS HERE

		# Which material to use to color the faces 
		# half red & half blue
		materialIndices = (
			0, 0, 0, 0, 0, 0,
			1, 1, 1, 1, 1, 1,
			)

		if whichBinding == 0:
			# Set up binding to use a different color for each face 
			myBinding.value(SoMaterialBinding.PER_FACE)
		elif whichBinding == 1:
			# Set up binding to use a different color at each 
			# vertex, BUT, vertices shared between faces will 
			# have the same color.
			myBinding.value(SoMaterialBinding.PER_VERTEX_INDEXED)
		elif whichBinding == 2:
			myBinding.value(SoMaterialBinding.PER_FACE_INDEXED)
			myIndexedFaceSet.materialIndex.setValues(0, 12, materialIndices)

## CODE FOR The Inventor Mentor ENDS HERE
##############################################################

	myViewer = SoGtkExaminerViewer(myWindow)
	myViewer.setSceneGraph(root)
	myViewer.setTitle("Material Bindings")
	myViewer.show()
	myViewer.viewAll()

	SoGtk_show(myWindow)
	SoGtk_mainLoop()

if __name__ == "__main__":
	main()
