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
# This is an example from the Inventor Mentor.
# chapter 15, example 2.
#
# Uses 3 translate1Draggers to change the x, y, and z 
# components of a translation. A calculator engine assembles 
# the components.
# Arranges these draggers along edges of a box containing the
# 3D text to be moved.
# The 3D text and the box are made with SoShapeKits
#

from pivy import *
import sys

def main():
	# Initialize Inventor and Qt
	myWindow = SoQt_init(sys.argv[0])  
	if myWindow == None: sys.exit(1)     

	root = SoSeparator()
	root.ref()

	# Create 3 translate1Draggers and place them in space.
	xDragSep = SoSeparator()
	yDragSep = SoSeparator()
	zDragSep = SoSeparator()
	root.addChild(xDragSep)
	root.addChild(yDragSep)
	root.addChild(zDragSep)
	# Separators will each hold a different transform
	xDragXf = SoTransform()
	yDragXf = SoTransform()
	zDragXf = SoTransform()
	xDragXf.set("translation  0 -4 8")
	yDragXf.set("translation -8  0 8 rotation 0 0 1  1.57")
	zDragXf.set("translation -8 -4 0 rotation 0 1 0 -1.57")
	xDragSep.addChild(xDragXf)
	yDragSep.addChild(yDragXf)
	zDragSep.addChild(zDragXf)

	# Add the draggers under the separators, after transforms
	xDragger = SoTranslate1Dragger()
	yDragger = SoTranslate1Dragger()
	zDragger = SoTranslate1Dragger()
	xDragSep.addChild(xDragger)
	yDragSep.addChild(yDragger)
	zDragSep.addChild(zDragger)

	# Create shape kit for the 3D text
	# The text says 'Slide Cubes To Move Me'
	textKit = SoShapeKit()
	root.addChild(textKit)
	myText3 = SoText3()
	textKit.setPart("shape", myText3)
	myText3.justification(SoText3.CENTER)
	myText3.string.set1Value(0,"Slide Arrows")
	myText3.string.set1Value(1,"To")
	myText3.string.set1Value(2,"Move Me")
	textKit.set("font { size 2}")
	textKit.set("material { diffuseColor 1 1 0}")

	# Create shape kit for surrounding box.
	# It's an unpickable cube, sized as (16,8,16)
	boxKit = SoShapeKit()
	root.addChild(boxKit)
	boxKit.setPart("shape", SoCube())
	boxKit.set("drawStyle { style LINES }")
	boxKit.set("pickStyle { style UNPICKABLE }")
	boxKit.set("material { emissiveColor 1 0 1 }")
	boxKit.set("shape { width 16 height 8 depth 16 }")

	# Create the calculator to make a translation
	# for the text.  The x component of a translate1Dragger's 
	# translation field shows how far it moved in that 
	# direction. So our text's translation is:
	# (xDragTranslate[0],yDragTranslate[0],zDragTranslate[0])
	myCalc = SoCalculator()
	myCalc.ref()
	myCalc.A.connectFrom(xDragger.translation)
	myCalc.B.connectFrom(yDragger.translation)
	myCalc.C.connectFrom(zDragger.translation)
	myCalc.expression("oA = vec3f(A[0],B[0],C[0])")

	# Connect the the translation in textKit from myCalc
	textXf = cast(textKit.getPart("transform",TRUE), "SoTransform")
	textXf.translation.connectFrom(myCalc.oA)
	
	myViewer = SoQtExaminerViewer(myWindow)
	myViewer.setSceneGraph(root)
	myViewer.setTitle("Slider Box")
	myViewer.viewAll()
	myViewer.show()

	SoQt_show(myWindow)
	SoQt_mainLoop()

if __name__ == "__main__":
    main()
