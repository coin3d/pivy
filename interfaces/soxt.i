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
%module soxt

%{

#include <Inventor/Xt/devices/SoXtLinuxJoystick.h>
#include <Inventor/Xt/devices/SoXtDevice.h>
#include <Inventor/Xt/devices/SoXtKeyboard.h>
#include <Inventor/Xt/devices/SoXtMouse.h>
#include <Inventor/Xt/devices/SoXtSpaceball.h>
#include <Inventor/Xt/editors/SoXtColorEditor.h>
#include <Inventor/Xt/editors/SoXtMaterialEditor.h>
#include <Inventor/Xt/nodes/SoGuiColorEditor.h>
#include <Inventor/Xt/nodes/SoGuiMaterialEditor.h>
#include <Inventor/Xt/viewers/SoXtViewer.h>
#include <Inventor/Xt/viewers/SoXtConstrainedViewer.h>
#include <Inventor/Xt/viewers/SoXtFullViewer.h>
#include <Inventor/Xt/viewers/SoXtExaminerViewer.h>
#include <Inventor/Xt/viewers/SoXtFlyViewer.h>
#include <Inventor/Xt/viewers/SoXtPlaneViewer.h>
#include <Inventor/Xt/widgets/SoXtPopupMenu.h>
#include <Inventor/Xt/SoXtResource.h>
#include <Inventor/Xt/SoXt.h>
#include <Inventor/Xt/SoXtBasic.h>
#include <Inventor/Xt/SoXtObject.h>
#include <Inventor/Xt/SoXtCursor.h>
#include <Inventor/Xt/SoXtComponent.h>
#include <Inventor/Xt/SoXtGLWidget.h>
#include <Inventor/Xt/SoXtRenderArea.h>
#include <Inventor/Xt/SoXtColorEditor.h>
#include <Inventor/Xt/SoXtMaterialEditor.h>

#include <Inventor/SbDPMatrix.h>
#include <Inventor/SbDPRotation.h>
#include <Inventor/SbVec2d.h>
#include <Inventor/C/threads/thread.h>

/* make CustomCursor in SoXtCursor known to SWIG */
typedef SoXtCursor::CustomCursor CustomCursor;

/* FIXME: there is a major pitfall reg. this solution, namely
 * thread safety! reconsider! 20030626 tamer.
 */
static void *
Pivy_PythonInteractiveLoop(void *data) {
  PyRun_InteractiveLoop(stdin, "<stdin>");
  return NULL;
}
%}

/* include the typemaps common to all pivy modules */
%include pivy_common_typemaps.i

%include Inventor/Xt/devices/SoXtLinuxJoystick.h
%include Inventor/Xt/devices/SoXtDevice.h
%include Inventor/Xt/devices/SoXtKeyboard.h
%include Inventor/Xt/devices/SoXtMouse.h
%include Inventor/Xt/devices/SoXtSpaceball.h
%include Inventor/Xt/editors/SoXtColorEditor.h
%include Inventor/Xt/editors/SoXtMaterialEditor.h
%include Inventor/Xt/nodes/SoGuiColorEditor.h
%include Inventor/Xt/nodes/SoGuiMaterialEditor.h
%include Inventor/Xt/viewers/SoXtViewer.h
%include Inventor/Xt/viewers/SoXtConstrainedViewer.h
%include Inventor/Xt/viewers/SoXtFullViewer.h
%include Inventor/Xt/viewers/SoXtExaminerViewer.h
%include Inventor/Xt/viewers/SoXtFlyViewer.h
%include Inventor/Xt/viewers/SoXtPlaneViewer.h
%include Inventor/Xt/widgets/SoXtPopupMenu.h
%include Inventor/Xt/SoXtResource.h
%include Inventor/Xt/SoXt.h
%include Inventor/Xt/SoXtBasic.h
%include Inventor/Xt/SoXtObject.h
%include Inventor/Xt/SoXtCursor.h
%include Inventor/Xt/SoXtComponent.h
%include Inventor/Xt/SoXtGLWidget.h
%include Inventor/Xt/SoXtRenderArea.h
%include Inventor/Xt/SoXtColorEditor.h
%include Inventor/Xt/SoXtMaterialEditor.h
