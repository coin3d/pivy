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
# chapter 9, example 2.
#
# Using the offscreen renderer to generate a texture map.
# Generate simple scene and grab the image to use as
# a texture map.
#

from pivy import *
import sys

def generateTextureMap(root, texture, textureWidth, textureHeight):
	myViewport = SbViewportRegion(textureWidth, textureHeight)

	# Render the scene
	myRenderer = SoOffscreenRenderer(myViewport)
	myRenderer.setBackgroundColor(SbColor(0.3, 0.3, 0.3))
	if not myRenderer.render(root):
		del myRenderer
		return FALSE

	# Generate the texture
	texture.image.setValue(SbVec2s(textureWidth, textureHeight),
						   SoOffscreenRenderer.RGB, myRenderer.getBuffer())

	del myRenderer
	return TRUE

def main():
	# Initialize Inventor and Gtk
	appWindow = SoGtk_init(sys.argv[0])
	if appWindow == None:
		sys.exit(1)

	# Make a scene from reading in a file
	texRoot = SoSeparator()
	input = SoInput()

	texRoot.ref()
	input.openFile("jumpyMan.iv")
	result = SoDB_readAll(input)

	myCamera = SoPerspectiveCamera()
	rot = SoRotationXYZ()
	rot.axis(SoRotationXYZ.X)
	rot.angle(M_PI_2)
	myCamera.position.setValue(SbVec3f(-0.2, -0.2, 2.0))
	myCamera.scaleHeight(0.4) 
	texRoot.addChild(myCamera)
	texRoot.addChild(SoDirectionalLight())
	texRoot.addChild(rot)
	texRoot.addChild(result)

	# Generate the texture map
	texture = SoTexture2()
	texture.ref()
	if generateTextureMap(texRoot, texture, 64, 64):
		print "Successfully generated texture map"
	else:
		print "Could not generate texture map"
	texRoot.unref()

	# Make a scene with a cube and apply the texture to it
	root = SoSeparator()
	root.ref()
	root.addChild(texture)
	root.addChild(SoCube())

	# Initialize an Examiner Viewer
	viewer = SoGtkExaminerViewer(appWindow)
	viewer.setSceneGraph(root)
	viewer.setTitle("Offscreen Rendered Texture")

	# In Inventor 2.1, if the machine does not have hardware texture
	# mapping, we must override the default drawStyle to display textures.
	viewer.setDrawStyle(SoGtkViewer.STILL, SoGtkViewer.VIEW_AS_IS)

	viewer.show()

	SoGtk_show(appWindow)
	SoGtk_mainLoop()

if __name__ == "__main__":
	main()
