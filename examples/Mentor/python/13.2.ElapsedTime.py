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
# chapter 13, example 3.
#
# Elapsed time engine.
# The output from an elapsed time engine is used to control
# the translation of the object.  The resulting effect is
# that the figure slides across the scene.
#

from pivy import *
import sys

def main():
	# Initialize Inventor and Qt
	myWindow = SoQt_init(sys.argv[0])  
	if myWindow == None: sys.exit(1)     

	root = SoSeparator()
	root.ref()

	# Add a camera and light
	myCamera = SoPerspectiveCamera()
	myCamera.position.setValue(-2.0, -2.0, 5.0)
	myCamera.heightAngle(M_PI/2.5)
	myCamera.nearDistance(2.0)
	myCamera.farDistance(7.0)
	root.addChild(myCamera)
	root.addChild(SoDirectionalLight())

	# Set up transformations
	slideTranslation = SoTranslation()
	root.addChild(slideTranslation)
	initialTransform = SoTransform()
	initialTransform.translation.setValue(-5., 0., 0.)
	initialTransform.scaleFactor.setValue(10., 10., 10.)
	initialTransform.rotation.setValue(SbVec3f(1,0,0), M_PI/2.)
	root.addChild(initialTransform)

	# Read the figure object from a file and add to the scene
	myInput = SoInput()
	if not myInput.openFile("jumpyMan.iv"):
		sys.exit (1)
	figureObject = SoDB_readAll(myInput)
	if figureObject == None:
		sys.exit(1)
	root.addChild(figureObject)

	# Make the X translation value change over time.
	myCounter = SoElapsedTime()
	slideDistance = SoComposeVec3f()
	slideDistance.x.connectFrom(myCounter.timeOut)
	slideTranslation.translation.connectFrom(slideDistance.vector)

	myRenderArea = SoQtRenderArea(myWindow)
	myRegion = SbViewportRegion(myRenderArea.getSize()) 
	myRenderArea.setSceneGraph(root)
	myRenderArea.setTitle("Sliding Man")
	myRenderArea.show()

	SoQt_show(myWindow)
	SoQt_mainLoop()

if __name__ == "__main__":
    main()
