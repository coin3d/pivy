#ifndef COIN_SOINTERSECTIONDETECTIONACTION_H
#define COIN_SOINTERSECTIONDETECTIONACTION_H

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

#include <Inventor/actions/SoSubAction.h>
#include <Inventor/actions/SoAction.h>
#include <Inventor/actions/SoCallbackAction.h>

struct SoIntersectingPrimitive {
  SoPath * path;
  enum PrimitiveType {
    SEGMENT = 2,
    LINE_SEGMENT = 2,
    TRIANGLE = 3
  } type;
  SbVec3f vertex[3];
  SbVec3f xf_vertex[3];
};

class SoIntersectionDetectionActionP;


#ifdef __PIVY__
%{
static SoCallbackAction::Response
SoIntersectionVisitationPythonCB(void * closure, 
                                 const SoPath * where)
   {
  PyObject *func, *arglist;
  PyObject *result, *path;
  int iresult = 0;

  path = SWIG_NewPointerObj((void *) where, SWIGTYPE_p_SoPath, 1);

  /* the first item in the userdata sequence is the python callback
   * function; the second is the supplied userdata python object */
  func = PyTuple_GetItem((PyObject *)closure, 0);
  arglist = Py_BuildValue("OO", PyTuple_GetItem((PyObject *)closure, 1), path);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
	printf("SoIntersectionVisitationPythonCB(void * closure, const SoPath * where) failed!\n");
  }
  else {
	iresult = PyInt_AsLong(result);
  }
  
  Py_DECREF(arglist);
  Py_XDECREF(result);

  return (SoCallbackAction::Response)iresult;
}


static SbBool
SoIntersectionFilterPythonCB(void * closure,
                             const SoPath * p1,
                             const SoPath * p2)
{   
  PyObject *func, *arglist;
  PyObject *result, *path1, *path2;
  int iresult = 0;

  path1 = SWIG_NewPointerObj((void *) path1, SWIGTYPE_p_SoPath, 1);
  path2 = SWIG_NewPointerObj((void *) path2, SWIGTYPE_p_SoPath, 1);

  /* the first item in the userdata sequence is the python callback
   * function; the second is the supplied userdata python object */
  func = PyTuple_GetItem((PyObject *)closure, 0);
  arglist = Py_BuildValue("OOO", PyTuple_GetItem((PyObject *)closure, 1), path1, path2);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
	printf("SoIntersectionFilterPythonCB(void * closure, const SoPath * p1, const SoPath * p2) failed!\n");
  }
  else {
	iresult = PyInt_AsLong(result);
  }
  
  Py_DECREF(arglist);
  Py_XDECREF(result);

  return (SbBool)iresult;
}

static SoIntersectionDetectionAction::Resp
SoIntersectionPythonCB(void * closure, 
                 const SoIntersectingPrimitive * p1, 
                 const SoIntersectingPrimitive * p2)
{
  PyObject *func, *arglist;
  PyObject *result, *primitive1, *primitive2;
  int iresult = 0;

  primitive1 = SWIG_NewPointerObj((void *) primitive1, SWIGTYPE_p_SoIntersectingPrimitive, 1);
  primitive2 = SWIG_NewPointerObj((void *) primitive2, SWIGTYPE_p_SoIntersectingPrimitive, 1);

  /* the first item in the userdata sequence is the python callback
   * function; the second is the supplied userdata python object */
  func = PyTuple_GetItem((PyObject *)closure, 0);
  arglist = Py_BuildValue("OOO", PyTuple_GetItem((PyObject *)closure, 1), primitive1, primitive2);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
	printf("SoIntersectionPythonCB(void * closure, const SoIntersectingPrimitive * p1, const SoIntersectingPrimitive * p2) failed!\n");
  }
  else {
	iresult = PyInt_AsLong(result);
  }
  
  Py_DECREF(arglist);
  Py_XDECREF(result);

  return (SoIntersectionDetectionAction::Resp)iresult;
}
%}

%rename(apply_nod) SoIntersectionDetectionAction::apply(SoNode *root);
%rename(apply_pat) SoIntersectionDetectionAction::apply(SoPath *path);

%feature("shadow") SoIntersectionDetectionAction::apply(const SoPathList & paths, SbBool obeysRules = FALSE) %{
def apply(*args):
   if len(args) == 2:
      if isinstance(args[1], SoNode):
         return apply(_pivy.SoIntersectionDetectionAction_apply_nod,args)
      elif isinstance(args[1], SoPath):
         return apply(_pivy.SoIntersectionDetectionAction_apply_pat,args)
   return apply(_pivy.SoIntersectionDetectionAction_apply,args)
%}
#endif

class COIN_DLL_API SoIntersectionDetectionAction : public SoAction {
  typedef SoAction hinherited;
  SO_ACTION_HEADER(SoIntersectionDetectionAction);
public:
  static void initClass(void);
  SoIntersectionDetectionAction(void);
  virtual ~SoIntersectionDetectionAction(void);

  enum Resp {
    NEXT_PRIMITIVE,
    NEXT_SHAPE,
    ABORT
  };

  typedef SoCallbackAction::Response SoIntersectionVisitationCB(void * closure, const SoPath * where);
  typedef SbBool SoIntersectionFilterCB(void * closure, const SoPath * p1, const SoPath * p2);
  typedef Resp SoIntersectionCB(void * closure, const SoIntersectingPrimitive * p1, const SoIntersectingPrimitive * p2);

  void setIntersectionDetectionEpsilon(float epsilon);
  float getIntersectionDetectionEpsilon(void) const;

  static void setIntersectionEpsilon(float epsilon);
  static float getIntersectionEpsilon(void);

  void setTypeEnabled(SoType type, SbBool enable);
  SbBool isTypeEnabled(SoType type, SbBool checkgroups = FALSE) const;

  void setManipsEnabled(SbBool enable);
  SbBool isManipsEnabled(void) const;

  void setDraggersEnabled(SbBool enable);
  SbBool isDraggersEnabled(void) const;

  void setShapeInternalsEnabled(SbBool enable);
  SbBool isShapeInternalsEnabled(void) const;

  void addVisitationCallback(SoType type, SoIntersectionVisitationCB * cb, void * closure);
  void removeVisitationCallback(SoType type, SoIntersectionVisitationCB * cb, void * closure);

  virtual void apply(SoNode * node);
  virtual void apply(SoPath * path);
  virtual void apply(const SoPathList & paths, SbBool obeysRules = FALSE);

  virtual void setFilterCallback(SoIntersectionFilterCB * cb, void * closure = NULL);
  virtual void addIntersectionCallback(SoIntersectionCB * cb, void * closure  = NULL);
  virtual void removeIntersectionCallback(SoIntersectionCB * cb, void * closure  = NULL);

#ifdef __PIVY__
  /* add python specific callback functions */
  %extend {
    void addPythonVisitationCallback(SoType type, PyObject * pyfunc, PyObject * closure) {
	  PyObject *t = PyTuple_New(2);
	  PyTuple_SetItem(t, 0, pyfunc);
	  PyTuple_SetItem(t, 1, closure);
	  Py_INCREF(pyfunc);
	  Py_INCREF(closure);

	  self->addVisitationCallback(type, SoIntersectionVisitationPythonCB, (void *) t);       
    }

    void removePythonVisitationCallback(SoType type, PyObject * pyfunc, PyObject * closure) {
	  PyObject *t = PyTuple_New(2);
	  PyTuple_SetItem(t, 0, pyfunc);
	  PyTuple_SetItem(t, 1, closure);
	  Py_INCREF(pyfunc);
	  Py_INCREF(closure);

	  self->removeVisitationCallback(type, SoIntersectionVisitationPythonCB, (void *) t);
    }

    void setPythonFilterCallback(PyObject * pyfunc, PyObject * closure = NULL) {
	  PyObject *t = PyTuple_New(2);
	  PyTuple_SetItem(t, 0, pyfunc);
	  PyTuple_SetItem(t, 1, closure);
	  Py_INCREF(pyfunc);
	  Py_INCREF(closure);

	  self->setFilterCallback(SoIntersectionFilterPythonCB, (void *) t);
    }

    void addIntersectionCallback(PyObject * pyfunc, PyObject * closure  = NULL) {
	  PyObject *t = PyTuple_New(2);
	  PyTuple_SetItem(t, 0, pyfunc);
	  PyTuple_SetItem(t, 1, closure);
	  Py_INCREF(pyfunc);
	  Py_INCREF(closure);

	  self->addIntersectionCallback(SoIntersectionPythonCB, (void *) t);
    }

    void removeIntersectionCallback(PyObject * pyfunc, PyObject * closure  = NULL) {
	  PyObject *t = PyTuple_New(2);
	  PyTuple_SetItem(t, 0, pyfunc);
	  PyTuple_SetItem(t, 1, closure);
	  Py_INCREF(pyfunc);
	  Py_INCREF(closure);

	  self->removeIntersectionCallback(SoIntersectionPythonCB, (void *) t);
    }
  }
#endif

private:
  SoIntersectionDetectionActionP * pimpl;
};

#endif // !COIN_SOINTERSECTIONDETECTIONACTION_H
