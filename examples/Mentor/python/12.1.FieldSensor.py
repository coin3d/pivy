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
# chapter 12, example 1.
#
# Sense changes to a viewer's camera's position.
#

from pivy import *
import sys

# Callback that reports whenever the viewer's position changes.
def cameraChangedCB(data, sensor):
	viewerCamera = cast(data, "SoCamera")

	cameraPosition = viewerCamera.position.getValue()
	print "Camera position: (%g,%g,%g)" % (cameraPosition[0],
										   cameraPosition[1],
										   cameraPosition[2])
	
def main():
	if len(sys.argv) != 2:
		print >> sys.stderr, "Usage: %s filename.iv" % (sys.argv[0])
		sys.exit(1)

	myWindow = SoGtk_init(sys.argv[0])
	if myWindow == None: sys.exit(1)

	inputFile = SoInput()
	if inputFile.openFile(sys.argv[1]) == 0:
		print >> sys.stderr, "Could not open file %s" % (sys.argv[1])
		sys.exit(1)
   
	root = SoDB_readAll(inputFile)
	root.ref()

	myViewer = SoGtkExaminerViewer(myWindow)
	myViewer.setSceneGraph(root)
	myViewer.setTitle("Camera Sensor")
	myViewer.show()

	# Get the camera from the viewer, and attach a 
	# field sensor to its position field:
	camera = myViewer.getCamera()
	mySensor = SoFieldSensor(cameraChangedCB, camera)
	mySensor.attach(camera.position)
	
	SoGtk_show(myWindow)
	SoGtk_mainLoop()

if __name__ == "__main__":
    main()
