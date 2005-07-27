/**
 * Copyright (C) 2002-2005, Tamer Fahmy <tamer@tammura.at>
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met:
 *   * Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *   * Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in
 *     the documentation and/or other materials provided with the
 *     distribution.
 *   * Neither the name of the copyright holder nor the names of its
 *     contributors may be used to endorse or promote products derived
 *     from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 **/
%module(package="pivy.gui") sogtk

#include <Inventor/Gtk/devices/SoGtkDevice.h>
#include <Inventor/Gtk/devices/SoGtkKeyboard.h>
#include <Inventor/Gtk/devices/SoGtkMouse.h>
#include <Inventor/Gtk/devices/SoGtkSpaceball.h>
#include <Inventor/Gtk/widgets/SoGtkPopupMenu.h>
#include <Inventor/Gtk/viewers/SoGtkViewer.h>
#include <Inventor/Gtk/viewers/SoGtkConstrainedViewer.h>
#include <Inventor/Gtk/viewers/SoGtkFullViewer.h>
#include <Inventor/Gtk/viewers/SoGtkExaminerViewer.h>
#include <Inventor/Gtk/viewers/SoGtkFlyViewer.h>
#include <Inventor/Gtk/viewers/SoGtkPlaneViewer.h>
#include <Inventor/Gtk/SoGtkGraphEditor.h>
#include <Inventor/Gtk/SoGtkRoster.h>
#include <Inventor/Gtk/SoGtk.h>
#include <Inventor/Gtk/SoGtkBasic.h>
#include <Inventor/Gtk/SoGtkObject.h>
#include <Inventor/Gtk/SoGtkCursor.h>
#include <Inventor/Gtk/SoGtkComponent.h>
#include <Inventor/Gtk/SoGtkGLWidget.h>
#include <Inventor/Gtk/SoGtkRenderArea.h>

#include "coin_header_includes.h"

/* FIXME: there is a major pitfall reg. this solution, namely
 * thread safety! reconsider! 20030626 tamer.
 */
static void *Pivy_PythonInteractiveLoop(void *data) {
  PyRun_InteractiveLoop(stdin, "<stdin>");
  return NULL;
}

%}

/* include the typemaps common to all pivy modules */
%include pivy_common_typemaps.i

/* import the pivy main interface file */
%import coin.i

%include Inventor/Gtk/devices/SoGtkDevice.h
%include Inventor/Gtk/devices/SoGtkKeyboard.h
%include Inventor/Gtk/devices/SoGtkMouse.h
%include Inventor/Gtk/devices/SoGtkSpaceball.h
%include Inventor/Gtk/widgets/SoGtkPopupMenu.h
%include Inventor/Gtk/viewers/SoGtkViewer.h
%include Inventor/Gtk/viewers/SoGtkConstrainedViewer.h
%include Inventor/Gtk/viewers/SoGtkFullViewer.h
%include Inventor/Gtk/viewers/SoGtkExaminerViewer.h
%include Inventor/Gtk/viewers/SoGtkFlyViewer.h
%include Inventor/Gtk/viewers/SoGtkPlaneViewer.h
%include Inventor/Gtk/SoGtkGraphEditor.h
%include Inventor/Gtk/SoGtkRoster.h
%include Inventor/Gtk/SoGtk.h
%include Inventor/Gtk/SoGtkBasic.h
%include Inventor/Gtk/SoGtkObject.h
%include Inventor/Gtk/SoGtkCursor.h
%include Inventor/Gtk/SoGtkComponent.h
%include Inventor/Gtk/SoGtkGLWidget.h
%include Inventor/Gtk/SoGtkRenderArea.h
