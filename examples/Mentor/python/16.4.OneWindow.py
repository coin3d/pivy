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
# chapter 16, example 4.
#
# This example builds a render area and Material Editor within 
# a window supplied by the application. It uses a Motif form 
# widget to lay both components inside the same window.  
# It attaches the editor to the material of an object.
#

from pivy import *
import sys

def main():
	# Initialize Inventor and Gtk
	myWindow = SoGtk_init(sys.argv[0])
   
	# Build the form to hold both components
	myForm = GtkCreateWidget("Form", xmFormWidgetClass, myWindow, None, 0)
   
	# Build the render area and Material Editor
	myRenderArea = SoGtkRenderArea(myForm)
	myRenderArea.setSize(SbVec2s(200, 200))
	myEditor = SoGtkMaterialEditor(myForm)
   
	# Layout the components within the form
	args = []
	GtkSetArg(args[0], XmNtopAttachment,    XmATTACH_FORM)
	GtkSetArg(args[1], XmNbottomAttachment, XmATTACH_FORM)
	GtkSetArg(args[2], XmNleftAttachment,   XmATTACH_FORM) 
	GtkSetArg(args[3], XmNrightAttachment,  XmATTACH_POSITION)
	GtkSetArg(args[4], XmNrightPosition,    40)
	GtkSetValues(myRenderArea.getWidget(), args, 5)
	GtkSetArg(args[2], XmNrightAttachment,  XmATTACH_FORM) 
	GtkSetArg(args[3], XmNleftAttachment,   XmATTACH_POSITION)
	GtkSetArg(args[4], XmNleftPosition,     41) 
	GtkSetValues(myEditor.getWidget(), args, 5)
	
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
   
	# Make the scene graph visible
	myRenderArea.setSceneGraph(root)
   
	# Attach the material editor to the material in the scene
	myEditor.attach(myMaterial)
   
	# Show the main window
	myRenderArea.show()
	myEditor.show()
	SoGtk_show(myForm)    # this calls GtkManageChild
	SoGtk_show(myWindow)  # this calls GtkRealizeWidget
   
	# Loop forever
	SoGtk_mainLoop()

if __name__ == "__main__":
    main()
