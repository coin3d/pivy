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
# chapter 6, example 2.
#
# This example renders a globe and uses 3D text to label the
# continents Africa and Asia.
#

from pivy import *
import sys

def main():
	# Initialize Inventor and Gtk
	myWindow = SoGtk_init(sys.argv[0])
	if myWindow == None: sys.exit(1)

	root = SoGroup()
	root.ref()

	# Choose a font
	myFont = SoFont()
	myFont.name("Times-Roman")
	myFont.size.setValue(.2)
	root.addChild(myFont)

	# We'll color the front of the text white, and the sides 
	# dark grey. So use a materialBinding of PER_PART and
	# two diffuseColor values in the material node.
	myMaterial = SoMaterial()
	myBinding = SoMaterialBinding()
	myMaterial.diffuseColor.set1Value(0,SbColor(1,1,1))
	myMaterial.diffuseColor.set1Value(1,SbColor(.1,.1,.1))
	myBinding.value(SoMaterialBinding.PER_PART)
	root.addChild(myMaterial)
	root.addChild(myBinding)

	# Create the globe
	sphereSep = SoSeparator()
	myTexture2 = SoTexture2()
	sphereComplexity = SoComplexity()
	sphereComplexity.value(0.55)
	root.addChild(sphereSep)
	sphereSep.addChild(myTexture2)
	sphereSep.addChild(sphereComplexity)
	sphereSep.addChild(SoSphere())
	myTexture2.filename("globe.rgb")

	# Add Text3 for AFRICA, transformed to proper location.
	africaSep = SoSeparator()
	africaTransform = SoTransform()
	africaText = SoText3()
	africaTransform.rotation.setValue(SbVec3f(0,1,0),.4)
	africaTransform.translation.setValue(.25,.0,1.25)
	africaText.parts(SoText3.ALL)
	africaText.string("AFRICA")
	root.addChild(africaSep)
	africaSep.addChild(africaTransform)
	africaSep.addChild(africaText)

	# Add Text3 for ASIA, transformed to proper location.
	asiaSep = SoSeparator()
	asiaTransform = SoTransform()
	asiaText = SoText3()
	asiaTransform.rotation.setValue(SbVec3f(0,1,0),1.5)
	asiaTransform.translation.setValue(.8,.6,.5)
	asiaText.parts(SoText3.ALL)
	asiaText.string("ASIA")
	root.addChild(asiaSep)
	asiaSep.addChild(asiaTransform)
	asiaSep.addChild(asiaText)

	myViewer = SoGtkExaminerViewer(myWindow)
	myViewer.setSceneGraph(root)
	myViewer.setTitle("3D Text")

	# In Inventor 2.1, if the machine does not have hardware texture
	# mapping, we must override the default drawStyle to display textures.
	myViewer.setDrawStyle(SoGtkViewer.STILL, SoGtkViewer.VIEW_AS_IS)

	myViewer.show()
	myViewer.viewAll()

	SoGtk_show(myWindow)
	SoGtk_mainLoop()

if __name__ == "__main__":
	main()
