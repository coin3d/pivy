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
# This is an example from The Inventor Mentor
# chapter 10, example 1.
#
# The scene graph has 4 objects which may be
# selected by picking with the left mouse button
# (use shift key to extend the selection to more
# than one object).
# 
# Hitting the up arrow key will increase the size of
# each selected object; hitting down arrow will decrease
# the size of each selected object.
#

from pivy import *
import sys

# Global data
cubeTransform, sphereTransform, coneTransform, cylTransform = [None] * 4

# Scale each object in the selection list
def myScaleSelection(selection, sf):
	global cubeTransform, sphereTransform, coneTransform, cylTransform

	# Scale each object in the selection list
	for i in range(selection.getNumSelected()):
		selectedPath = selection.getPath(i)
		xform = None

		# Look for the shape node, starting from the tail of the
		# path.  Once we know the type of shape, we know which
		# transform to modify
		for j in range(selectedPath.getLength()):
			if xform != None: break
			n = cast(selectedPath.getNodeFromTail(j), "SoNode")

			if n.isOfType(SoCube_getClassTypeId()):
				xform = cubeTransform
			elif n.isOfType(SoCone_getClassTypeId()):
				xform = coneTransform
			elif n.isOfType(SoSphere_getClassTypeId()):
				xform = sphereTransform
			elif n.isOfType(SoCylinder_getClassTypeId()):
				xform = cylTransform

		# Apply the scale
		scaleFactor = xform.scaleFactor.getValue()
		scaleFactor *= sf
		xform.scaleFactor.setValue(scaleFactor)

###############################################################
# CODE FOR The Inventor Mentor STARTS HERE  (part 2)

# If the event is down arrow, then scale down every object 
# in the selection list if the event is up arrow, scale up.
# The userData is the selectionRoot from main().
def myKeyPressCB(userData, eventCB):
	selection = cast(userData, "SoSelection")
	event = eventCB.getEvent()

	# check for the Up and Down arrow keys being pressed
	if SoKeyboardEvent_isKeyPressEvent(event, SoKeyboardEvent.UP_ARROW):
		myScaleSelection(selection, 1.1)
		eventCB.setHandled()
	elif SoKeyboardEvent_isKeyPressEvent(event, SoKeyboardEvent.DOWN_ARROW):
		myScaleSelection(selection, 1.0/1.1)
		eventCB.setHandled()

# CODE FOR The Inventor Mentor ENDS HERE
###############################################################

def main():
	global cubeTransform, sphereTransform, coneTransform, cylTransform
	# Print out usage message
	print "Left mouse button        - selects object"
	print "<shift>Left mouse button - selects multiple objects"
	print "Up and Down arrows       - scale selected objects"

	# Initialize Inventor and Gtk
	myWindow = SoGtk_init(sys.argv[0])
	if myWindow == None:
		sys.exit(1)

	# Create and set up the selection node
	selectionRoot = SoSelection()
	selectionRoot.ref()
	selectionRoot.policy(SoSelection.SHIFT)
   
	# Add a camera and some light
	myCamera = SoPerspectiveCamera()
	selectionRoot.addChild(myCamera)
	selectionRoot.addChild(SoDirectionalLight())

###############################################################
# CODE FOR The Inventor Mentor STARTS HERE  (part 1)

	# An event callback node so we can receive key press events
	myEventCB = SoEventCallback()
	myEventCB.addPythonEventCallback(SoKeyboardEvent_getClassTypeId(), 
									 myKeyPressCB, selectionRoot)
	selectionRoot.addChild(myEventCB)

# CODE FOR The Inventor Mentor ENDS HERE
###############################################################

	# Add some geometry to the scene

	# a red cube
	cubeRoot = SoSeparator()
	cubeMaterial = SoMaterial()
	cubeTransform = SoTransform()
	cubeRoot.addChild(cubeTransform)
	cubeRoot.addChild(cubeMaterial)
	cubeRoot.addChild(SoCube())
	cubeTransform.translation.setValue(-2, 2, 0)
	cubeMaterial.diffuseColor.setValue(.8, 0, 0)
	selectionRoot.addChild(cubeRoot)

	# a blue sphere
	sphereRoot = SoSeparator()
	sphereMaterial = SoMaterial()
	sphereTransform = SoTransform()
	sphereRoot.addChild(sphereTransform)
	sphereRoot.addChild(sphereMaterial)
	sphereRoot.addChild(SoSphere())
	sphereTransform.translation.setValue(2, 2, 0)
	sphereMaterial.diffuseColor.setValue(0, 0, .8)
	selectionRoot.addChild(sphereRoot)

	# a green cone
	coneRoot = SoSeparator()
	coneMaterial = SoMaterial()
	coneTransform = SoTransform()
	coneRoot.addChild(coneTransform)
	coneRoot.addChild(coneMaterial)
	coneRoot.addChild(SoCone())
	coneTransform.translation.setValue(2, -2, 0)
	coneMaterial.diffuseColor.setValue(0, .8, 0)
	selectionRoot.addChild(coneRoot)

	# a magenta cylinder
	cylRoot = SoSeparator()
	cylMaterial = SoMaterial()
	cylTransform = SoTransform()
	cylRoot.addChild(cylTransform)
	cylRoot.addChild(cylMaterial)
	cylRoot.addChild(SoCylinder())
	cylTransform.translation.setValue(-2, -2, 0)
	cylMaterial.diffuseColor.setValue(.8, 0, .8)
	selectionRoot.addChild(cylRoot)

	# Create a render area for viewing the scene
	myRenderArea = SoGtkRenderArea(myWindow)
	myRenderArea.setSceneGraph(selectionRoot)
	
	# need to make a reference like this otherwise SoBoxHighlightRenderAction() gets
	# dereferenced after the myRenderArea.setGLRenderAction() call, resulting in its
	# destructor to be called.
	# i.e.: myRenderArea.setGLRenderAction(SoBoxHighlightRenderAction()) would result
	# in a segfault!
	# in my opinion this should _not_ happen, but it does! :(
	#
	# FIXME: investigate why this is so...
	# myRenderArea.setGLRenderAction(SoBoxHighlightRenderAction())
	boxhra = SoBoxHighlightRenderAction()
	myRenderArea.setGLRenderAction(boxhra)
	
	myRenderArea.redrawOnSelectionChange(selectionRoot)
	myRenderArea.setTitle("Adding Event Callbacks")

	# Make the camera see the whole scene
	viewportRegion = myRenderArea.getViewportRegion()
	myCamera.viewAll(selectionRoot, viewportRegion, 2.0)

	# Show our application window, and loop forever...
	myRenderArea.show()
	SoGtk_show(myWindow)
	SoGtk_mainLoop()

if __name__ == "__main__":
    main()
