#!/usr/bin/env python

##
# Copyright (C) 1998-2004 by Systems in Motion. All rights reserved.
#
# Python translation: Tamer Fahmy <tamer@tammura.at>, 2004 Vienna, Austria

from shapescale import *
from sogui import *
from pivy import *

from random import random
import sys

def construct_new_marker(v):
    markerroot = SoSeparator()

    t = SoTranslation()
    t.translation.setValue(v)
    markerroot.addChild(t)
  
    kit = ShapeScale()
    kit.active(TRUE)
    kit.projectedSize(5.0)
  
    # create the marker
    markersep = SoSeparator()
  
    mat = SoBaseColor()
    mat.rgb.setValue(random(), random(), random())
    markersep.addChild(mat)
  
    # marker shape should be unit size, with center in (0.0f, 0.0f, 0.0f)
    cube = SoCube()
    cube.width(1.0)
    cube.height(1.0)
    cube.depth(1.0)
  
    markersep.addChild(cube)
    kit.setPart("shape", markersep)
    markerroot.addChild(kit)
  
    return markerroot


def event_cb(viewer, n):
    mbe = cast(n.getEvent(), "SoMouseButtonEvent")

    if mbe.getButton() == SoMouseButtonEvent.BUTTON1 and \
           mbe.getState() == SoButtonEvent.DOWN:

        rp = SoRayPickAction(viewer.getViewportRegion())
        rp.setPoint(mbe.getPosition())
        rp.apply(viewer.getSceneManager().getSceneGraph())

        point = rp.getPickedPoint()
        if point == None:
            print >>sys.stderr, "\n** miss! **\n"
            return

        n.setHandled()

        p = rp.getCurPath()

        for i in range(p.getLength()):
            n = p.getNodeFromTail(i)
            if n.isOfType(SoGroup.getClassTypeId()):
                n.addChild(construct_new_marker(point.getPoint()))
                break
        

def show_instructions():
    print """
This example program demonstrates the use of the ShapeScale nodekit.
Quick instructions:


  * place the marker by clicking on a shape with the left mouse button
  * hit ESC to toggle back and forth to view mode
  * zoom back and forth to see how the markers stay the same size

"""

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print >>sys.stderr, "\nSpecify an Inventor file as argument.\n"
        sys.exit(-1)

    window = SoGui.init(sys.argv[0])
    ShapeScale.initClass() # init our extension nodekit

    ex1 = SoGuiExaminerViewer(window)

    input = SoInput()
    if not input.openFile(sys.argv[1]):
        print >>sys.stderr, "Unable to open file: %s\n" % sys.argv[1]
        sys.exit(-1)

    root = SoDB.readAll(input) 

    if root == None:
        print >>sys.stderr, "Unable to read file: %s\n" % sys.argv[1]
        sys.exit(-1)

    show_instructions()

    newroot = SoSeparator()
    newroot.ref()

    newroot.addChild(root)

    # create event callback and marker nodes
    sep = SoSeparator()
    newroot.addChild(sep)

    ecb = SoEventCallback()
    ecb.addEventCallback(SoMouseButtonEvent.getClassTypeId(), event_cb, ex1)
    sep.addChild(ecb)

    ex1.setSceneGraph(newroot)
    ex1.setTransparencyType(SoGLRenderAction.SORTED_OBJECT_BLEND)
    ex1.setViewing(FALSE)
  
    ex1.show()
    SoGui.show(window)

    SoGui.mainLoop()
    del ex1

    newroot.unref()
    sys.exit(0)
