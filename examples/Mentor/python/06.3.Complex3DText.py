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
#     the documentation and#or other materials provided with the
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
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES LOSS OF USE,
# DATA, OR PROFITS OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

###
# This is an example from the Inventor Mentor,
# chapter 6, example 3.
#
# This example renders arguments as text within an
# SoXTExaminerViewer.  It is a little fancier than 6.2.
#

from pivy import *
import sys

def main():
	# Initialize Inventor and Qt
	myWindow = SoQt_init(sys.argv[0])
	if myWindow == None: sys.exit(1)

	root = SoGroup()
	root.ref()

	# Set up camera 
	myCamera = SoPerspectiveCamera()
	myCamera.position.setValue(0, -(len(sys.argv) - 1) / 2, 10)
	myCamera.nearDistance.setValue(5.0)
	myCamera.farDistance.setValue(15.0)
	root.addChild(myCamera)

	# Let's make the front of the text white, 
	# and the sides and back shiny yellow
	myMaterial = SoMaterial()
	colors = [SbColor()]*3
	# diffuse
	colors[0].setValue(1, 1, 1)
	colors[1].setValue(1, 1, 0)
	colors[2].setValue(1, 1, 0)
	myMaterial.diffuseColor.setValues(0, 3, colors)

	# specular
	colors[0].setValue(1, 1, 1)
	# Note: Inventor 2.1 doesn't support multiple specular colors.
	# 
    # colors[1].setValue(1, 1, 0)
    # colors[2].setValue(1, 1, 0)
    # myMaterial.specularColor.setValues(0, 3, colors)
	#
	myMaterial.specularColor.setValue(colors[0])
	myMaterial.shininess.setValue(.1)
	root.addChild(myMaterial)

	# Choose a font likely to exist.
	myFont = SoFont()
	myFont.name("Times-Roman")
	root.addChild(myFont)

	# Specify a beveled cross-section for the text
	myProfileCoords = SoProfileCoordinate2()
	coords = [SbVec2f()]*4
	coords[0].setValue( .00, .00)
	coords[1].setValue( .25, .25)
	coords[2].setValue(1.25, .25)
	coords[3].setValue(1.50, .00)
	myProfileCoords.point.setValues(0, 4, coords)
	root.addChild(myProfileCoords)

	myLinearProfile = SoLinearProfile()
	index = (0, 1, 2, 3)
	myLinearProfile.index.setValues(0, 4, index)
	root.addChild(myLinearProfile)

	# Set the material binding to PER_PART
	myMaterialBinding = SoMaterialBinding()
	myMaterialBinding.value.setValue(SoMaterialBinding.PER_PART)
	root.addChild(myMaterialBinding)

	# Add the text
	myText3 = SoText3()
	myText3.string.setValue("Beveled Text")
	myText3.justification.setValue(SoText3.CENTER)
	myText3.parts.setValue(SoText3.ALL)
   
	root.addChild(myText3)

	myViewer = SoQtExaminerViewer(myWindow)
	myViewer.setSceneGraph(root)
	myViewer.setTitle("Complex 3D Text")
	myViewer.show()
	myViewer.viewAll()

	SoQt_show(myWindow)
	SoQt_mainLoop()

if __name__ == "__main__":
	main()

