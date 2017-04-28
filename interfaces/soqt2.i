/*
 * Copyright (c) 2002-2007 Systems in Motion
 *
 * Permission to use, copy, modify, and distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 * OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */


// define PY_2 for c++ preprocessor
#ifndef PY_2
#define PY_2
#endif

// define PY_2 for swig preprocessor
%{
#ifndef PY_2
#define PY_2
#endif
%}



%define SOQT_MODULE_DOCSTRING
"The soqt module is a wrapper for the SoQt library. The module will try
to import the shiboken module which is used for PySide. If found the involved
wrapped Qt structures are converted to ones suitable for PySide,
otherwise it will fall back to regular SWIG structures."
%enddef

%module(package="pivy.gui", docstring=SOQT_MODULE_DOCSTRING) soqt

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
#include <Inventor/Qt/devices/SoQtMouse.h>
#include <Inventor/Qt/SoQtBasic.h>
#include <Inventor/Qt/SoQtComponent.h>
#include <Inventor/Qt/SoQtCursor.h>
#include <Inventor/Qt/SoQtGLWidget.h>
#include <Inventor/Qt/SoQt.h>
#include <Inventor/Qt/SoQtObject.h>
#include <Inventor/Qt/SoQtRenderArea.h>
#include <Inventor/Qt/viewers/SoQtConstrainedViewer.h>
#include <Inventor/Qt/viewers/SoQtExaminerViewer.h>
#include <Inventor/Qt/viewers/SoQtFlyViewer.h>
#include <Inventor/Qt/viewers/SoQtFullViewer.h>
#include <Inventor/Qt/viewers/SoQtPlaneViewer.h>
#include <Inventor/Qt/viewers/SoQtViewer.h>
#include <Inventor/Qt/widgets/SoQtPopupMenu.h>
#include <Inventor/Qt/widgets/SoQtThumbWheel.h>

#include "coin_header_includes.h"

/* make CustomCursor in SoQtCursor known to SWIG */
typedef SoQtCursor::CustomCursor CustomCursor;

/* FIXME: there is a major pitfall reg. this solution, namely
 * thread safety! reconsider! 20030626 tamer.
 */
static void *
Pivy_PythonInteractiveLoop(void *data) {
  PyRun_InteractiveLoop(stdin, "<stdin>");
  return NULL;
}

static const char * PYSIDE_QTGUI = "PySide.QtGui";
static const char * PYSIDE_QTCORE = "PySide.QtCore";


static PyObject* getShiboken()
{
  // simplified version
  // to get a qt representation in python
  // simple import shiboken from python.
  // from Shiboken import shiboken
  return PyDict_GetItemString(PyModule_GetDict(PyImport_AddModule("__main__")), "shiboken");
}

%}

/* include the typemaps common to all pivy modules */
%include pivy_common_typemaps.i

/* import the pivy main interface file */
%import coin.i

/* typemaps to bridge against PySide */
%typemap(out) QEvent * {
  $result = NULL;
  {
    PyObject *qt;
    PyObject *shiboken = getShiboken();
    /* try to create a PySide QEvent instance through shiboken */

    
    if (shiboken && PyModule_Check(shiboken)) {
      /* check if the qt module is available and import it */
      if (!(qt = PyDict_GetItemString(PyModule_GetDict(PyImport_AddModule("__main__")), PYSIDE_QTCORE))) {
        qt = PyImport_ImportModule(PYSIDE_QTCORE);
      }
      
      if (qt && PyModule_Check(qt)) {
        /* grab the wrapInstance(addr, type) function */
        PyObject *shiboken_wrapinst_func;
        shiboken_wrapinst_func = PyDict_GetItemString(PyModule_GetDict(shiboken), "wrapInstance");
        
        if (PyCallable_Check(shiboken_wrapinst_func)) {
          PyObject *qevent_type, *arglist;
          qevent_type = PyDict_GetItemString(PyModule_GetDict(qt), "QEvent");
          
          arglist = Py_BuildValue("(lO)", $1, qevent_type);
          
          if (!($result = PyEval_CallObject(shiboken_wrapinst_func, arglist))) {
            PyErr_Print();
          }
          
          Py_DECREF(arglist);
        }
      }
    }

    /* if no QEvent could be created through shiboken return a swig QEvent type */
    if (PyErr_ExceptionMatches(PyExc_ImportError) || !$result) {
      PyErr_Clear();
      $result = SWIG_NewPointerObj((void *)($1), SWIGTYPE_p_QEvent, 0);
    }
  }
}

%typemap(out) QWidget * {
  $result = NULL;
  {
    PyObject *qt;
    PyObject *shiboken = getShiboken();
    /* try to create a PySide QWidget instance through shiboken */

    
    if (shiboken && PyModule_Check(shiboken)) {
      /* check if the qt module is available and import it */
      if (!(qt = PyDict_GetItemString(PyModule_GetDict(PyImport_AddModule("__main__")), PYSIDE_QTGUI))) {
        qt = PyImport_ImportModule(PYSIDE_QTGUI);
      }
      
      if (qt && PyModule_Check(qt)) {
        /* grab the wrapInstance(addr, type) function */
        PyObject *shiboken_wrapinst_func;
        shiboken_wrapinst_func = PyDict_GetItemString(PyModule_GetDict(shiboken), "wrapInstance");
        
        if (PyCallable_Check(shiboken_wrapinst_func)) {
          PyObject *qwidget_type, *arglist;
          qwidget_type = PyDict_GetItemString(PyModule_GetDict(qt), "QWidget");
          
          arglist = Py_BuildValue("(lO)", $1, qwidget_type);
          
          if (!($result = PyEval_CallObject(shiboken_wrapinst_func, arglist))) {
            PyErr_Print();
          }
          
          Py_DECREF(arglist);
        }
      }
    }

    /* if no QWidget could be created through shiboken return a swig QWidget type */
    if (PyErr_ExceptionMatches(PyExc_ImportError) || !$result) {
      PyErr_Clear();
      $result = SWIG_NewPointerObj((void *)($1), SWIGTYPE_p_QWidget, 0);
    }
  }
}

%typemap(in) QEvent * {
  {
    PyObject *shiboken = getShiboken();
    
    
    if (shiboken && PyModule_Check(shiboken)) {
      /* grab the getCppPointer(obj) function */
      PyObject *shiboken_unwrapinst_func;
      shiboken_unwrapinst_func = PyDict_GetItemString(PyModule_GetDict(shiboken), "getCppPointer");
        
      if (PyCallable_Check(shiboken_unwrapinst_func)) {
        PyObject *arglist, *address;
        arglist = Py_BuildValue("(O)", $input);
        if (!(address = PyEval_CallObject(shiboken_unwrapinst_func, arglist))) {
          PyErr_Print();
        } else if (PyNumber_Check(address)) {
          $1 = (QEvent*)PyLong_AsVoidPtr(address);
        } else if (PyTuple_Check(address)) {
          $1 = (QEvent*)PyLong_AsVoidPtr(PyTuple_GetItem(address, 0));
        }
          
        Py_DECREF(arglist);
      }
    }
  }

  if (PyErr_ExceptionMatches(PyExc_ImportError) || !$1) {
    PyErr_Clear();
    if ((SWIG_ConvertPtr($input, (void **)(&$1), SWIGTYPE_p_QEvent, SWIG_POINTER_EXCEPTION | 0)) == -1) SWIG_fail;
  }
}

%typemap(in) QWidget * {
  {
    if ($input == Py_None) {
      $1 = NULL;
    } else {
      PyObject *shiboken = getShiboken();
    
      /* check if the shiboken module is available and import it */
      if (!(shiboken = PyDict_GetItemString(PyModule_GetDict(PyImport_AddModule("__main__")), "shiboken"))) {
        shiboken = PyImport_ImportModule("shiboken");
      }
    
      if (shiboken && PyModule_Check(shiboken)) {
        /* grab the getCppPointer(obj) function */
        PyObject *shiboken_unwrapinst_func;
        shiboken_unwrapinst_func = PyDict_GetItemString(PyModule_GetDict(shiboken), "getCppPointer");
      
        if (PyCallable_Check(shiboken_unwrapinst_func)) {
          PyObject *arglist, *address;
          arglist = Py_BuildValue("(O)", $input);
          if (!(address = PyEval_CallObject(shiboken_unwrapinst_func, arglist))) {
            PyErr_Print();
          } else if (PyNumber_Check(address)) {
            $1 = (QWidget*)PyLong_AsVoidPtr(address);
          } else if (PyTuple_Check(address)) {
          $1 = (QWidget*)PyLong_AsVoidPtr(PyTuple_GetItem(address, 0));
        }
        
          Py_DECREF(arglist);
        }
      }
    }
  
    if (PyErr_ExceptionMatches(PyExc_ImportError) || !$1) {
      PyErr_Clear();
      if ((SWIG_ConvertPtr($input, (void **)(&$1), SWIGTYPE_p_QWidget, SWIG_POINTER_EXCEPTION | 0)) == -1) SWIG_fail;
    }
  }  
}

class QEvent { QEvent(Type type); };
class QWidget { QWidget(QWidget* parent=0, const char* name=0, WFlags f=0); };

/* typemap typechecks for the overloaded constructors needed from SWIG 1.3.25 upwards */
%typemap(typecheck) QEvent * {
  void *ptr = NULL;
  {
    PyObject *shiboken = getShiboken()
    
    
    if (shiboken && PyModule_Check(shiboken)) {
      /* grab the getCppPointer(obj) function */
      PyObject *shiboken_unwrapinst_func;
      shiboken_unwrapinst_func = PyDict_GetItemString(PyModule_GetDict(shiboken), "getCppPointer");
        
      if (PyCallable_Check(shiboken_unwrapinst_func)) {
        PyObject *arglist, *address;
        arglist = Py_BuildValue("(O)", $input);
        if (!(address = PyEval_CallObject(shiboken_unwrapinst_func, arglist))) {
          PyErr_Print();
        } else if (PyNumber_Check(address)) {
         ptr = (QEvent*)PyLong_AsVoidPtr(address);
        } else if (PyTuple_Check(address)) {
         ptr = (QEvent*)PyLong_AsVoidPtr(PyTuple_GetItem(address, 0));
        }
          
        Py_DECREF(arglist);
      }
    }
  }

  $1 = 1;
  if (PyErr_ExceptionMatches(PyExc_ImportError) || !ptr) {
    $1 = 0;
    PyErr_Clear();
    if ((SWIG_ConvertPtr($input, (void **)(&ptr), SWIGTYPE_p_QEvent, 0)) != -1) {
      $1 = 1;
    }
  }
}

%typemap(typecheck) QWidget * {
  void *ptr = NULL;
  {
    PyObject *shiboken = getShiboken();
    
    
    if (shiboken && PyModule_Check(shiboken)) {
      /* grab the getCppPointer(obj) function */
      PyObject *shiboken_unwrapinst_func;
      shiboken_unwrapinst_func = PyDict_GetItemString(PyModule_GetDict(shiboken), "getCppPointer");
        
      if (PyCallable_Check(shiboken_unwrapinst_func)) {
        PyObject *arglist, *address;
        arglist = Py_BuildValue("(O)", $input);
        if (!(address = PyEval_CallObject(shiboken_unwrapinst_func, arglist))) {
          PyErr_Print();
        } else if (PyNumber_Check(address)) {
         ptr = (QWidget*)PyLong_AsVoidPtr(address);
        } else if (PyTuple_Check(address)) {
         ptr = (QWidget*)PyLong_AsVoidPtr(PyTuple_GetItem(address, 0));
        }
          
        Py_DECREF(arglist);
      }
    }
  }

  $1 = 1;
  if (PyErr_ExceptionMatches(PyExc_ImportError) || !ptr) {
    $1 = 0;
    PyErr_Clear();
    if ((SWIG_ConvertPtr($input, (void **)(&ptr), SWIGTYPE_p_QWidget, 0)) != -1) {
      $1 = 1;
    }
  }
}

%include Inventor/Qt/devices/SoQtDevice.h
%include Inventor/Qt/devices/SoQtKeyboard.h
%include Inventor/Qt/devices/SoQtMouse.h
%include Inventor/Qt/SoQtBasic.h
%include Inventor/Qt/SoQtObject.h
%include Inventor/Qt/SoQt.h
%include Inventor/Qt/SoQtGLWidget.h
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
