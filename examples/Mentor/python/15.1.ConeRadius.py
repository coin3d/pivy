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
# This is an example from the Inventor Mentor.
# chapter 15, example 1.
#
# Uses an SoTranslate1Dragger to control the bottomRadius field 
# of an SoCone.  The 'translation' field of the dragger is the 
# input to an SoDecomposeVec3f engine. The engine extracts the
# x component from the translation. This extracted value is
# connected to the bottomRadius field of the cone.
#

from pivy import *
import sys

def main():
	# Initialize Inventor and Gtk
	myWindow = SoGtk_init(sys.argv[0])  
	if myWindow == None: sys.exit(1)     

	root = SoSeparator()
	root.ref()

	# Create myDragger with an initial translation of (1,0,0)
	myDragger = SoTranslate1Dragger()
	root.addChild(myDragger)
	myDragger.translation.setValue(1,0,0)

	# Place an SoCone above myDragger
	myTransform = SoTransform()
	myCone = SoCone()
	root.addChild(myTransform)
	root.addChild(myCone)
	myTransform.translation.setValue(0,3,0)

	# SoDecomposeVec3f engine extracts myDragger's x-component
	# The result is connected to myCone's bottomRadius.
	myEngine = SoDecomposeVec3f()
	myEngine.vector.connectFrom(myDragger.translation)
	myCone.bottomRadius.connectFrom(myEngine.x)

	# Display them in a viewer
	myViewer = SoGtkExaminerViewer(myWindow)
	myViewer.setSceneGraph(root)
	myViewer.setTitle("Dragger Edits Cone Radius")
	myViewer.viewAll()
	myViewer.show()

	SoGtk_show(myWindow)
	SoGtk_mainLoop()

if __name__ == "__main__":
    main()
