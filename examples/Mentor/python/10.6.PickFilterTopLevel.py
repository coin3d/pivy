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
# chapter 10, example 6.
#
# This example demonstrates the use of the pick filter
# callback to implement a top level selection policy.
# That is, always select the top most group beneath the
# selection node,  rather than selecting the actual
# shape that was picked.
#

from sogui import *
from pivy import *
import sys

# Pick the topmost node beneath the selection node
def pickFilterCB(void, pick):
    # See which child of selection got picked
    p = pick.getPath()
    
    for i in range(p.getLength() - 1):
        n = p.getNode(i)
        if n.isOfType(SoSelection_getClassTypeId()):
            break

    # Copy 2 nodes from the path:
    # selection and the picked child
    return p.copy(i, 2)

def main():
    # Initialization
    mainWindow = SoGui.init(sys.argv[0])
    
    # Open the data file
    input = SoInput()
    datafile = "parkbench.iv"
    if not input.openFile(datafile):
        print >> sys.stderr, "Cannot open %s for reading." % (datafile)
        sys.exit(1)

    # Read the input file
    sep = SoSeparator()
    sep.addChild(SoDB_readAll(input))
   
    # Create two selection roots - one will use the pick filter.
    topLevelSel = SoSelection()
    topLevelSel.addChild(sep)
    topLevelSel.setPickFilterCallback(pickFilterCB)

    defaultSel = SoSelection()
    defaultSel.addChild(sep)

    # Create two viewers, one to show the pick filter for top level
    # selection, the other to show default selection.
    viewer1 = SoGuiExaminerViewer(mainWindow)
    viewer1.setSceneGraph(topLevelSel)
    boxhra1 = SoBoxHighlightRenderAction()
    viewer1.setGLRenderAction(boxhra1)
    viewer1.redrawOnSelectionChange(topLevelSel)
    viewer1.setTitle("Top Level Selection")

    viewer2 = SoGuiExaminerViewer()
    viewer2.setSceneGraph(defaultSel)
    boxhra2 = SoBoxHighlightRenderAction()
    viewer2.setGLRenderAction(boxhra2)
    viewer2.redrawOnSelectionChange(defaultSel)
    viewer2.setTitle("Default Selection")

    viewer1.show()
    viewer2.show()
   
    SoGui.show(mainWindow)
    SoGui.mainLoop()

if __name__ == "__main__":
    main()
