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
# This is an example from The Inventor Mentor,
# chapter 9, example 5.
#
# Using a callback for generated primitives.
# A simple scene with a sphere is created.
# A callback is used to write out the triangles that
# form the sphere in the scene.
#

from pivy import *
import sys

##############################################################
# CODE FOR The Inventor Mentor STARTS HERE

def printVertex(vertex):
	point = vertex.getPoint()
	print "\tCoords     = (%g, %g, %g)" % (point[0], point[1], point[2])

	normal = vertex.getNormal()
	print "\tNormal     = (%g, %g, %g)" % (normal[0], normal[1], normal[2])

def printHeaderCallback(void, callbackAction, node):
	print "\n Sphere ",
	# Print the node name (if it exists) and address
	if not not node.getName():
		print 'named "%s" ' % node.getName().getString(),
	print "at address %r\n" % node.this

	return SoCallbackAction.CONTINUE

def printTriangleCallback(void, callbackAction,
						  vertex1, vertex2, vertex3):
	print "Triangle:"
	printVertex(vertex1)
	printVertex(vertex2)
	printVertex(vertex3)

def printSpheres(root):
	myAction = SoCallbackAction()
	
	myAction.addPythonPreCallback(SoSphere_getClassTypeId(),
								  printHeaderCallback, None)
	myAction.addPythonTriangleCallback(SoSphere_getClassTypeId(), 
									   printTriangleCallback, None)

	myAction.apply(root)
	
# CODE FOR The Inventor Mentor ENDS HERE
##############################################################

def main():
	# Initialize Inventor
	SoDB_init()

	# Make a scene containing a red sphere
	root = SoSeparator()
	myCamera = SoPerspectiveCamera()
	myMaterial = SoMaterial()
	root.ref()
	root.addChild(myCamera)
	root.addChild(SoDirectionalLight())
	myMaterial.diffuseColor.setValue(1.0, 0.0, 0.0)   # Red
	root.addChild(myMaterial)
	root.addChild(SoSphere())
	root.ref()

	# Write out the triangles that form the sphere in the scene
	printSpheres(root)

	root.unref()
	return 0

if __name__ == "__main__":
	sys.exit(main())

