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
# This is an example from The Inventor Mentor,
# chapter 10, example 5.
#
# The scene graph has a sphere and a text 3D object. 
# A selection node is placed at the top of the scene graph. 
# When an object is selected, a selection callback is called
# to change the material color of that object.
#

from pivy import *
import sys

# global data
textMaterial, sphereMaterial = [None]*2
reddish = (1.0, 0.2, 0.2)  # Color when selected
white   = (0.8, 0.8, 0.8)  # Color when not selected

# This routine is called when an object gets selected. 
# We determine which object was selected, and change 
# that objects material color.
def mySelectionCB(void, selectionPath):
	if selectionPath.getTail().isOfType(SoText3_getClassTypeId()):
		textMaterial.diffuseColor.setValue(reddish)
	elif selectionPath.getTail().isOfType(SoSphere_getClassTypeId()):
		sphereMaterial.diffuseColor.setValue(reddish)

# This routine is called whenever an object gets deselected. 
# We determine which object was deselected, and reset 
# that objects material color.
def myDeselectionCB(void, deselectionPath):
	if deselectionPath.getTail().isOfType(SoText3_getClassTypeId()):
		textMaterial.diffuseColor.setValue(white)
	elif deselectionPath.getTail().isOfType(SoSphere_getClassTypeId()):
		sphereMaterial.diffuseColor.setValue(white)

def main():
	global textMaterial, sphereMaterial
	
	# Initialize Inventor and Qt
	myWindow = SoQt_init(sys.argv[0])
	if myWindow == None: sys.exit(1)

	# Create and set up the selection node
	selectionRoot = SoSelection()
	selectionRoot.ref()
	selectionRoot.policy(SoSelection.SINGLE)
	selectionRoot.addPythonSelectionCallback(mySelectionCB)
	selectionRoot.addPythonDeselectionCallback(myDeselectionCB)

	# Create the scene graph
	root = SoSeparator()
	selectionRoot.addChild(root)

	myCamera = SoPerspectiveCamera()
	root.addChild(myCamera)
	root.addChild(SoDirectionalLight())

	# Add a sphere node
	sphereRoot = SoSeparator()
	sphereTransform = SoTransform()
	sphereTransform.translation.setValue(17., 17., 0.)
	sphereTransform.scaleFactor.setValue(8., 8., 8.)
	sphereRoot.addChild(sphereTransform)

	sphereMaterial = SoMaterial()
	sphereMaterial.diffuseColor.setValue(.8, .8, .8)
	sphereRoot.addChild(sphereMaterial)
	sphereRoot.addChild(SoSphere())
	root.addChild(sphereRoot)

	# Add a text node
	textRoot = SoSeparator()
	textTransform = SoTransform()
	textTransform.translation.setValue(0., -1., 0.)
	textRoot.addChild(textTransform)

	textMaterial = SoMaterial()
	textMaterial.diffuseColor.setValue(.8, .8, .8)
	textRoot.addChild(textMaterial)
	textPickStyle = SoPickStyle()
	textPickStyle.style.setValue(SoPickStyle.BOUNDING_BOX)
	textRoot.addChild(textPickStyle)
	myText = SoText3()
	myText.string("rhubarb")
	textRoot.addChild(myText)
	root.addChild(textRoot)

	myRenderArea = SoQtRenderArea(myWindow)
	myRenderArea.setSceneGraph(selectionRoot)
	myRenderArea.setTitle("My Selection Callback")
	myRenderArea.show()

	# Make the camera see the whole scene
	myViewport = myRenderArea.getViewportRegion()
	myCamera.viewAll(root, myViewport, 2.0)

	SoQt_show(myWindow)
	SoQt_mainLoop()

if __name__ == "__main__":
    main()
