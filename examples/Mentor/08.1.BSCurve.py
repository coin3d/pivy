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
# chapter 8, example 1.
#
# This example creates and displays a B-Spline curve.
# The curve is order 3 with 7 control points and a knot
# vector of length 10.  One of its knots has multiplicity
# 2 to illustrate a curve with a spike in it.
#

import sys

from pivy.coin import *
from pivy.sogui import *

floorData = """#Inventor V2.0 ascii\n
Separator {\n
   SpotLight {\n
      cutOffAngle 0.9\n
      dropOffRate 0.2\n 
      location 6 12 2\n 
      direction 0 -1 0\n
   }\n
   ShapeHints {\n
      faceType UNKNOWN_FACE_TYPE\n
   }\n
   Texture2Transform {\n
      #rotation 1.57\n
      scaleFactor 8 8\n
   }\n
   Texture2 {\n
      filename oak.rgb\n
   }\n
   NormalBinding {\n
        value  PER_PART\n
   }\n
   Material { diffuseColor 1 1 1 specularColor 1 1 1 shininess 0.4 }\n
   DEF FloorPanel Separator {\n
      DEF FloorStrip Separator {\n
         DEF FloorBoard Separator {\n
            Normal { vector 0 1 0 }\n
            TextureCoordinate2 {\n
               point [ 0 0, 0.5 0, 0.5 2, 0.5 4, 0.5 6,\n
                       0.5 8, 0 8, 0 6, 0 4, 0 2 ] }\n
            Coordinate3 {\n
               point [ 0 0 0, .5 0 0, .5 0 -2, .5 0 -4, .5 0 -6,\n
                       .5 0 -8, 0 0 -8, 0 0 -6, 0 0 -4, 0 0 -2, ]\n
            }\n
            FaceSet { numVertices 10 }\n
            BaseColor { rgb 0.3 0.1 0.0 }\n
            Translation { translation 0.125 0 -0.333 }\n
            Cylinder { parts TOP radius 0.04167 height 0.002 }\n
            Translation { translation 0.25 0 0 }\n
            Cylinder { parts TOP radius 0.04167 height 0.002 }\n
            Translation { translation 0 0 -7.333 }\n
            Cylinder { parts TOP radius 0.04167 height 0.002 }\n
            Translation { translation -0.25 0 0 }\n
            Cylinder { parts TOP radius 0.04167 height 0.002 }\n
         }\n
         Translation { translation 0 0 8.03 }\n
         USE FloorBoard\n
         Translation { translation 0 0 8.04 }\n
         USE FloorBoard\n
      }\n
      Translation { translation 0.53 0 -0.87 }\n
      USE FloorStrip\n
      Translation { translation 0.53 0 -2.3 }\n
      USE FloorStrip\n
      Translation { translation 0.53 0 1.3 }\n
      USE FloorStrip\n
      Translation { translation 0.53 0 1.1 }\n
      USE FloorStrip\n
      Translation { translation 0.53 0 -0.87 }\n
      USE FloorStrip\n
      Translation { translation 0.53 0 1.7 }\n
      USE FloorStrip\n
      Translation { translation 0.53 0 -0.5 }\n
      USE FloorStrip\n
   }\n
   Translation { translation 4.24 0 0 }\n
   USE FloorPanel\n
   Translation { translation 4.24 0 0 }\n
   USE FloorPanel\n
}"""

##############################################################
# CODE FOR The Inventor Mentor STARTS HERE

# The control points for this curve
pts = (
   ( 4.0, -6.0,  6.0),
   (-4.0,  1.0,  0.0),
   (-1.5,  5.0, -6.0),
   ( 0.0,  2.0, -2.0),
   ( 1.5,  5.0, -6.0),
   ( 4.0,  1.0,  0.0),
   (-4.0, -6.0,  6.0))

# The knot vector
knots = (1, 2, 3, 4, 5, 5, 6, 7, 8, 9)

# Create the nodes needed for the B-Spline curve.
def makeCurve():
    curveSep = SoSeparator()
    curveSep.ref()
    
    # Set the draw style of the curve.
    drawStyle = SoDrawStyle()
    drawStyle.lineWidth = 4
    curveSep.addChild(drawStyle)
    
    # Define the NURBS curve including the control points
    # and a complexity.
    complexity = SoComplexity()
    controlPts = SoCoordinate3()
    curve      = SoNurbsCurve()
    complexity.value = 0.8
    controlPts.point.setValues(0, 7, pts)
    curve.numControlPoints = 7
    curve.knotVector.setValues(0, 10, knots)
    curveSep.addChild(complexity)
    curveSep.addChild(controlPts)
    curveSep.addChild(curve)
    
    curveSep.unrefNoDelete()
    return curveSep

# CODE FOR The Inventor Mentor ENDS HERE
##############################################################

def main():   
    # Initialize Inventor and Qt
    appWindow = SoGui.init(sys.argv[0])
    if appWindow == None:
        sys.exit(1)
        
    root = SoSeparator()
    root.ref()
    
    # Create the scene graph for the heart
    heart    = SoSeparator()
    curveSep = makeCurve()
    lmodel   = SoLightModel()
    clr      = SoBaseColor()
    
    lmodel.model = SoLightModel.BASE_COLOR
    clr.rgb = (1.0, 0.0, 0.1)
    heart.addChild(lmodel)
    heart.addChild(clr)
    heart.addChild(curveSep)
    root.addChild(heart)
    
    # Create the scene graph for the floor
    floor = SoSeparator()
    xlate = SoTranslation()
    rot   = SoRotation()
    scale = SoScale()
    input = SoInput()
    
    input.setBuffer(floorData)
    result = SoDB.readAll(input)
    xlate.translation = (-12.0, -5.0, -5.0)
    scale.scaleFactor = (2.0, 1.0, 2.0)
    rot.rotation.setValue(SbRotation(SbVec3f(0.0, 1.0, 0.0), M_PI/2.0))
    floor.addChild(rot)
    floor.addChild(xlate)
    floor.addChild(scale)
    floor.addChild(result)
    root.addChild(floor)
    
    # Create the scene graph for the heart's shadow
    shadow = SoSeparator()
    shmdl  = SoLightModel()
    shmtl  = SoMaterial()
    shclr  = SoBaseColor()
    shxl   = SoTranslation()
    shscl  = SoScale()
    
    shmdl.model = SoLightModel.BASE_COLOR
    shclr.rgb = (0.21, 0.15, 0.09)
    shmtl.transparency = 0.5
    shxl.translation = (0.0, -4.9, 0.0)
    shscl.scaleFactor = (1.0, 0.0, 1.0)
    shadow.addChild(shmtl)
    shadow.addChild(shmdl)
    shadow.addChild(shclr)
    shadow.addChild(shxl)
    shadow.addChild(shscl)
    shadow.addChild(curveSep)
    root.addChild(shadow)
    
    # Initialize an Examiner Viewer
    viewer = SoGuiExaminerViewer(appWindow)
    viewer.setSceneGraph(root)
    viewer.setTitle("B-Spline Curve")
    cam = viewer.getCamera()
    cam.position = (-6.0, 8.0, 20.0)
    cam.pointAt(SbVec3f(0.0, -2.0, -4.0))
    viewer.show()
    
    SoGui.show(appWindow)
    SoGui.mainLoop()

if __name__ == "__main__":
    main()
