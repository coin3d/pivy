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
# This is an example from the Inventor Mentor
# chapter 13, example 4.
#
# Time counter engine.
# The output from an time counter engine is used to control
# horizontal and vertical motion of a figure object.
# The resulting effect is that the figure jumps across
# the screen.
#

from pivy import *
import sys

def main():
	# Initialize Inventor and Gtk
	myWindow = SoGtk_init(sys.argv[0])  
	if myWindow == None: sys.exit(1)     

	root = SoSeparator()
	root.ref()
	
	# Add a camera and light
	myCamera = SoPerspectiveCamera()
	myCamera.position.setValue(-8.0, -7.0, 20.0)
	myCamera.heightAngle(M_PI/2.5)
	myCamera.nearDistance(15.0)
	myCamera.farDistance(25.0)
	root.addChild(myCamera)
	root.addChild(SoDirectionalLight())

##############################################################
# CODE FOR The Inventor Mentor STARTS HERE

	# Set up transformations
	jumpTranslation = SoTranslation()
	root.addChild(jumpTranslation)
	initialTransform = SoTransform()
	initialTransform.translation.setValue(-20., 0., 0.)
	initialTransform.scaleFactor.setValue(40., 40., 40.)
	initialTransform.rotation.setValue(SbVec3f(1,0,0), M_PI/2.)
	root.addChild(initialTransform)

	# Read the man object from a file and add to the scene
	myInput = SoInput()
	if not myInput.openFile("jumpyMan.iv"):
		sys.exit(1)
	manObject = SoDB_readAll(myInput)
	if manObject == None:
		sys.exit(1)
	root.addChild(manObject)

	# Create two counters, and connect to X and Y translations.
	# The Y counter is small and high frequency.
	# The X counter is large and low frequency.
	# This results in small jumps across the screen, 
	# left to right, again and again and again and ....
	jumpHeightCounter = SoTimeCounter()
	jumpWidthCounter = SoTimeCounter()
	jump = SoComposeVec3f()

	jumpHeightCounter.max(4)
	jumpHeightCounter.frequency(1.5)
	jumpWidthCounter.max(40)
	jumpWidthCounter.frequency(0.15)

	jump.x.connectFrom(jumpWidthCounter.output)
	jump.y.connectFrom(jumpHeightCounter.output)
	jumpTranslation.translation.connectFrom(jump.vector)

# CODE FOR The Inventor Mentor ENDS HERE
##############################################################

	myRenderArea = SoGtkRenderArea(myWindow)
	myRegion = SbViewportRegion(myRenderArea.getSize()) 
	myRenderArea.setSceneGraph(root)
	myRenderArea.setTitle("Jumping Man")
	myRenderArea.show()

	SoGtk_show(myWindow)
	SoGtk_mainLoop()

if __name__ == "__main__":
    main()
