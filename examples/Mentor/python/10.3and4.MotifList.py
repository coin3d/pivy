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
# chapter 10, example 3.
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
# This also demonstrates selecting objects from a Motif
# list, and calling select/deselect functions on the
# SoSelection node to change the selection. Use the Shift
# key to extend the selection (i.e. pick more than one
# item in the motif list.)
#

from pivy import *
import sys

# Function prototypes
void mySelectionCB(void *, SoPath *)
void myKeyPressCB(void *, SoEventCallback *)
void myScaleSelection(SoSelection *, float)
Widget createList(Display *, SoSelection *)
void myListPickCB(Widget, char *, XmListCallbackStruct *)

# Global data
SbViewportRegion viewportRegion
Widget motifList
SoTransform *cubeTransform, *sphereTransform,
            *coneTransform, *cylTransform

###############################################################
# CODE FOR The Inventor Mentor STARTS HERE  

CUBE, SPHERE, CONE,	CYL, NUM_OBJECTS = 0, 1, 2, 3, 4

objectNames= (
	"Cube",
	"Sphere",
	"Cone",
	"Cylinder"
	)

# CODE FOR The Inventor Mentor ENDS HERE
###############################################################



# Create the object list widget
Widget
createList(Display *display, SoSelection *selection)
{
   Widget shell
   Arg    args[4]
   int    i, n

   # Create a new shell window for the list
   n = 0
   XtSetArg(args[n], XmNtitle, "Selection")
   n++
   shell = XtAppCreateShell("example", "Inventor",
      topLevelShellWidgetClass, display, args, n)

###############################################################
# CODE FOR The Inventor Mentor STARTS HERE  (part 3)

   # Create a table of object names
   XmString *table = new XmString[NUM_OBJECTS]
   for (i=0 i<NUM_OBJECTS i++) {
       table[i] = XmStringCreate(objectNames[i], 
				 XmSTRING_DEFAULT_CHARSET)
   }

   # Create the list widget
   n = 0
   XtSetArg(args[n], XmNitems, table)
   n++
   XtSetArg(args[n], XmNitemCount, NUM_OBJECTS)
   n++
   XtSetArg(args[n], XmNselectionPolicy, XmEXTENDED_SELECT)
   n++

   motifList = XmCreateScrolledList(shell, "funcList", args, n)
   XtAddCallback(motifList, XmNextendedSelectionCallback,
      (XtCallbackProc) myListPickCB, (XtPointer) selection)

# CODE FOR The Inventor Mentor ENDS HERE
###############################################################

   # Free the name table
   for (i = 0 i < NUM_OBJECTS i++)
      XmStringFree(table[i])
   free(table)

   # Manage the list and return the shell
   XtManageChild(motifList)

   return shell
}

# This callback is invoked every time the user picks
# an item in the Motif list.
void
myListPickCB(Widget, char *userData,
            XmListCallbackStruct *listData)
{
   SoSelection *selection = (SoSelection *) userData
   SoSearchAction mySearchAction

   # Remove the selection callbacks so that we don't get
   # called back while we are updating the selection list
   selection.removeSelectionCallback(
            mySelectionCB, (void *) TRUE)
   selection.removeDeselectionCallback(
            mySelectionCB, (void *) FALSE)

###############################################################
# CODE FOR The Inventor Mentor STARTS HERE  (part 4)

   # Clear the selection node, then loop through the list
   # and reselect
   selection.deselectAll()

   # Update the SoSelection based on what is selected in
   # the motif list.  We do this by extracting the string
   # from the selected XmString, and searching for the 
   # object of that name.
   for (int i = 0 i < listData.selected_item_count i++) {
      mySearchAction.setName(
            SoXt::decodeString(listData.selected_items[i]))
      mySearchAction.apply(selection)
      selection.select(mySearchAction.getPath())
   }

# CODE FOR The Inventor Mentor ENDS HERE
###############################################################

   # Add the selection callbacks again
   selection.addSelectionCallback(
            mySelectionCB, (void *) TRUE)
   selection.addDeselectionCallback(
            mySelectionCB, (void *) FALSE)
}


# This is called whenever an object is selected or deselected.
# if userData is TRUE, then it's a selection else deselection.
# (we set this convention up when we registered this callback).
# The function updates the Motif list to reflect the current
# selection.
void
mySelectionCB(void *userData, SoPath *selectionPath)
{
   Arg args[1]
   SbBool isSelection = (SbBool) userData

   # We have to temporarily change the selection policy to
   # MULTIPLE so that we can select and deselect single items.
   XtSetArg(args[0], XmNselectionPolicy, XmMULTIPLE_SELECT)
   XtSetValues(motifList, args, 1)

   SoNode *node = selectionPath.getTail()

   for (int i = 0 i < NUM_OBJECTS i++) {
      if (node.getName() == objectNames[i]) {
         if (isSelection) {
             XmListSelectPos(motifList, i+1, False)
         } else XmListDeselectPos(motifList, i+1)
         XmUpdateDisplay(motifList)
         break
      }
   }

   # Restore the selection policy to extended.
   XtSetArg(args[0], XmNselectionPolicy, XmEXTENDED_SELECT)
   XtSetValues(motifList, args, 1)
}

###############################################################
# CODE FOR The Inventor Mentor STARTS HERE  (Example 10-4)

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
	# Print out usage message
	print "Left mouse button        - selects object"
	print "<shift>Left mouse button - selects multiple objects"
	print "Up and Down arrows       - scale selected objects"
	
	# Initialize Inventor and Qt
	myWindow = SoQt_init(sys.argv[0])
	if myWindow == None: sys.exit(1)

	# Create and set up the selection node
	selectionRoot = SoSelection()
	selectionRoot.ref()
	selectionRoot.policy(SoSelection.SHIFT)
	selectionRoot.addSelectionCallback(mySelectionCB, (void *) TRUE)
	selectionRoot.addDeselectionCallback(mySelectionCB, (void *) FALSE)
   
	# Add a camera and some light
	myCamera = SoPerspectiveCamera()
	selectionRoot.addChild(myCamera)
	selectionRoot.addChild(SoDirectionalLight())

	# Add an event callback so we can receive key press events
	myEventCB = SoEventCallback()
	myEventCB.addEventCallback(SoKeyboardEvent_getClassTypeId(), 
							   myKeyPressCB, selectionRoot)
	selectionRoot.addChild(myEventCB)

	# Add some geometry to the scene
	# a red cube
	cubeRoot = SoSeparator()
	cubeMaterial = SoMaterial()
	cubeTransform = SoTransform()
	cube = SoCube()
	cubeRoot.addChild(cubeTransform)
	cubeRoot.addChild(cubeMaterial)
	cubeRoot.addChild(cube)
	cubeTransform.translation.setValue(-2, 2, 0)
	cubeMaterial.diffuseColor.setValue(.8, 0, 0)
	selectionRoot.addChild(cubeRoot)

	# a blue sphere
	sphereRoot = SoSeparator()
	sphereMaterial = SoMaterial()
	sphereTransform = SoTransform()
	sphere = SoSphere()
	sphereRoot.addChild(sphereTransform)
	sphereRoot.addChild(sphereMaterial)
	sphereRoot.addChild(sphere)
	sphereTransform.translation.setValue(2, 2, 0)
	sphereMaterial.diffuseColor.setValue(0, 0, .8)
	selectionRoot.addChild(sphereRoot)

	# a green cone
	coneRoot = SoSeparator()
	coneMaterial = SoMaterial()
	coneTransform = SoTransform()
	cone = SoCone()
	coneRoot.addChild(coneTransform)
	coneRoot.addChild(coneMaterial)
	coneRoot.addChild(cone)
	coneTransform.translation.setValue(2, -2, 0)
	coneMaterial.diffuseColor.setValue(0, .8, 0)
	selectionRoot.addChild(coneRoot)

	# a magenta cylinder
	cylRoot = SoSeparator()
	cylMaterial = SoMaterial()
	cylTransform = SoTransform()
	cyl = SoCylinder()
	cylRoot.addChild(cylTransform)
	cylRoot.addChild(cylMaterial)
	cylRoot.addChild(cyl)
	cylTransform.translation.setValue(-2, -2, 0)
	cylMaterial.diffuseColor.setValue(.8, 0, .8)
	selectionRoot.addChild(cylRoot)

###############################################################
# CODE FOR The Inventor Mentor STARTS HERE  (part 2)

    cube.setName(objectNames[CUBE])
	sphere.setName(objectNames[SPHERE])
	cone.setName(objectNames[CONE])
	cyl.setName(objectNames[CYL])

# CODE FOR The Inventor Mentor ENDS HERE
###############################################################

    # Create a render area for viewing the scene
	myRenderArea = SoQtRenderArea(myWindow)
	boxhra = SoBoxHighlightRenderAction()
	myRenderArea.setGLRenderAction(boxhra)
	myRenderArea.redrawOnSelectionChange(selectionRoot)
	myRenderArea.setSceneGraph(selectionRoot)
	myRenderArea.setTitle("Motif Selection List")

	# Make the camera see the whole scene
	viewportRegion = myRenderArea.getViewportRegion()
	myCamera.viewAll(selectionRoot, viewportRegion, 2.0)

	# Create a Motif list for selecting objects without picking
	Widget objectList = createList(XtDisplay(myWindow), selectionRoot)

	# Show our application window, and loop forever...
	myRenderArea.show()
	SoQt_show(myWindow)
	SoQt_show(objectList)
	SoQt_mainLoop()

if __name__ == "__main__":
    main()
