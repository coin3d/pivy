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
# chapter 2, example 1.
#
# Hello Cone example program; draws a red cone in a window.
#

from pivy import *
import sys

def main():
	# Initialize Inventor. This returns a main window to use.
	# If unsuccessful, exit.

	myWindow = SoGtk_init(sys.argv[0])
	if myWindow == None: sys.exit(1)

	# Make a scene containing a red cone
	root = SoSeparator()
	myCamera = SoPerspectiveCamera()
	myMaterial = SoMaterial()
	root.ref()
	root.addChild(myCamera)
	root.addChild(SoDirectionalLight())
	myMaterial.diffuseColor.setValue(1.0, 0.0, 0.0)   # Red
	root.addChild(myMaterial)
	root.addChild(SoCone())

	# Create a renderArea in which to see our scene graph.
	# The render area will appear within the main window.
	myRenderArea = SoGtkRenderArea(myWindow)

	# Make myCamera see everything.
	myCamera.viewAll(root, myRenderArea.getViewportRegion());

	# Put our scene in myRenderArea, change the title
	myRenderArea.setSceneGraph(root)
	myRenderArea.setTitle("Hello Cone")
	myRenderArea.show()

	SoGtk_show(myWindow)  # Display main window
	SoGtk_mainLoop()    # Main Inventor event loop

if __name__ == "__main__":
	main()
