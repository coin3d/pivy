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
#if defined(_WIN32) || defined(__WIN32__)
#include <windows.h>
#undef max
#undef ERROR
#undef DELETE
#undef ANY
#endif

#include <Inventor/Qt/devices/SoQtDevice.h>
#include <Inventor/Qt/devices/SoQtKeyboard.h>
#include <Inventor/Qt/devices/SoQtSpaceball.h>
#include <Inventor/Qt/devices/SoQtMouse.h>
#include <Inventor/Qt/SoQtBasic.h>
#include <Inventor/Qt/nodes/SoGuiColorEditor.h>
#include <Inventor/Qt/editors/SoQtColorEditor.h>
#include <Inventor/Qt/SoQtObject.h>
#include <Inventor/Qt/SoQt.h>
#include <Inventor/Qt/SoQtGLWidget.h>
#include <Inventor/Qt/SoQtColorEditor.h>
#include <Inventor/Qt/viewers/SoQtPlaneViewer.h>
#include <Inventor/Qt/viewers/SoQtViewer.h>
#include <Inventor/Qt/viewers/SoQtExaminerViewer.h>
#include <Inventor/Qt/viewers/SoQtFlyViewer.h>
#include <Inventor/Qt/viewers/SoQtConstrainedViewer.h>
#include <Inventor/Qt/viewers/SoQtFullViewer.h>
#include <Inventor/Qt/widgets/SoQtThumbWheel.h>
#include <Inventor/Qt/widgets/SoQtPopupMenu.h>
#include <Inventor/Qt/SoQtComponent.h>
#include <Inventor/Qt/SoQtCursor.h>
#include <Inventor/Qt/SoQtRenderArea.h>

#include <Inventor/SbDPMatrix.h>
#include <Inventor/SbDPRotation.h>
#include <Inventor/SbVec2d.h>
#include <Inventor/C/threads/thread.h>

/* make CustomCursor in SoQtCursor known to SWIG */
typedef SoQtCursor::CustomCursor CustomCursor;

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

/* typemaps to bridge against PyQt */

%typemap(out) QEvent * {
  {
    PyObject *sip, *qt;

    /* try to create a PyQt QEvent instance over sip */
    
    /* check if the sip module is available and import it */
    if (!(sip = PyDict_GetItemString(PyModule_GetDict(PyImport_AddModule("__main__")),
                                     "sip"))) {
      sip = PyImport_ImportModule("sip");
    }
    
    if (sip && PyModule_Check(sip)) {
      /* check if the qt module is available and import it */
      if (!(qt = PyDict_GetItemString(PyModule_GetDict(PyImport_AddModule("__main__")),
                                      "qt"))) {
        qt = PyImport_ImportModule("qt");
      }
      
      if (qt && PyModule_Check(qt)) {
        /* grab the wrapinstance(addr, type) function */
        PyObject *sip_wrapinst_func;
        sip_wrapinst_func = PyDict_GetItemString(PyModule_GetDict(sip),
                                                 "wrapinstance");
        
        if (PyCallable_Check(sip_wrapinst_func)) {
          PyObject *qevent_type, *arglist;
          qevent_type = PyDict_GetItemString(PyModule_GetDict(qt), "QEvent");
          
          arglist = Py_BuildValue("(lO)", $1, qevent_type);
          
          if (!($result = PyEval_CallObject(sip_wrapinst_func, arglist))) {
            PyErr_Print();
          }
          
          Py_DECREF(arglist);
        }
      }
    }

    /* if no QEvent could be created through sip return a swig QEvent type */
    if (!$result) {
      $result = SWIG_NewPointerObj((void *)$1, SWIGTYPE_p_QEvent, 0);
    }
  }
}

%typemap(out) QWidget * {
  {
    PyObject *sip, *qt;

    /* try to create a PyQt QWidget instance over sip */
    
    /* check if the sip module is available and import it */
    if (!(sip = PyDict_GetItemString(PyModule_GetDict(PyImport_AddModule("__main__")),
                                     "sip"))) {
      sip = PyImport_ImportModule("sip");
    }
    
    if (sip && PyModule_Check(sip)) {
      /* check if the qt module is available and import it */
      if (!(qt = PyDict_GetItemString(PyModule_GetDict(PyImport_AddModule("__main__")),
                                      "qt"))) {
        qt = PyImport_ImportModule("qt");
      }
      
      if (qt && PyModule_Check(qt)) {
        /* grab the wrapinstance(addr, type) function */
        PyObject *sip_wrapinst_func;
        sip_wrapinst_func = PyDict_GetItemString(PyModule_GetDict(sip),
                                                 "wrapinstance");
        
        if (PyCallable_Check(sip_wrapinst_func)) {
          PyObject *qwidget_type, *arglist;
          qwidget_type = PyDict_GetItemString(PyModule_GetDict(qt), "QWidget");
          
          arglist = Py_BuildValue("(lO)", $1, qwidget_type);
          
          if (!($result = PyEval_CallObject(sip_wrapinst_func, arglist))) {
            PyErr_Print();
          }
          
          Py_DECREF(arglist);
        }
      }
    }

    /* if no QWidget could be created through sip return a swig QWidget type */
    if (!$result) {
      $result = SWIG_NewPointerObj((void *)$1, SWIGTYPE_p_QWidget, 0);
    }
  }
}

%typemap(in) QEvent * {
  {
    PyObject *sip;
    
    /* check if the sip module is available and import it */
    if (!(sip = PyDict_GetItemString(PyModule_GetDict(PyImport_AddModule("__main__")),
                                     "sip"))) {
      sip = PyImport_ImportModule("sip");
    }
    
    if (sip && PyModule_Check(sip)) {
      /* grab the unwrapinstance(obj) function */
      PyObject *sip_unwrapinst_func;
      sip_unwrapinst_func = PyDict_GetItemString(PyModule_GetDict(sip),
                                                 "unwrapinstance");
        
      if (PyCallable_Check(sip_unwrapinst_func)) {
        PyObject *arglist, *address;
        arglist = Py_BuildValue("(O)", $input);
        if (!(address = PyEval_CallObject(sip_unwrapinst_func, arglist))) {
          PyErr_Print();
        } else if (PyNumber_Check(address)) {
            $1 = (QEvent*)PyLong_AsLong(address);
        }
          
        Py_DECREF(arglist);
      }
    }
  }

  if (!$1) {
    if ((SWIG_ConvertPtr($input, (void **)&$1, SWIGTYPE_p_QEvent,SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
  }
}

%typemap(in) QWidget * {
  {
    PyObject *sip;
    
    /* check if the sip module is available and import it */
    if (!(sip = PyDict_GetItemString(PyModule_GetDict(PyImport_AddModule("__main__")),
                                     "sip"))) {
      sip = PyImport_ImportModule("sip");
    }
    
    if (sip && PyModule_Check(sip)) {
      /* grab the unwrapinstance(obj) function */
      PyObject *sip_unwrapinst_func;
      sip_unwrapinst_func = PyDict_GetItemString(PyModule_GetDict(sip),
                                                 "unwrapinstance");
      
      if (PyCallable_Check(sip_unwrapinst_func)) {
        PyObject *arglist, *address;
        arglist = Py_BuildValue("(O)", $input);
        if (!(address = PyEval_CallObject(sip_unwrapinst_func, arglist))) {
          PyErr_Print();
        } else if (PyNumber_Check(address)) {
            $1 = (QWidget*)PyLong_AsLong(address);
        }
        
        Py_DECREF(arglist);
      }
    }
  }
  
  if (!$1) {
    if ((SWIG_ConvertPtr($input, (void **)&$1, SWIGTYPE_p_QWidget,SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
  }
}

%include Inventor/Qt/devices/SoQtDevice.h
%include Inventor/Qt/devices/SoQtKeyboard.h
%include Inventor/Qt/devices/SoQtSpaceball.h
%include Inventor/Qt/devices/SoQtMouse.h
%include Inventor/Qt/SoQtBasic.h
%include Inventor/Qt/nodes/SoGuiColorEditor.h
%include Inventor/Qt/editors/SoQtColorEditor.h
%include Inventor/Qt/SoQtObject.h
%include Inventor/Qt/SoQt.h
%include Inventor/Qt/SoQtGLWidget.h
%include Inventor/Qt/SoQtColorEditor.h
%include Inventor/Qt/viewers/SoQtPlaneViewer.h
%include Inventor/Qt/viewers/SoQtViewer.h
%include Inventor/Qt/viewers/SoQtExaminerViewer.h
%include Inventor/Qt/viewers/SoQtFlyViewer.h
%include Inventor/Qt/viewers/SoQtConstrainedViewer.h
%include Inventor/Qt/viewers/SoQtFullViewer.h
%include Inventor/Qt/widgets/SoQtPopupMenu.h
%include Inventor/Qt/SoQtComponent.h
%include Inventor/Qt/SoQtCursor.h
%include Inventor/Qt/SoQtRenderArea.h
