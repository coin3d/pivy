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
# chapter 5, example 3.
#
# This example creates a TriangleStripSet. It creates
# a pennant-shaped flag.
#

from pivy import *
import sys

##############################################################
## CODE FOR The Inventor Mentor STARTS HERE

#
# Positions of all of the vertices:
#
vertexPositions = (
   (  0,   12,    0 ), (   0,   15,    0),
   (2.1, 12.1,  -.2 ), ( 2.1, 14.6,  -.2),
   (  4, 12.5,  -.7 ), (   4, 14.5,  -.7),
   (4.5, 12.6,  -.8 ), ( 4.5, 14.4,  -.8),
   (  5, 12.7,   -1 ), (   5, 14.4,   -1),
   (4.5, 12.8, -1.4 ), ( 4.5, 14.6, -1.4),
   (  4, 12.9, -1.6 ), (   4, 14.8, -1.6),
   (3.3, 12.9, -1.8 ), ( 3.3, 14.9, -1.8),
   (  3,   13, -2.0 ), (   3, 14.9, -2.0), 
   (3.3, 13.1, -2.2 ), ( 3.3, 15.0, -2.2),
   (  4, 13.2, -2.5 ), (   4, 15.0, -2.5),
   (  6, 13.5, -2.2 ), (   6, 14.8, -2.2),
   (  8, 13.4,   -2 ), (   8, 14.6,   -2),
   ( 10, 13.7, -1.8 ), (  10, 14.4, -1.8),
   ( 12,   14, -1.3 ), (  12, 14.5, -1.3),
   ( 15, 14.9, -1.2 ), (  15,   15, -1.2),

   (-.5, 15,   0 ), ( -.5, 0,   0),   # the flagpole
   (  0, 15,  .5 ), (   0, 0,  .5),
   (  0, 15, -.5 ), (   0, 0, -.5),
   (-.5, 15,   0 ), ( -.5, 0,   0)
)


# Number of vertices in each strip.
numVertices = (
   32, # flag
   8   # pole
)
 
# Colors for the 12 faces
colors = (
   ( .5, .5,  1 ), # purple flag
   ( .4, .4, .4 ), # grey flagpole
)

# set this variable to 0 if you want to use the other method
IV_STRICT = 1

# Routine to create a scene graph representing a pennant.
def makePennant():
	result = SoSeparator()
	result.ref()

	# A shape hints tells the ordering of polygons. 
	# This insures double sided lighting.
	myHints = SoShapeHints()
	myHints.vertexOrdering(SoShapeHints.COUNTERCLOCKWISE)
	result.addChild(myHints)

	if IV_STRICT:
		# This is the preferred code for Inventor 2.1 

		# Using the new SoVertexProperty node is more efficient
		myVertexProperty = SoVertexProperty()

		# Define colors for the strips
		for i in range(2):
			myVertexProperty.orderedRGBA.set1Value(i, SbColor(colors[i]).getPackedValue())
			myVertexProperty.materialBinding(SoMaterialBinding.PER_PART)

		# Define coordinates for vertices
		myVertexProperty.vertex.setValues(0, 40, vertexPositions)

		# Define the TriangleStripSet, made of two strips.
		myStrips = SoTriangleStripSet()
		myStrips.numVertices.setValues(0, 2, numVertices)
 
		myStrips.vertexProperty.setValue(myVertexProperty)
		result.addChild(myStrips)

	else:
		# Define colors for the strips
		myMaterials = SoMaterial()
		myMaterials.diffuseColor.setValues(0, 2, colors)
		result.addChild(myMaterials)
		myMaterialBinding = SoMaterialBinding()
		myMaterialBinding.value(SoMaterialBinding.PER_PART)
		result.addChild(myMaterialBinding)

		# Define coordinates for vertices
		myCoords = SoCoordinate3()
		myCoords.point.setValues(0, 40, vertexPositions)
		result.addChild(myCoords)

		# Define the TriangleStripSet, made of two strips.
		myStrips = SoTriangleStripSet()
		myStrips.numVertices.setValues(0, 2, numVertices)
		result.addChild(myStrips)

	result.unrefNoDelete()
	return result

## CODE FOR The Inventor Mentor ENDS HERE
##############################################################

def main():
	# Initialize Inventor and Gtk
	myWindow = SoGtk_init(sys.argv[0])
	if myWindow == None: sys.exit(1)

	root = makePennant()
	root.ref()

	myViewer = SoGtkExaminerViewer(myWindow)
	myViewer.setSceneGraph(root)
	myViewer.setTitle("Triangle Strip Set: Pennant")
	myViewer.show()
	myViewer.viewAll()

	SoGtk_show(myWindow)
	SoGtk_mainLoop()

if __name__ == "__main__":
	main()
