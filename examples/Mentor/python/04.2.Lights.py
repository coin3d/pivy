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
# chapter 4, example 2.
#
# Lights example.  
# Read in an object from a file.
# Use the ExaminerViewer to view it with two light sources.
# The red directional light doesn't move; the green point 
# light is moved back and forth using a shuttle node.
#

from pivy import *
import sys

def main():
	# Initialize Inventor and Gtk
	myWindow = SoGtk_init(sys.argv[0])
	if myWindow == None: sys.exit(1)

	root = SoSeparator()
	root.ref()

	# Add a directional light
	myDirLight = SoDirectionalLight()
	myDirLight.direction.setValue(0, -1, -1)
	myDirLight.color.setValue(1, 0, 0)
	root.addChild(myDirLight)

	# Put the shuttle and the light below a transform separator.
	# A transform separator pushes and pops the transformation 
	# just like a separator node, but other aspects of the state 
	# are not pushed and popped. So the shuttle's translation 
	# will affect only the light. But the light will shine on 
	# the rest of the scene.
	myTransformSeparator = SoTransformSeparator()
	root.addChild(myTransformSeparator)

	# A shuttle node translates back and forth between the two
	# fields translation0 and translation1.  
	# This moves the light.
	myShuttle = SoShuttle()
	myTransformSeparator.addChild(myShuttle)
	myShuttle.translation0.setValue(-2, -1, 3)
	myShuttle.translation1.setValue( 1,  2, -3)

	# Add the point light below the transformSeparator
	myPointLight = SoPointLight()
	myTransformSeparator.addChild(myPointLight)
	myPointLight.color.setValue(0, 1, 0)

	root.addChild(SoCone())

	myViewer = SoGtkExaminerViewer(myWindow)
	myViewer.setSceneGraph(root)
	myViewer.setTitle("Lights")
	myViewer.setHeadlight(FALSE)
	myViewer.show()

	SoGtk_show(myWindow)
	SoGtk_mainLoop()

if __name__ == "__main__":
	main()

