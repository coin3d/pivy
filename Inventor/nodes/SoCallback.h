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

#ifndef COIN_SOCALLBACK_H
#define COIN_SOCALLBACK_H

#include <Inventor/nodes/SoSubNode.h>


typedef void SoCallbackCB(void * userdata, SoAction * action);


#ifdef __PIVY__
%{
static void
SoPythonCallBack(void * userdata, SoAction * action)
{
  PyObject *func, *arglist;
  PyObject *result, *acCB;

  acCB = SWIG_NewPointerObj((void *) action, SWIGTYPE_p_SoAction, 1);

  /* the first item in the userdata sequence is the python callback
   * function; the second is the supplied userdata python object */
  func = PyTuple_GetItem((PyObject *)userdata, 0);
  arglist = Py_BuildValue("OO", PyTuple_GetItem((PyObject *)userdata, 1), acCB);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
	printf("SoPythonCallBack(void * userdata, SoAction * action) failed!\n");
  }

  Py_DECREF(arglist);
  Py_XDECREF(result);

  return /*void*/;
}
%}

%typemap(in) PyObject *pyfunc %{
  if (!PyCallable_Check($input)) {
	PyErr_SetString(PyExc_TypeError, "need a callable object!");
	return NULL;
  }
  $1 = $input;
%}
#endif

class COIN_DLL_API SoCallback : public SoNode {
    typedef SoNode inherited;

  SO_NODE_HEADER(SoCallback);

public:
  static void initClass(void);
  SoCallback(void);

  void setCallback(SoCallbackCB * function, void * userdata = NULL);

#ifdef __PIVY__
  /* add python specific callback functions */
  %addmethods {
	void setPythonCallback(PyObject *pyfunc, PyObject *userdata = NULL) {
	  if (userdata == NULL) {
		Py_INCREF(Py_None);
		userdata = Py_None;
	  }
	  
	  PyObject *t = PyTuple_New(2);
	  PyTuple_SetItem(t, 0, pyfunc);
	  PyTuple_SetItem(t, 1, userdata);
	  Py_INCREF(pyfunc);
	  Py_INCREF(userdata);

	  self->setCallback(SoPythonCallBack, (void *) t);
	}
  }
#endif

  virtual void doAction(SoAction * action);
  virtual void callback(SoCallbackAction * action);
  virtual void GLRender(SoGLRenderAction * action);
  virtual void getBoundingBox(SoGetBoundingBoxAction * action);
  virtual void getMatrix(SoGetMatrixAction * action);
  virtual void handleEvent(SoHandleEventAction * action);
  virtual void pick(SoPickAction * action);
  virtual void search(SoSearchAction * action);
  virtual void write(SoWriteAction * action);
  virtual void getPrimitiveCount(SoGetPrimitiveCountAction * action);

protected:
  virtual ~SoCallback();

  virtual void copyContents(const SoFieldContainer * from,
                            SbBool copyconnections);

private:
  SoCallbackCB * cbfunc;
  void * cbdata;
};

#endif // !COIN_SOCALLBACK_H
