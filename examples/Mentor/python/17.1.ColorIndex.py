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
# This is an example from The Inventor Mentor
# chapter 17, example 1.
#
# This examples shows how the user can create a custom
# X visual for doing color index rendering with
# an Inventor Viewer. This shows how to create the right
# visual, as well as load the color map with the wanted
# colors.
#

from pivy import *
import sys

# window attribute list to create a color index visual.
# This will create a double buffered color index window
# with the maximum number of bits and a zbuffer.
attribList = (GLX_DOUBLEBUFFER, 
			  GLX_BUFFER_SIZE, 1, 
			  GLX_DEPTH_SIZE, 1, 
			  None)

# list of colors to load in the color map
colors = ((.2, .2, .2), (.5, 1, .5), (.5, .5, 1))

sceneBuffer = """#Inventor V2.0 ascii

Separator {
   LightModel { model BASE_COLOR }
   ColorIndex { index 1 }
   Coordinate3 { point [ -1 -1 -1, -1 1 -1, 1 1 1, 1 -1 1] }
   FaceSet {}
   ColorIndex { index 2 }
   Coordinate3 { point [ -1 -1 1, -1 1 1, 1 1 -1, 1 -1 -1] }
   FaceSet {}
}"""

def main():
	# Initialize Inventor and Gtk
	myWindow = SoGtk::init(argv[0])
   
	# read the scene graph in
	input = SoInput()
	input.setBuffer(sceneBuffer)
	if not SoDB_readAll(input) or scene == None:
		print "Couldn't read scene"
		sys.exit(1)

	# create the color index visual
	vis = glXChooseVisual(GtkDisplay(myWindow), 
						  XScreenNumberOfScreen(GtkScreen(myWindow)),
						  attribList)
	if not vis:
		print "Couldn't create visual"
		sys.exit(1)
   
	# allocate the viewer, set the scene, the visual and
	# load the color map with the wanted colors.
	#
	# Color 0 will be used for the background (default) while
	# color 1 and 2 are used by the objects.
	#
	myViewer = SoGtkExaminerViewer(myWindow)
	myViewer.setNormalVisual(vis)
	myViewer.setColorMap(0, 3, (SbColor *) colors)
	myViewer.setSceneGraph(scene)
	myViewer.setTitle("Color Index Mode")
   
	# Show the viewer and loop forever...
	myViewer.show()
	GtkRealizeWidget(myWindow)
	SoGtk_mainLoop()

if __name__ == "__main__":
    main()
