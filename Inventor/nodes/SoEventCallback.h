/**************************************************************************\
 *
 *  This file is part of the Coin 3D visualization library.
 *  Copyright (C) 1998-2002 by Systems in Motion. All rights reserved.
 *
 *  This library is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU Lesser General Public License
 *  version 2.1 as published by the Free Software Foundation. See the
 *  file LICENSE.LGPL at the root directory of the distribution for
 *  more details.
 *
 *  If you want to use Coin for applications not compatible with the
 *  LGPL, please contact SIM to acquire a Professional Edition license.
 *
 *  Systems in Motion, Prof Brochs gate 6, 7030 Trondheim, NORWAY
 *  http://www.sim.no support@sim.no Voice: +47 22114160 Fax: +47 22207097
 *
\**************************************************************************/

#ifndef COIN_SOEVENTCALLBACK_H
#define COIN_SOEVENTCALLBACK_H

#include <Inventor/nodes/SoSubNode.h>
#include <Inventor/lists/SbList.h>

#ifndef COIN_INTERNAL
// Added for Inventor compliance
#include <Inventor/actions/SoHandleEventAction.h>
#endif // !COIN_INTERNAL


class SoEventCallback;
class SoPath;
class SoEvent;
class SoPickedPoint;
class SoHandleEventAction;

typedef void SoEventCallbackCB(void * userdata, SoEventCallback * node);

#ifdef __PIVY__
%{
static PyObject *pyfunc_callback = NULL;

static void
PythonCallBack(void)
{
  PyObject *func, *arglist;
  PyObject *result;

  func = pyfunc_callback;	 /* This is the function .... */
  arglist = Py_BuildValue("()");  /* No arguments needed */
  result =  PyEval_CallObject(func, arglist);
  Py_DECREF(arglist);
  Py_XDECREF(result);
  return /*void*/;
}

void
set_callback(PyObject *PyFunc)
{
  Py_XDECREF(pyfunc_callback);   /* dispose of previous callback */
  Py_XINCREF(PyFunc);	       /* add a reference to new callback */
  pyfunc_callback = PyFunc;      /* remember new callback */
  EventCB_set_callback(PythonCallBack);
}

%}

%typemap(in) PyObject *PyFunc {
  if (!PyCallable_Check($source)) {
    PyErr_SetString(PyExc_TypeError, "need a callable object!");
    return NULL;
  }
  $target = $source;
}

void
set_callback(PyObject *PyFunc);

#endif

class COIN_DLL_API SoEventCallback : public SoNode {
  typedef SoNode inherited;

  SO_NODE_HEADER(SoEventCallback);

public:
  static void initClass(void);
  SoEventCallback(void);

  void setPath(SoPath * path);
  const SoPath * getPath(void);

  void addEventCallback(SoType eventtype, SoEventCallbackCB * f,
                        void * userdata = NULL);
  void removeEventCallback(SoType eventtype, SoEventCallbackCB * f,
                           void * userdata = NULL);

  SoHandleEventAction * getAction(void) const;
  const SoEvent * getEvent(void) const;
  const SoPickedPoint * getPickedPoint(void) const;

  void setHandled(void);
  SbBool isHandled(void) const;

  void grabEvents(void);
  void releaseEvents(void);

protected:
  virtual ~SoEventCallback();

  virtual void handleEvent(SoHandleEventAction * action);

private:
  struct CallbackInfo {
    SoEventCallbackCB * func;
    SoType eventtype;
    void * userdata;

    // AIX native compiler xlC needs equality and inequality operators
    // to compile templates where these operators are referenced (even
    // if they are actually never used).

    SbBool operator==(const CallbackInfo & cbi) {
      return this->func == cbi.func && this->eventtype == cbi.eventtype && this->userdata == cbi.userdata;
    }
    SbBool operator!=(const CallbackInfo & cbi) {
      return !(*this == cbi);
    }
  };

  SbList<CallbackInfo> callbacks;
  SoHandleEventAction * heaction;
  SoPath * path;

};

#endif // !COIN_SOEVENTCALLBACK_H
