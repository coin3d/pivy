/**
 * Copyright (C) 2002-2004, Tamer Fahmy <tamer@tammura.at>
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
%module soqt

%{
#include <Inventor/Qt/devices/SoQtDevice.h>
#include <Inventor/Qt/devices/SoQtKeyboard.h>
#include <Inventor/Qt/devices/SoQtMouse.h>
#include <Inventor/Qt/devices/SoQtSpaceball.h>
#include <Inventor/Qt/editors/SoQtColorEditor.h>
#include <Inventor/Qt/nodes/SoGuiColorEditor.h>
#include <Inventor/Qt/viewers/SoQtViewer.h>
#include <Inventor/Qt/viewers/SoQtFullViewer.h>
#include <Inventor/Qt/viewers/SoQtExaminerViewer.h>
#include <Inventor/Qt/viewers/SoQtPlaneViewer.h>
#include <Inventor/Qt/viewers/SoQtConstrainedViewer.h>
#include <Inventor/Qt/viewers/SoQtFlyViewer.h>
#include <Inventor/Qt/widgets/SoQtPopupMenu.h>
#include <Inventor/Qt/SoQtColorEditor.h>
#include <Inventor/Qt/SoQt.h>
#include <Inventor/Qt/SoQtBasic.h>
#include <Inventor/Qt/SoQtObject.h>
#include <Inventor/Qt/SoQtCursor.h>
#include <Inventor/Qt/SoQtComponent.h>
#include <Inventor/Qt/SoQtGLWidget.h>
#include <Inventor/Qt/SoQtRenderArea.h>

#include <Inventor/SbDPMatrix.h>
#include <Inventor/SbDPRotation.h>
#include <Inventor/SbVec2d.h>
#include <Inventor/C/threads/thread.h>


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

%include Inventor/Qt/devices/SoQtDevice.h
%include Inventor/Qt/devices/SoQtKeyboard.h
%include Inventor/Qt/devices/SoQtMouse.h
%include Inventor/Qt/devices/SoQtSpaceball.h
%include Inventor/Qt/editors/SoQtColorEditor.h
%include Inventor/Qt/nodes/SoGuiColorEditor.h
%include Inventor/Qt/viewers/SoQtViewer.h
%include Inventor/Qt/viewers/SoQtFullViewer.h
%include Inventor/Qt/viewers/SoQtExaminerViewer.h
%include Inventor/Qt/viewers/SoQtPlaneViewer.h
%include Inventor/Qt/viewers/SoQtConstrainedViewer.h
%include Inventor/Qt/viewers/SoQtFlyViewer.h
%include Inventor/Qt/widgets/SoQtPopupMenu.h
%include Inventor/Qt/SoQtColorEditor.h
%include Inventor/Qt/SoQt.h
%include Inventor/Qt/SoQtBasic.h
%include Inventor/Qt/SoQtObject.h
%include Inventor/Qt/SoQtCursor.h
%include Inventor/Qt/SoQtComponent.h
%include Inventor/Qt/SoQtGLWidget.h
%include Inventor/Qt/SoQtRenderArea.h
