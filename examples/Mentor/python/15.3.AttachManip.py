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
# volume 1, chapter 15, example 3.
#
# Manipulator attachment example.
#
# The scene graph has an SoWrapperKit, a cube and a sphere.
# A file containing a luxo lamp is read in as the 'contents'
# part of the SoWrapperKit.
# When the user picks on the SoWrapperKit (lamp), the kit's 
# "transform" part is replaced with an SoTransformBoxManip.
# Alternatively, when the user picks the sphere, the
# sphere's associated transform is replaced by an
# SoHandleBoxManip.  Picking the cube causes an 
# SoTrackballManip to replace the cube's transform.
# 
# Manipulator callbacks are used to change
# the color of the object being manipulated.
# 
# Note that for illustration purposes, the
# cube and SoWrapperKit already have transform nodes 
# associated with them; the sphere does not. In all cases, 
# the routine createTransformPath() is used to find the 
# transform node that affects the picked object.
#

from pivy import *
import sys

# global data
myHandleBox      = None
myTrackball      = None
myTransformBox   = None
handleBoxPath    = None
trackballPath    = None
transformBoxPath = None

# Is this node of a type that is influenced by transforms?
def isTransformable(myNode):
    if myNode.isOfType(SoGroup_getClassTypeId()) or \
       myNode.isOfType(SoShape_getClassTypeId()) or \
       myNode.isOfType(SoCamera_getClassTypeId()) or \
       myNode.isOfType(SoLight_getClassTypeId()):
        return TRUE
    else: 
        return FALSE

#  Create a path to the transform node that affects the tail
#  of the input path.  Three possible cases:
#   [1] The path-tail is a node kit. Just ask the node kit for
#       a path to the part called "transform"
#   [2] The path-tail is NOT a group.  Search siblings of path
#       tail from right to left until you find a transform. If
#       none is found, or if another transformable object is 
#       found (shape,group,light,or camera), then insert a 
#       transform just to the left of the tail. This way, the 
#       manipulator only effects the selected object.
#   [3] The path-tail IS a group.  Search its children left to
#       right until a transform is found. If a transformable
#       node is found first, insert a transform just left of 
#       that node.  This way the manip will affect all nodes
#       in the group.
def createTransformPath(inputPath):
    pathLength = inputPath.getLength()
    if pathLength < 2: # Won't be able to get parent of tail
        return None

    tail = inputPath.getTail()

    # CASE 1: The tail is a node kit.
    # Nodekits have built in policy for creating parts.
    # The kit copies inputPath, then extends it past the 
    # kit all the way down to the transform. It creates the
    # transform if necessary.
    if tail.isOfType(SoBaseKit_getClassTypeId()):
        kit = cast(tail, "SoBaseKit")
        return kit.createPathToPart("transform",TRUE,inputPath)

    editXf = None
    parent = None
    existedBefore = FALSE

    # CASE 2: The tail is not a group.
    isTailGroup = tail.isOfType(SoGroup_getClassTypeId())
    if not isTailGroup:
        # 'parent' is node above tail. Search under parent right
        # to left for a transform. If we find a 'movable' node
        # insert a transform just left of tail.  
        parent = cast(inputPath.getNode(pathLength - 2), "SoGroup")
        tailIndx = parent.findChild(tail)

        for i in range(tailIndx, -1, -1):
            if editXf != None:
                break
            myNode = parent.getChild(i)
            if myNode.isOfType(SoTransform_getClassTypeId()):
                editXf = cast(myNode, "SoTransform")
            elif i != tailIndx and isTransformable(myNode):
                break

        if editXf == None:
            existedBefore = FALSE
            editXf = SoTransform()
            parent.insertChild(editXf, tailIndx)
        else:
            existedBefore = TRUE

    # CASE 3: The tail is a group.
    else:
        # Search the children from left to right for transform 
        # nodes. Stop the search if we come to a movable node.
        # and insert a transform before it.
        parent = cast(tail, "SoGroup")
        for i in range(parent.getNumChildren()):
            if editXf != NULL:
                break
            myNode = parent.getChild(i)
            if myNode.isOfType(SoTransform_getClassTypeId()):
                editXf = cast(myNode, "SoTransform")
            elif isTransformable(myNode):
                break

        if editXf == None:
            existedBefore = FALSE
            editXf = SoTransform()
            parent.insertChild(editXf, i)
        else :
            existedBefore = TRUE

    # Create 'pathToXform.' Copy inputPath, then make last
    # node be editXf.
    pathToXform = None
    pathToXform = inputPath.copy()
    pathToXform.ref()
    if not isTailGroup: # pop off the last entry.
        pathToXform.pop()
    # add editXf to the end
    xfIndex = parent.findChild(editXf)
    pathToXform.append(xfIndex)
    pathToXform.unrefNoDelete()
    
    return(pathToXform)

# This routine is called when an object
# gets selected. We determine which object
# was selected, then call replaceNode()
# to replace the object's transform with
# a manipulator.
def selectionCallback(void, # user data is not used
                      selectionPath):
    global myHandleBox, myTrackball, myTransformBox, handleBoxPath
    global trackballPath, transformBoxPath

    # Attach the manipulator.
    # Use the convenience routine to get a path to
    # the transform that effects the selected object.
    xformPath = createTransformPath(selectionPath)
    if xformPath == None: return
    xformPath.ref()

    # Attach the handle box to the sphere,
    # the trackball to the cube
    # or the transformBox to the wrapperKit
    if selectionPath.getTail().isOfType(SoSphere_getClassTypeId()):
        handleBoxPath = xformPath
        myHandleBox.replaceNode(xformPath)
    elif selectionPath.getTail().isOfType(SoCube_getClassTypeId()):
        trackballPath = xformPath
        myTrackball.replaceNode(xformPath)
    elif selectionPath.getTail().isOfType(SoWrapperKit_getClassTypeId()):
        transformBoxPath = xformPath
        myTransformBox.replaceNode(xformPath)

# This routine is called whenever an object gets
# deselected. It detaches the manipulator from
# the transform node, and removes it from the 
# scene graph that will not be visible.
def deselectionCallback(void, # user data is not used
                        deselectionPath):
    global myHandleBox, myTrackball, myTransformBox, handleBoxPath
    global trackballPath, transformBoxPath
    
    if deselectionPath.getTail().isOfType(SoSphere_getClassTypeId()):
        myHandleBox.replaceManip(handleBoxPath,None)
        handleBoxPath.unref()
    elif deselectionPath.getTail().isOfType(SoCube_getClassTypeId()):
        myTrackball.replaceManip(trackballPath,None)
        trackballPath.unref()
    elif deselectionPath.getTail().isOfType(SoWrapperKit_getClassTypeId()):
        myTransformBox.replaceManip(transformBoxPath,None)
        transformBoxPath.unref()

# This is called when a manipulator is
# about to begin manipulation.
def dragStartCallback(myMaterial, # user data
                      dragger):   # callback data not used
    (cast(myMaterial, "SoMaterial")).diffuseColor.setValue(1,.2,.2)

# This is called when a manipulator is
# done manipulating.
def dragFinishCallback(myMaterial, # user data
                       dragger):   # callback data not used
    (cast(myMaterial, "SoMaterial")).diffuseColor.setValue(.8,.8,.8)

def main():
    global myHandleBox, myTrackball, myTransformBox
    
    # Initialize Inventor and Qt
    myWindow = SoQt_init(sys.argv[0])  
    if myWindow == None: sys.exit(1)     

    # create and set up the selection node
    selectionRoot = SoSelection()
    selectionRoot.ref()
    selectionRoot.addPythonSelectionCallback(selectionCallback, None)
    selectionRoot.addPythonDeselectionCallback(deselectionCallback, None)

    # create the scene graph
    root = SoSeparator()
    selectionRoot.addChild(root)

    # Read a file into contents of SoWrapperKit 
    # Translate it to the right.
    myWrapperKit = SoWrapperKit()
    root.addChild(myWrapperKit)
    myInput = SoInput()
    if not myInput.openFile("luxo.iv"):
        sys.exit(1)
    objectFromFile = SoDB_readAll(myInput)
    if objectFromFile == None:
        sys.exit(1)
    myWrapperKit.setPart("contents",objectFromFile)
    myWrapperKit.set("transform { translation 3 -1 0 }")
    wrapperMat = cast(myWrapperKit.getPart("material",TRUE), "SoMaterial")
    wrapperMat.diffuseColor.setValue(.8, .8, .8)

    # Create a cube with its own transform.
    cubeRoot  = SoSeparator()
    cubeXform = SoTransform()
    cubeXform.translation.setValue(-4, 0, 0)
    root.addChild(cubeRoot)
    cubeRoot.addChild(cubeXform)

    cubeMat = SoMaterial()
    cubeMat.diffuseColor.setValue(.8, .8, .8)
    cubeRoot.addChild(cubeMat)
    cubeRoot.addChild(SoCube())

    # add a sphere node without a transform
    # (one will be added when we attach the manipulator)
    sphereRoot = SoSeparator()
    sphereMat = SoMaterial()
    root.addChild(sphereRoot)
    sphereRoot.addChild(sphereMat)
    sphereRoot.addChild(SoSphere())
    sphereMat.diffuseColor.setValue(.8, .8, .8)

    # create the manipulators
    myHandleBox = SoHandleBoxManip()
    myHandleBox.ref()
    myTrackball = SoTrackballManip()
    myTrackball.ref()
    myTransformBox = SoTransformBoxManip()
    myTransformBox.ref()

    # Get the draggers and add callbacks to them. Note
    # that you don't put callbacks on manipulators. You put
    # them on the draggers which handle events for them. 
    myDragger = myTrackball.getDragger()
    myDragger.addPythonStartCallback(dragStartCallback,cubeMat)
    myDragger.addPythonFinishCallback(dragFinishCallback,cubeMat)

    myDragger = myHandleBox.getDragger()
    myDragger.addPythonStartCallback(dragStartCallback,sphereMat)
    myDragger.addPythonFinishCallback(dragFinishCallback,sphereMat)

    myDragger = myTransformBox.getDragger()
    myDragger.addPythonStartCallback(dragStartCallback,wrapperMat)
    myDragger.addPythonFinishCallback(dragFinishCallback,wrapperMat)

    myViewer = SoQtExaminerViewer(myWindow)
    myViewer.setSceneGraph(selectionRoot)
    myViewer.setTitle("Attaching Manipulators")
    myViewer.show()
    myViewer.viewAll()
    
    SoQt_show(myWindow)
    SoQt_mainLoop()

if __name__ == "__main__":
    main()
