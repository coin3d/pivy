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
# chapter 9, example 1.
#
# Printing example.
# Read in an Inventor file and display it in ExaminerViewer.  Press
# the "p" key and the scene renders into a PostScript
# file for printing.
#

from pivy import *
import sys

class callbackData:
	vwr = None
	filename = None
	scene = None

##############################################################
## CODE FOR The Inventor Mentor STARTS HERE

def printToPostScript(root, file, viewer, printerDPI):
    # Calculate size of the images in inches which is equal to
    # the size of the viewport in pixels divided by the number
    # of pixels per inch of the screen device.  This size in
    # inches will be the size of the Postscript image that will
    # be generated.
	vp  = viewer.getViewportRegion()
	imagePixSize = vp.getViewportSizePixels()
	imageInches = SbVec2f()

	pixPerInch = SoOffscreenRenderer_getScreenPixelsPerInch()
	imageInches.setValue(imagePixSize[0] / pixPerInch,
                         imagePixSize[1] / pixPerInch)

    # The resolution to render the scene for the printer
    # is equal to the size of the image in inches times
    # the printer DPI
	postScriptRes = SbVec2s()
	postScriptRes.setValue(imageInches[0]*printerDPI,
                           imageInches[1]*printerDPI)

    # Create a viewport to render the scene into.
	myViewport = SbViewportRegion()
	myViewport.setWindowSize(postScriptRes)
	myViewport.setPixelsPerInch(printerDPI)
    
    # Render the scene
	myRenderer = SoOffscreenRenderer(myViewport)

	if not myRenderer.render(root):
		return FALSE

    # Generate PostScript and write it to the given file
	myRenderer.writeToPostScript(file)

	return TRUE

# CODE FOR The Inventor Mentor ENDS HERE
##############################################################

def processKeyEvents(data, cb):
	if SoKeyboardEvent_isKeyPressEvent(cb.getEvent(), SoKeyboardEvent.P):
		myFile = open(data.filename, "w")

		if myFile == None:
			sys.stderr.write("Cannot open output file\n")
			sys.exit(1)

		sys.stdout.write("Printing scene... ")
		sys.stdout.flush()
		if not printToPostScript(data.scene, myFile, data.vwr, 75):
			sys.stderr.write("Cannot print image\n")
			myFile.close()
			sys.exit(1)

		myFile.close()
		sys.stdout.write("  ...done printing.\n")
		sys.stdout.flush()
		cb.setHandled()

def main():
    # Initialize Inventor and Gtk
    appWindow = SoGtk_init(sys.argv[0])
    if appWindow == None:
	sys.exit(1)
        
    # Verify the command line arguments
    if len(sys.argv) != 3:
        sys.stdout.write("Usage: %s infile.iv outfile.ps\n" % sys.argv[0])
        sys.exit(1) 
  
    print "To print the scene: press the 'p' key while in picking mode"

    # Make a scene containing an event callback node
    root    = SoSeparator()
    eventCB = SoEventCallback()
    root.ref()
    root.addChild(eventCB)

    # Read the geometry from a file and add to the scene
    myInput = SoInput()
    if not myInput.openFile(sys.argv[1]):
        sys.exit(1)
    geomObject = SoDB_readAll(myInput)
    if geomObject == None:
        sys.exit(1)
    root.addChild(geomObject)

    viewer = SoGtkExaminerViewer(appWindow, "None", TRUE, SoGtkExaminerViewer.BUILD_ALL, SoGtkExaminerViewer.EDITOR)
    viewer.setSceneGraph(root)
    viewer.setTitle("Print to PostScript")
    
    # Setup the event callback data and routine for performing the print
    data = callbackData()
    data.vwr = viewer
    data.filename = sys.argv[2]
    data.scene = viewer.getSceneGraph()
    eventCB.addPythonEventCallback(SoKeyboardEvent_getClassTypeId(), processKeyEvents, data)
    viewer.show()

    SoGtk_show(appWindow)
    SoGtk_mainLoop()

if __name__ == "__main__":
    main()
