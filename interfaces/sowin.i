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
%module sowin

%{
#if defined(_WIN32) || defined(__WIN32__)
#include <windows.h>
#undef max
#undef ERROR
#undef DELETE
#undef ANY
#endif

#include <Inventor/Win/devices/SoWinDevice.h>
#include <Inventor/Win/devices/SoWinKeyboard.h>
#include <Inventor/Win/devices/SoWinMouse.h>
#include <Inventor/Win/devices/SoWinSpaceball.h>
#include <Inventor/Win/viewers/SoWinViewer.h>
#include <Inventor/Win/viewers/SoWinFullViewer.h>
#include <Inventor/Win/viewers/SoWinExaminerViewer.h>
#include <Inventor/Win/viewers/SoWinPlaneViewer.h>
#include <Inventor/Win/viewers/SoWinConstrainedViewer.h>
#include <Inventor/Win/viewers/SoWinFlyViewer.h>
#include <Inventor/Win/widgets/SoWinPopupMenu.h>
#include <Inventor/Win/SoWin.h>
#include <Inventor/Win/SoWinBasic.h>
#include <Inventor/Win/SoWinObject.h>
#include <Inventor/Win/SoWinCursor.h>
#include <Inventor/Win/SoWinComponent.h>
#include <Inventor/Win/SoWinGLWidget.h>
#include <Inventor/Win/SoWinRenderArea.h>

#include <Inventor/nodes/SoNode.h>
#include <Inventor/fields/SoField.h>

#include <Inventor/SbDPMatrix.h>
#include <Inventor/SbDPRotation.h>
#include <Inventor/SbVec2d.h>
#include <Inventor/C/threads/thread.h>

/* make CustomCursor in SoWinCursor known to SWIG */
typedef SoWinCursor::CustomCursor CustomCursor;

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

%include Inventor/Win/devices/SoWinDevice.h
%include Inventor/Win/devices/SoWinKeyboard.h
%include Inventor/Win/devices/SoWinMouse.h
%include Inventor/Win/devices/SoWinSpaceball.h
%include Inventor/Win/viewers/SoWinViewer.h
%include Inventor/Win/viewers/SoWinFullViewer.h
%include Inventor/Win/viewers/SoWinExaminerViewer.h
%include Inventor/Win/viewers/SoWinPlaneViewer.h
%include Inventor/Win/viewers/SoWinConstrainedViewer.h
%include Inventor/Win/viewers/SoWinFlyViewer.h
%include Inventor/Win/widgets/SoWinPopupMenu.h
%include Inventor/Win/SoWin.h
%include Inventor/Win/SoWinBasic.h
%include Inventor/Win/SoWinObject.h
%include Inventor/Win/SoWinCursor.h
%include Inventor/Win/SoWinComponent.h
%include Inventor/Win/SoWinGLWidget.h
%include Inventor/Win/SoWinRenderArea.h
