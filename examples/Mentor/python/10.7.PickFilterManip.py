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
# chapter 10, example 7.
#
# This example demonstrates the use of the pick filter
# callback to pick through manipulators.
#
# The scene graph has several objects. Clicking the left
# mouse on an object selects it and adds a manipulator to
# it. Clicking again deselects it and removes the manipulator.
# In this case, the pick filter is needed to deselect the
# object rather than select the manipulator.
#

from sogui import *
from pivy import *
import sys

# Returns path to xform left of the input path tail.
# Inserts the xform if none found. In this example,
# assume that the xform is always the node preceeding
# the selected shape.
def findXform(p):
    # Copy the input path up to tail's parent.
    returnPath = p.copy(0, p.getLength() - 1)

    # Get the parent of the selected shape
    g = cast(p.getNodeFromTail(1), "SoGroup")
    tailNodeIndex = p.getIndexFromTail(0)

    # Check if there is already a transform node
    if tailNodeIndex > 0:
        n = g.getChild(tailNodeIndex - 1)
        if n.isOfType(SoTransform_getClassTypeId()):
            # Append to returnPath and return it.
            returnPath.append(n)
            return returnPath

    # Otherwise, add a transform node.
    xf = SoTransform()
    g.insertChild(xf, tailNodeIndex) # right before the tail
    # Append to returnPath and return it.
    returnPath.append(xf)
    return returnPath

# Returns the manip affecting this path. In this example,
# the manip is always preceeding the selected shape.
def findManip(p):
    # Copy the input path up to tail's parent.
    returnPath = p.copy(0, p.getLength() - 1)

    # Get the index of the last node in the path.
    tailNodeIndex = p.getIndexFromTail(0)

    # Append the left sibling of the tail to the returnPath
    returnPath.append(tailNodeIndex - 1)
    return returnPath

# Add a manipulator to the transform affecting this path
# The first parameter, userData, is not used.
def selCB(void, path):
    if path.getLength() < 2: return
    
    # Find the transform affecting this object
    xfPath = findXform(path)
    xfPath.ref()
    
    # Replace the transform with a manipulator
    manip = SoHandleBoxManip()
    manip.ref()
    manip.replaceNode(xfPath)

    # Unref the xfPath
    xfPath.unref()

# Remove the manipulator affecting this path.
# The first parameter, userData, is not used.
def deselCB(void, path):
    if path.getLength() < 2: return

    # Find the manipulator affecting this object
    manipPath = findManip(path)
    manipPath.ref()

    # Replace the manipulator with a transform 
    manip = cast(manipPath.getTail(), "SoTransformManip")
    manip.replaceManip(manipPath, SoTransform())
    manip.unref()

    # Unref the manipPath
    manipPath.unref()

##############################################################
# CODE FOR The Inventor Mentor STARTS HERE  (part 1)

def pickFilterCB(void, pick):
    filteredPath = None
    
    # See if the picked object is a manipulator. 
    # If so, change the path so it points to the object the manip
    # is attached to.
    p = pick.getPath()
    n = p.getTail()
    if n.isOfType(SoTransformManip_getClassTypeId()):
        # Manip picked! We know the manip is attached
        # to its next sibling. Set up and return that path.
        manipIndex = p.getIndex(p.getLength() - 1)
        filteredPath = p.copy(0, p.getLength() - 1)
        filteredPath.append(manipIndex + 1) # get next sibling
    else:
        filteredPath = p

    return filteredPath

# CODE FOR The Inventor Mentor ENDS HERE  
##############################################################

# Create a sample scene graph
def myText(str, i, color):
    sep  = SoSeparator()
    col  = SoBaseColor()
    xf   = SoTransform()
    text = SoText3()
   
    col.rgb.setValue(color)
    xf.translation.setValue(6.0 * i, 0.0, 0.0)
    text.string(str)
    text.parts(SoText3.FRONT | SoText3.SIDES)
    text.justification(SoText3.CENTER)
    sep.addChild(col)
    sep.addChild(xf)
    sep.addChild(text)
   
    return sep

def buildScene():
    scene = SoSeparator()
    font  = SoFont()
   
    font.size(10)
    scene.addChild(font)
    scene.addChild(myText("O",  0, SbColor(0, 0, 1)))
    scene.addChild(myText("p",  1, SbColor(0, 1, 0)))
    scene.addChild(myText("e",  2, SbColor(0, 1, 1)))
    scene.addChild(myText("n",  3, SbColor(1, 0, 0)))
    # Open Inventor is two words!
    scene.addChild(myText("I",  5, SbColor(1, 0, 1)))
    scene.addChild(myText("n",  6, SbColor(1, 1, 0)))
    scene.addChild(myText("v",  7, SbColor(1, 1, 1)))
    scene.addChild(myText("e",  8, SbColor(0, 0, 1)))
    scene.addChild(myText("n",  9, SbColor(0, 1, 0)))
    scene.addChild(myText("t", 10, SbColor(0, 1, 1)))
    scene.addChild(myText("o", 11, SbColor(1, 0, 0)))
    scene.addChild(myText("r", 12, SbColor(1, 0, 1)))
   
    return scene

def main():
    # Initialization
    mainWindow = SoGui.init(sys.argv[0])
    
    # Create a scene graph. Use the toggle selection policy.
    sel = SoSelection()
    sel.ref()
    sel.policy.setValue(SoSelection.TOGGLE)
    sel.addChild(buildScene())

    # Create a viewer
    viewer = SoGuiExaminerViewer(mainWindow)
    viewer.setSceneGraph(sel)
    viewer.setTitle("Select Through Manips")
    viewer.show()

    # Selection callbacks
    sel.addSelectionCallback(selCB)
    sel.addDeselectionCallback(deselCB)
    sel.setPickFilterCallback(pickFilterCB)
    
    SoGui.show(mainWindow)
    SoGui.mainLoop()

if __name__ == "__main__":
    main()
