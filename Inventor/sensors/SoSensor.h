#ifndef COIN_SOSENSOR_H
#define COIN_SOSENSOR_H

/**************************************************************************\
 *
 *  This file is part of the Coin 3D visualization library.
 *  Copyright (C) 1998-2003 by Systems in Motion.  All rights reserved.
 *
 *  This library is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU General Public License
 *  ("GPL") version 2 as published by the Free Software Foundation.
 *  See the file LICENSE.GPL at the root directory of this source
 *  distribution for additional information about the GNU GPL.
 *
 *  For using Coin with software that can not be combined with the GNU
 *  GPL, and for taking advantage of the additional benefits of our
 *  support services, please contact Systems in Motion about acquiring
 *  a Coin Professional Edition License.
 *
 *  See <URL:http://www.coin3d.org> for  more information.
 *
 *  Systems in Motion, Teknobyen, Abels Gate 5, 7030 Trondheim, NORWAY.
 *  <URL:http://www.sim.no>.
 *
\**************************************************************************/

#include <Inventor/SbBasic.h>

class SoSensor;

typedef void SoSensorCB(void * data, SoSensor * sensor);

#ifdef __PIVY__
%{
static void
SoSensorPythonCB(void * data, SoSensor * sensor)
{
  PyObject *func, *arglist;
  PyObject *result, *sensCB;

  sensCB = SWIG_NewPointerObj((void *) sensor, SWIGTYPE_p_SoSensor, 1);

  /* the first item in the data sequence is the python callback
   * function; the second is the supplied data python object */
  func = PyTuple_GetItem((PyObject *)data, 0);
  arglist = Py_BuildValue("OO", PyTuple_GetItem((PyObject *)data, 1), sensCB);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
	printf("SoSensorPythonCB(void * data, SoSensor * sensor) failed!\n");
  }

  Py_DECREF(arglist);
  Py_XDECREF(result);

  return /*void*/;
}
%}

%rename(SoSensor_scb_v) SoSensor::SoSensor(SoSensorCB * func, void * data);

%feature("shadow") SoSensor::SoSensor %{
def __init__(self,*args):
   if len(args) == 2:
      args = (args[0], (args[0], args[1]))
      self.this = apply(_pivy.new_SoSensor_scb_v,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SoSensor,args)
   self.thisown = 1
%}

%typemap(in) SoSensorCB * func %{
  if (!PyCallable_Check($input)) {
	PyErr_SetString(PyExc_TypeError, "need a callable object!");
	return NULL;
  }
  $1 = SoSensorPythonCB;
%}

%typemap(in) void * data %{
  if (!PyTuple_Check($input)) {
	PyErr_SetString(PyExc_TypeError, "tuple expected!");
	return NULL;
  }

  Py_INCREF($input);
  $1 = (void *)$input;
%}
#endif

class COIN_DLL_API SoSensor {
public:
  SoSensor(void);
  SoSensor(SoSensorCB * func, void * data);
  virtual ~SoSensor(void);

  void setFunction(SoSensorCB * callbackfunction);
  SoSensorCB * getFunction(void) const;
  void setData(void * callbackdata);
  void * getData(void) const;

  virtual void schedule(void) = 0;
  virtual void unschedule(void) = 0;
  virtual SbBool isScheduled(void) const = 0;

  virtual void trigger(void);

  virtual SbBool isBefore(const SoSensor * s) const = 0;
  void setNextInQueue(SoSensor * next);
  SoSensor * getNextInQueue(void) const;

  static void initClass(void);

protected:
  SoSensorCB * func;
  void * funcData;
};

#endif // !COIN_SOSENSOR_H
