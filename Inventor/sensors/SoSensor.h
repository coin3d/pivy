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

#ifndef COIN_SOSENSOR_H
#define COIN_SOSENSOR_H

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
      self.this = apply(pivyc.new_SoSensor_scb_v,args)
      self.thisown = 1
      return
   self.this = apply(pivyc.new_SoSensor,args)
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
