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
# chapter 17, example 2.
#
# Example of combining Inventor and OpenGL rendering.
# Create an Inventor render area and draw a red cube 
# and a blue sphere.  Render the floor with OpenGL 
# through a Callback node.
#

from pivy import *
from OpenGL.GL import *
import sys

floorObj = []

# Build a scene with two objects and some light
def buildScene(root):
    # Some light
    root.addChild(SoLightModel())
    root.addChild(SoDirectionalLight())

    # A red cube translated to the left and down
    myTrans = SoTransform()
    myTrans.translation.setValue(-2.0, -2.0, 0.0)
    root.addChild(myTrans)

    myMtl = SoMaterial()
    myMtl.diffuseColor.setValue(1.0, 0.0, 0.0)
    root.addChild(myMtl)
   
    root.addChild(SoCube())

    # A blue sphere translated right
    myTrans = SoTransform()
    myTrans.translation.setValue(4.0, 0.0, 0.0)
    root.addChild(myTrans)

    myMtl = SoMaterial()
    myMtl.diffuseColor.setValue(0.0, 0.0, 1.0)
    root.addChild(myMtl)
   
    root.addChild(SoSphere())

# Build the floor that will be rendered using OpenGL.
def buildFloor():
    global floorObj
    a = 0

    for i in range(9):
        for j in range(9):
            floorObj.append([-5.0 + j*1.25, 0.0, -5.0 + i*1.25])
            a+=1
            
# Draw the lines that make up the floor, using OpenGL
def drawFloor():
    global floorObj

    glBegin(GL_LINES)
    for i in range(4):
        glVertex3fv(floorObj[i*18])
        glVertex3fv(floorObj[(i*18)+8])
        glVertex3fv(floorObj[(i*18)+17])
        glVertex3fv(floorObj[(i*18)+9])
    i+=1
    glVertex3fv(floorObj[i*18])
    glVertex3fv(floorObj[(i*18)+8])
    glEnd()

    glBegin(GL_LINES)
    for i in range(4):
        glVertex3fv(floorObj[i*2])
        glVertex3fv(floorObj[(i*2)+72])
        glVertex3fv(floorObj[(i*2)+73])
        glVertex3fv(floorObj[(i*2)+1])

    i+=1
    glVertex3fv(floorObj[i*2])
    glVertex3fv(floorObj[(i*2)+72])
    glEnd()

# Callback routine to render the floor using OpenGL
def myCallbackRoutine(void, action):
    # only render the floor during GLRender actions:
    if not action.isOfType(SoGLRenderAction_getClassTypeId()): return
   
    glPushMatrix()
    glTranslatef(0.0, -3.0, 0.0)
    glColor3f(0.0, 0.7, 0.0)
    glLineWidth(2)
    glDisable(GL_LIGHTING)  # so we don't have to set normals
    drawFloor()
    glEnable(GL_LIGHTING)   
    glLineWidth(1)
    glPopMatrix()
   
    # With Inventor 2.1, it's necessary to reset SoGLLazyElement after
    # making calls (such as glColor3f()) that affect material state.
    # In this case, the diffuse color and light model are being modified,
    # so the logical-or of DIFFUSE_MASK and LIGHT_MODEL_MASK is passed 
    # to SoGLLazyElement::reset().  
    # Additional information can be found in the publication
    # "Open Inventor 2.1 Porting and Performance Tips"
  
    # state = action.getState()
    # lazyElt = cast(SoLazyElement_getInstance(state), "SoGLLazyElement")
    # lazyElt.reset(state, (SoLazyElement.DIFFUSE_MASK)|(SoLazyElement.LIGHT_MODEL_MASK))

def main():
    # Initialize Inventor utilities
    myWindow = SoQt_init("Example 17.1")

    buildFloor()

    # Build a simple scene graph, including a camera and
    # a SoCallback node for performing some GL rendering.
    root = SoSeparator()
    root.ref()

    myCamera = SoPerspectiveCamera()
    myCamera.position.setValue(0.0, 0.0, 5.0)
    myCamera.heightAngle(M_PI/2.0)  # 90 degrees
    myCamera.nearDistance(2.0)
    myCamera.farDistance(12.0)
    root.addChild(myCamera)

    myCallback = SoCallback()
    myCallback.setCallback(myCallbackRoutine)
    root.addChild(myCallback)

    buildScene(root)
   
    # Initialize an Inventor Qt RenderArea and draw the scene.
    myRenderArea = SoQtRenderArea(myWindow)
    myRenderArea.setSceneGraph(root)
    myRenderArea.setTitle("OpenGL Callback")
    myRenderArea.setBackgroundColor(SbColor(.8, .8, .8))
    myRenderArea.show()
    drawFloor()
    
    SoQt_show(myWindow)
    SoQt_mainLoop()

if __name__ == "__main__":
    main()
