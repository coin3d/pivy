#!/usr/bin/env python

###
# Copyright (c) 2005, Øystein Handegard <handegar@sim.no>
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

import math
from pivy.coin import *
from pivy.sogui import *

##############################################################

def generateColoredLights(distance):
    scenegraph = SoSeparator()
    rotor = SoRotor()
    rotor.rotation = (1, 1, 1, 0)
    rotor.speed = 0.2

    redlight = SoPointLight()
    redlight.color = (1, 0, 0)
    redlight.location = (0, distance, 0)
    
    goldlight = SoPointLight()
    goldlight.color = (1, 185.0/256, 75.0/256)
    goldlight.location = (distance, 0, 0)
    
    trans = SoTranslation()
    trans.translation = (distance, 0, distance)

    scenegraph.addChild(rotor)
    scenegraph.addChild(redlight)
    scenegraph.addChild(rotor)
    scenegraph.addChild(goldlight)
    return scenegraph
    
def generateTile(height, width, thickness):
    h = height*(1-(8*thickness))
    w = width*(1-(8*thickness))
    s = (8*thickness)+1.0
    t = -thickness

    points = ((0, -w/2.0, -h/2.0), (0, w/2.0, -h/2.0), (0, w/2.0, h/2.0), (0, -w/2.0, h/2.0),
              (t, -(s*w)/2.0, -(s*h)/2.0), (t, (s*w)/2.0, (-s*h)/2.0), (t, (s*w)/2.0, (s*h)/2.0), (t, (-s*w)/2.0, (s*h)/2.0))
    indices = (0, 1, 2, 3, -1,  4, 5, 1, 0, -1,  5, 6, 2, 1, -1,  3, 2, 6, 7, -1,  0, 3, 7, 4, -1 )

    coordset = SoCoordinate3()
    coordset.point.setValues(0, len(points), points)

    faceset = SoIndexedFaceSet()
    faceset.coordIndex.setValues(0, len(indices), indices)

    sep = SoSeparator()
    sep.addChild(coordset)
    sep.addChild(faceset)
    
    return sep
    

def generateMirrorBall(radius, tileheight, tilewidth):
    root = SoSeparator()
    
    tilethickness = ((tilewidth + tileheight)/2.0)/50.0 # looks nice
    tile = generateTile(tileheight, tilewidth, tilethickness)
        
    radiustrans = SoTranslation()
    radiustrans.translation = SbVec3f(radius,0,0)

    mirrormat = SoMaterial()
    mirrormat.specularColor = (1, 1, 1)
    mirrormat.diffuseColor = (0.2, 0.2, 0.2)    
    mirrormat.shinyness = 0.5
    root.addChild(mirrormat)

    rot1 = SbRotation()
    rot2 = SbRotation() 

    x = M_PI
    anglesteplong = M_PI / (2.0 * math.asin(tileheight / (2.0 * radius)))
    anglesteplat = M_PI / (2.0 * math.asin(tilewidth / (2.0 * radius)))

    while x > 0:
        y = M_PI*2
        while y > 0:
            sep = SoSeparator()
            rot1.setValue(SbVec3f(0,0,1), x)
            rot2.setValue(SbVec3f(1, 0, 0), y)
            y = y - (M_PI*2 / ((anglesteplong*2)*math.sin(x)))            
            rot = SoRotation()
            rot.rotation = (rot1*rot2)
            sep.addChild(rot)
            sep.addChild(radiustrans)
            sep.addChild(tile)
            root.addChild(sep)
        x = x - (M_PI / anglesteplat)

    return root
    
##############################################################

def main():
    myWindow = SoGui.init(sys.argv[0])
    if myWindow == None: sys.exit(1)
    
    # Radius and tile size of the mirror-ball
    radius = 8
    tilesizex = 1
    tilesizey = 0.8

    # Create rotating lights around the ball
    lights = generateColoredLights(radius * 50.0)
    lights.addChild(SoResetTransform())

    # Generate mirror ball.
    print "Generating a mirror ball with radius %d and tile size %.1fx%.1f..." % (radius, tilesizex, tilesizey)
    lights.addChild(generateMirrorBall(radius, tilesizex, tilesizey))
    print "...finished."

    # setup viewer
    myViewer = SoGuiExaminerViewer(myWindow)
    myViewer.setSceneGraph(lights)
    myViewer.setTitle("Examiner Viewer")
    myViewer.viewAll()
    myViewer.show()

    SoGui.show(myWindow)
    SoGui.mainLoop()

    return 0

if __name__ == "__main__":
    sys.exit(main())
