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
# chapter 16, example 2.
#
# This example builds a render area in a window supplied by
# the application and a Material Editor in its own window.
# It uses callbacks for the component to report new values.
#

from pivy import *
import sys

#  This is called by the Material Editor when a value changes
def myMaterialEditorCB(userData, newMtl):
	myMtl = cast(userData, "SoMaterial")

	# Copy all the fields from the new material
	myMtl.copyFieldValues(newMtl)

def main():
	# Initialize Inventor and Gtk
	myWindow = SoGtk_init(sys.argv[0])  
	if myWindow == None: sys.exit(1)     

	# Build the render area in the applications main window
	myRenderArea = SoGtkRenderArea(myWindow)
	myRenderArea.setSize(SbVec2s(200, 200))
   
	# Build the Material Editor in its own window
	myEditor = SoGtkMaterialEditor()
   
	# Create a scene graph
	root = SoSeparator()
	myCamera = SoPerspectiveCamera()
	myMaterial = SoMaterial()
   
	root.ref()
	myCamera.position.setValue(0.212482, -0.881014, 2.5)
	myCamera.heightAngle(M_PI/4)
	root.addChild(myCamera)
	root.addChild(SoDirectionalLight())
	root.addChild(myMaterial)

	# Read the geometry from a file and add to the scene
	myInput = SoInput()
	if not myInput.openFile("dogDish.iv"):
		sys.exit(1)
	geomObject = SoDB_readAll(myInput)
	if geomObject == None:
		sys.exit(1)
	root.addChild(geomObject)

	# Add a callback for when the material changes
	myEditor.addPythonMaterialChangedCallback(myMaterialEditorCB, myMaterial) 

	# Set the scene graph
	myRenderArea.setSceneGraph(root)

	# Show the main window and the Material Editor
	myRenderArea.setTitle("Editor Callback")
	myRenderArea.show()
	SoGtk_show(myWindow)
	myEditor.show()

	# Loop forever
	SoGtk_mainLoop()

if __name__ == "__main__":
    main()
