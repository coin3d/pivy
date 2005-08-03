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
# chapter 3, example 1.
#
# This code shows how to create a molecule out of 3 spherical
# atoms.  The molecule illustrates how the ordering of nodes
# within a scene graph affects the rendered image.
#
#

import sys

from pivy.coin import *
from pivy.sogui import *

def makeWaterMolecule():
##############################################################
#  CODE FOR The Inventor Mentor STARTS HERE

    # Construct all parts
    waterMolecule = SoGroup()  # water molecule

    oxygen = SoGroup()         # oxygen atom
    redPlastic = SoMaterial()
    sphere1 = SoSphere()
    
    hydrogen1 = SoGroup()      # hydrogen atoms
    hydrogen2 = SoGroup()
    hydrogenXform1 = SoTransform()
    hydrogenXform2 = SoTransform()
    whitePlastic = SoMaterial()
    sphere2 = SoSphere()
    sphere3 = SoSphere()
    
    # Set all field values for the oxygen atom
    redPlastic.ambientColor = (1.0, 0.0, 0.0)
    redPlastic.diffuseColor = (1.0, 0.0, 0.0) 
    redPlastic.specularColor = (0.5, 0.5, 0.5)
    redPlastic.shininess = 0.5
    
    # Set all field values for the hydrogen atoms
    hydrogenXform1.scaleFactor = (0.75, 0.75, 0.75)  
    hydrogenXform1.translation = (0.0, -1.2, 0.0)  
    hydrogenXform2.translation = (1.1852, 1.3877, 0.0)
    whitePlastic.ambientColor = (1.0, 1.0, 1.0)  
    whitePlastic.diffuseColor = (1.0, 1.0, 1.0) 
    whitePlastic.specularColor = (0.5, 0.5, 0.5)
    whitePlastic.shininess = 0.5
    
    # Create a hierarchy
    waterMolecule.addChild(oxygen)   
    waterMolecule.addChild(hydrogen1)   
    waterMolecule.addChild(hydrogen2)
    
    oxygen.addChild(redPlastic)
    oxygen.addChild(sphere1)
    hydrogen1.addChild(hydrogenXform1)
    hydrogen1.addChild(whitePlastic)
    hydrogen1.addChild(sphere2)
    hydrogen2.addChild(hydrogenXform2)
    hydrogen2.addChild(sphere3)

## CODE FOR The Inventor Mentor ENDS HERE
##############################################################

    return waterMolecule

def main():
    # Initialize Inventor and Qt
    myWindow = SoGui.init(sys.argv[0])
    if myWindow == None: sys.exit(1)

    root = SoSeparator()
    root.ref()

    # This function contains our code fragment.
    root.addChild(makeWaterMolecule())

    myViewer = SoGuiExaminerViewer(myWindow)
    myViewer.setSceneGraph(root)
    myViewer.setTitle("H two O")
    myViewer.show()
    myViewer.viewAll()

    SoGui.show(myWindow)
    SoGui.mainLoop()

if __name__ == "__main__":
    main()
