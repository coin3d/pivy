#!/usr/bin/env python

###
# Copyright (C) 2002-2004, Tamer Fahmy <tamer@tammura.at>
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
# Pivy SoGui proxy class for the different SoGui bindings
#

import sys

# global variables that hold the references to the possible classes in the
# corresponding SoGui binding
SoGuiCursor      = None
SoGuiComponent   = None
SoGuiGLWidget    = None
SoGuiRenderArea  = None
SoGuiViewer      = None
SoGuiFullViewer  = None
SoGuiFlyViewer   = None
SoGuiPlaneViewer = None
SoGuiDevice      = None
SoGuiKeyboard    = None
SoGuiMouse       = None
SoGuiSpaceball   = None
SoGuiExaminerViewer = None
SoGuiConstrainedViewer = None

class SoGui_Proxy:
    "a proxy object which routes the calls through their counterparts"
    
    def __init__(self, obj, debug):
        global SoGuiCursor, SoGuiComponent, SoGuiGLWidget, SoGuiRenderArea
        global SoGuiViewer, SoGuiFullViewer, SoGuiFlyViewer, SoGuiPlaneViewer
        global SoGuiDevice, SoGuiKeyboard, SoGuiMouse, SoGuiSpaceball
        global SoGuiExaminerViewer, SoGuiConstrainedViewer

        self.debug = debug
        
        # if no binding has been specified check for availability of a known
        # one in a defined order SoQt -> SoXt -> SoGtk
        if not obj:
            try:
                soqt = __import__('soqt')
                obj = soqt.SoQt
                SoGuiCursor      = soqt.SoQtCursor
                SoGuiComponent   = soqt.SoQtComponent
                SoGuiGLWidget    = soqt.SoQtGLWidget
                SoGuiRenderArea  = soqt.SoQtRenderArea
                SoGuiViewer      = soqt.SoQtViewer
                SoGuiFullViewer  = soqt.SoQtFullViewer
                SoGuiFlyViewer   = soqt.SoQtFlyViewer
                SoGuiPlaneViewer = soqt.SoQtPlaneViewer
                SoGuiDevice      = soqt.SoQtDevice
                SoGuiKeyboard    = soqt.SoQtKeyboard
                SoGuiMouse       = soqt.SoQtMouse
                SoGuiSpaceball   = soqt.SoQtSpaceball
                SoGuiExaminerViewer = soqt.SoQtExaminerViewer                
                SoGuiConstrainedViewer = soqt.SoQtConstrainedViewer
            except ImportError:
                try:
                    soxt = __import__('soxt')
                    obj = soxt.Soxt
                    SoGuiCursor      = soxt.SoXtCursor
                    SoGuiComponent   = soxt.SoXtComponent
                    SoGuiGLWidget    = soxt.SoXtGLWidget
                    SoGuiRenderArea  = soxt.SoXtRenderArea
                    SoGuiViewer      = soxt.SoXtViewer
                    SoGuiFullViewer  = soxt.SoXtFullViewer
                    SoGuiFlyViewer   = soxt.SoXtFlyViewer
                    SoGuiPlaneViewer = soxt.SoXtPlaneViewer
                    SoGuiDevice      = soxt.SoXtDevice
                    SoGuiKeyboard    = soxt.SoXtKeyboard
                    SoGuiMouse       = soxt.SoXtMouse
                    SoGuiSpaceball   = soxt.SoXtSpaceball
                    SoGuiExaminerViewer = soxt.SoXtExaminerViewer                
                    SoGuiConstrainedViewer = soxt.SoXtConstrainedViewer
                except ImportError:
                    try:
                        sogtk = __import__('sogtk')
                        obj = sogtk.SoGtk
                        SoGuiCursor      = sogtk.SoGtkCursor
                        SoGuiComponent   = sogtk.SoGtkComponent
                        SoGuiGLWidget    = sogtk.SoGtkGLWidget
                        SoGuiRenderArea  = sogtk.SoGtkRenderArea
                        SoGuiViewer      = sogtk.SoGtkViewer
                        SoGuiFullViewer  = sogtk.SoGtkFullViewer
                        SoGuiFlyViewer   = sogtk.SoGtkFlyViewer
                        SoGuiPlaneViewer = sogtk.SoGtkPlaneViewer
                        SoGuiDevice      = sogtk.SoGtkDevice
                        SoGuiKeyboard    = sogtk.SoGtkKeyboard
                        SoGuiMouse       = sogtk.SoGtkMouse
                        SoGuiSpaceball   = sogtk.SoGtkSpaceball
                        SoGuiExaminerViewer = sogtk.SoGtkExaminerViewer                
                        SoGuiConstrainedViewer = sogtk.SoGtkConstrainedViewer
                    except ImportError:
                        print "SoGui proxy error: None of the known Gui bindings were found! Please specify one!"
                        sys.exit(1)

        # check if object is a user provided string possibly a new unknown SoGui binding.
        # try to bind it.
        elif type(obj) == type(""):
            try:
                sogui = __import__(obj.lower())
                gui = obj
                obj = eval("sogui." + obj)
                SoGuiCursor      = eval("sogui." + gui + "Cursor")
                SoGuiComponent   = eval("sogui." + gui + "Component")
                SoGuiGLWidget    = eval("sogui." + gui + "GLWidget")
                SoGuiRenderArea  = eval("sogui." + gui + "RenderArea")
                SoGuiViewer      = eval("sogui." + gui + "Viewer")
                SoGuiFullViewer  = eval("sogui." + gui + "FullViewer")
                SoGuiFlyViewer   = eval("sogui." + gui + "FlyViewer")
                SoGuiPlaneViewer = eval("sogui." + gui + "PlaneViewer")
                SoGuiDevice      = eval("sogui." + gui + "Device")
                SoGuiKeyboard    = eval("sogui." + gui + "Keyboard")
                SoGuiMouse       = eval("sogui." + gui + "Mouse")
                SoGuiSpaceball   = eval("sogui." + gui + "Spaceball")
                SoGuiExaminerViewer = eval("sogui." + gui + "ExaminerViewer")
                SoGuiConstrainedViewer = eval("sogui." + gui + "ConstrainedViewer")
            except ImportError:
                print "SoGui proxy error: The specified Gui binding could not be bound!"
                sys.exit(1)
                
        self.__obj__ = obj

    def __getattr__(self, name):
        if self.debug:
            print "getattr called for", name
        return getattr(self.__obj__, name)

    def __repr__(self):
        return "SoGui proxy for " + `self.__obj__`

    __str__ = __repr__


# instantiate the proxy
obj = None; debug = 0

# look for user overrides in the main dictionary of the interpreter
if sys.modules.has_key('__main__'):
    try:
        debug = sys.modules['__main__'].SOGUI_DEBUG
    except AttributeError:
        pass
    
    try:
        obj = sys.modules['__main__'].SOGUI_BINDING
    except AttributeError:
        pass

SoGui = SoGui_Proxy(obj, debug)
