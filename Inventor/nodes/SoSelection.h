#ifndef COIN_SOSELECTION_H
#define COIN_SOSELECTION_H

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

#include <Inventor/nodes/SoSubNode.h>
#include <Inventor/nodes/SoSeparator.h>
#include <Inventor/fields/SoSFEnum.h>
#include <Inventor/lists/SoPathList.h>

class SoSelection;
class SoPath;
class SoPickedPoint;
class SoCallbackList;

typedef void SoSelectionPathCB(void * data, SoPath * path);
typedef void SoSelectionClassCB(void * data, SoSelection * sel);
typedef SoPath * SoSelectionPickCB(void * data, const SoPickedPoint * pick);

#ifdef __PIVY__
%{
static void
SoSelectionPathPythonCB(void * data, SoPath * path)
{
  PyObject *func, *arglist;
  PyObject *result, *pathCB;

  pathCB = SWIG_NewPointerObj((void *) path, SWIGTYPE_p_SoPath, 1);

  /* the first item in the data sequence is the python callback
   * function; the second is the supplied data python object */
  func = PyTuple_GetItem((PyObject *)data, 0);
  arglist = Py_BuildValue("OO", PyTuple_GetItem((PyObject *)data, 1), pathCB);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
	printf("SoSelectionPathPythonCB(void * data, SoPath * path) failed!\n");
  }

  Py_DECREF(arglist);
  Py_XDECREF(result);

  return /*void*/;
}

static void
SoSelectionClassPythonCB(void * data, SoSelection * sel)
{
  PyObject *func, *arglist;
  PyObject *result, *selCB;

  selCB = SWIG_NewPointerObj((void *) sel, SWIGTYPE_p_SoSelection, 1);

  /* the first item in the data sequence is the python callback
   * function; the second is the supplied data python object */
  func = PyTuple_GetItem((PyObject *)data, 0);
  arglist = Py_BuildValue("OO", PyTuple_GetItem((PyObject *)data, 1), selCB);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
	printf("SoSelectionClassPythonCB(void * data, SoSelection * sel) failed!\n");
  }

  Py_DECREF(arglist);
  Py_XDECREF(result);

  return /*void*/;
}

static SoPath *
SoSelectionPickPythonCB(void * data, const SoPickedPoint * pick)
{
  PyObject *func, *arglist;
  PyObject *result, *pickCB;
  SoPath *resultobj;

  pickCB = SWIG_NewPointerObj((void *) pick, SWIGTYPE_p_SoPickedPoint, 1);

  /* the first item in the data sequence is the python callback
   * function; the second is the supplied data python object */
  func = PyTuple_GetItem((PyObject *)data, 0);
  arglist = Py_BuildValue("OO", PyTuple_GetItem((PyObject *)data, 1), pickCB);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
	printf("SoSelectionPickPythonCB(void * data, const SoPickedPoint * pick) failed!\n");
  }
  else {
	SWIG_ConvertPtr(result, (void **) &resultobj, SWIGTYPE_p_SoPath, 1);
  }

  Py_DECREF(arglist);
  Py_XDECREF(result);

  return resultobj;
}
%}

%typemap(in) PyObject *pyfunc %{
  if (!PyCallable_Check($input)) {
	PyErr_SetString(PyExc_TypeError, "need a callable object!");
	return NULL;
  }
  $1 = $input;
%}

%rename(SoSelection_i) SoSelection::SoSelection(const int nChildren);

%feature("shadow") SoSelection::SoSelection %{
def __init__(self,*args):
   if len(args) == 1:
      self.this = apply(_pivy.new_SoSelection_i,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SoSelection,args)
   self.thisown = 1
%}

%rename(select_nod) SoSelection::select(SoNode *node);

%feature("shadow") SoSelection::select(const SoPath * path) %{
def select(*args):
   if isinstance(args[1], SoNode):
      return apply(_pivy.SoSelection_select_nod,args)
   return apply(_pivy.SoSelection_select,args)
%}

%rename(deselect_i) SoSelection::deselect(const int which);
%rename(deselect_nod) SoSelection::deselect(SoNode *node);

%feature("shadow") SoSelection::deselect(const SoPath * path) %{
def deselect(*args):
   if isinstance(args[1], SoNode):
      return apply(_pivy.SoSelection_deselect_nod,args)
   elif type(args[1]) == type(1):
      return apply(_pivy.SoSelection_deselect_i,args)
   return apply(_pivy.SoSelection_select,args)
%}

%rename(toggle_nod) SoSelection::toggle(SoNode * node);

%feature("shadow") SoSelection::toggle(const SoPath * path) %{
def toggle(*args):
   if isinstance(args[1], SoNode):
      return apply(_pivy.SoSelection_toggle_nod,args)
   return apply(_pivy.SoSelection_toggle,args)
%}

%rename(isSelected_nod) SoSelection::isSelected(SoNode * node) const;

%feature("shadow") isSelected(const SoPath * path) const %{
def isSelected(*args):
   if isinstance(args[1], SoNode):
      return apply(_pivy.SoSelection_isSelected_nod,args)
   return apply(_pivy.SoSelection_isSelected,args)
%}
#endif

class COIN_DLL_API SoSelection : public SoSeparator {
  typedef SoSeparator inherited;

  SO_NODE_HEADER(SoSelection);

public:
  static void initClass(void);
  SoSelection(void);

  enum Policy {
    SINGLE, TOGGLE, SHIFT
  };

  SoSFEnum policy;

  SoSelection(const int nChildren);

  void select(const SoPath * path);
  void select(SoNode *node);
  void deselect(const SoPath * path);
  void deselect(const int which);
  void deselect(SoNode * node);
  void toggle(const SoPath * path);
  void toggle(SoNode * node);
  SbBool isSelected(const SoPath * path) const;
  SbBool isSelected(SoNode * node) const;
  void deselectAll(void);
  int getNumSelected(void) const;
  const SoPathList * getList(void) const;
  SoPath * getPath(const int index) const;
  SoPath * operator[](const int i) const;
  void addSelectionCallback(SoSelectionPathCB * f, void * userData = NULL);
  void removeSelectionCallback(SoSelectionPathCB * f, void * userData = NULL);
  void addDeselectionCallback(SoSelectionPathCB * f, void * userData = NULL);
  void removeDeselectionCallback(SoSelectionPathCB * f,
                                 void * userData = NULL);
  void addStartCallback(SoSelectionClassCB * f, void * userData = NULL);
  void removeStartCallback(SoSelectionClassCB * f, void * userData = NULL);
  void addFinishCallback(SoSelectionClassCB * f, void * userData = NULL);
  void removeFinishCallback(SoSelectionClassCB * f, void * userData = NULL);
  void setPickFilterCallback(SoSelectionPickCB * f, void * userData = NULL,
                             const SbBool callOnlyIfSelectable = TRUE);
  void setPickMatching(const SbBool pickMatching);
  SbBool isPickMatching(void) const;
  SbBool getPickMatching(void) const;
  void addChangeCallback(SoSelectionClassCB * f, void * userData = NULL);
  void removeChangeCallback(SoSelectionClassCB * f, void * userData = NULL);

#ifdef __PIVY__
  /* add python specific callback functions */
  %extend {
	void addPythonSelectionCallback(PyObject *pyfunc, PyObject *userdata = NULL) {
	  if (userdata == NULL) {
		Py_INCREF(Py_None);
		userdata = Py_None;
	  }
	  
	  PyObject *t = PyTuple_New(2);
	  PyTuple_SetItem(t, 0, pyfunc);
	  PyTuple_SetItem(t, 1, userdata);
	  Py_INCREF(pyfunc);
	  Py_INCREF(userdata);

	  self->addSelectionCallback(SoSelectionPathPythonCB, (void *) t);
	}

	void removePythonSelectionCallback(PyObject *pyfunc, PyObject *userdata = NULL) {
	  if (userdata == NULL) {
		Py_INCREF(Py_None);
		userdata = Py_None;
	  }
	  
	  PyObject *t = PyTuple_New(2);
	  PyTuple_SetItem(t, 0, pyfunc);
	  PyTuple_SetItem(t, 1, userdata);

	  self->removeSelectionCallback(SoSelectionPathPythonCB, (void *) t);
	}

	void addPythonDeselectionCallback(PyObject *pyfunc, PyObject *userdata = NULL) {
	  if (userdata == NULL) {
		Py_INCREF(Py_None);
		userdata = Py_None;
	  }
	  
	  PyObject *t = PyTuple_New(2);
	  PyTuple_SetItem(t, 0, pyfunc);
	  PyTuple_SetItem(t, 1, userdata);
	  Py_INCREF(pyfunc);
	  Py_INCREF(userdata);

	  self->addDeselectionCallback(SoSelectionPathPythonCB, (void *) t);
	}

	void removePythonDeselectionCallback(PyObject *pyfunc, PyObject *userdata = NULL) {
	  if (userdata == NULL) {
		Py_INCREF(Py_None);
		userdata = Py_None;
	  }
	  
	  PyObject *t = PyTuple_New(2);
	  PyTuple_SetItem(t, 0, pyfunc);
	  PyTuple_SetItem(t, 1, userdata);

	  self->removeDeselectionCallback(SoSelectionPathPythonCB, (void *) t);
	}

	void addPythonStartCallback(PyObject *pyfunc, PyObject *userdata = NULL) {
	  if (userdata == NULL) {
		Py_INCREF(Py_None);
		userdata = Py_None;
	  }
	  
	  PyObject *t = PyTuple_New(2);
	  PyTuple_SetItem(t, 0, pyfunc);
	  PyTuple_SetItem(t, 1, userdata);
	  Py_INCREF(pyfunc);
	  Py_INCREF(userdata);

	  self->addStartCallback(SoSelectionClassPythonCB, (void *) t);
	}

	void removePythonStartCallback(PyObject *pyfunc, PyObject *userdata = NULL) {
	  if (userdata == NULL) {
		Py_INCREF(Py_None);
		userdata = Py_None;
	  }
	  
	  PyObject *t = PyTuple_New(2);
	  PyTuple_SetItem(t, 0, pyfunc);
	  PyTuple_SetItem(t, 1, userdata);

	  self->removeStartCallback(SoSelectionClassPythonCB, (void *) t);
	}

	void addPythonFinishCallback(PyObject *pyfunc, PyObject *userdata = NULL) {
	  if (userdata == NULL) {
		Py_INCREF(Py_None);
		userdata = Py_None;
	  }
	  
	  PyObject *t = PyTuple_New(2);
	  PyTuple_SetItem(t, 0, pyfunc);
	  PyTuple_SetItem(t, 1, userdata);
	  Py_INCREF(pyfunc);
	  Py_INCREF(userdata);

	  self->addFinishCallback(SoSelectionClassPythonCB, (void *) t);
	}

	void removePythonFinishCallback(PyObject *pyfunc, PyObject *userdata = NULL) {
	  if (userdata == NULL) {
		Py_INCREF(Py_None);
		userdata = Py_None;
	  }
	  
	  PyObject *t = PyTuple_New(2);
	  PyTuple_SetItem(t, 0, pyfunc);
	  PyTuple_SetItem(t, 1, userdata);

	  self->removeFinishCallback(SoSelectionClassPythonCB, (void *) t);
	}

	void setPythonPickFilterCallback(PyObject *pyfunc, PyObject *userdata = NULL, int callOnlyIfSelectable = 1) {
	  if (userdata == NULL) {
		Py_INCREF(Py_None);
		userdata = Py_None;
	  }
	  
	  PyObject *t = PyTuple_New(2);
	  PyTuple_SetItem(t, 0, pyfunc);
	  PyTuple_SetItem(t, 1, userdata);
	  Py_INCREF(pyfunc);
	  Py_INCREF(userdata);

	  self->setPickFilterCallback(SoSelectionPickPythonCB, (void *) t, callOnlyIfSelectable);
	}

	void addPythonChangeCallback(PyObject *pyfunc, PyObject *userdata = NULL) {
	  if (userdata == NULL) {
		Py_INCREF(Py_None);
		userdata = Py_None;
	  }
	  
	  PyObject *t = PyTuple_New(2);
	  PyTuple_SetItem(t, 0, pyfunc);
	  PyTuple_SetItem(t, 1, userdata);
	  Py_INCREF(pyfunc);
	  Py_INCREF(userdata);

	  self->addChangeCallback(SoSelectionClassPythonCB, (void *) t);
	}

	void removePythonChangeCallback(PyObject *pyfunc, PyObject *userdata = NULL) {
	  if (userdata == NULL) {
		Py_INCREF(Py_None);
		userdata = Py_None;
	  }
	  
	  PyObject *t = PyTuple_New(2);
	  PyTuple_SetItem(t, 0, pyfunc);
	  PyTuple_SetItem(t, 1, userdata);
	  Py_INCREF(pyfunc);
	  Py_INCREF(userdata);

	  self->removeChangeCallback(SoSelectionClassPythonCB, (void *) t);
	}
  }
#endif

protected:
  virtual ~SoSelection();

  void invokeSelectionPolicy(SoPath *path, SbBool shiftDown);
  void performSingleSelection(SoPath *path);
  void performToggleSelection(SoPath *path);
  SoPath * copyFromThis(const SoPath * path) const;
  void addPath(SoPath *path);
  void removePath(const int which);
  int findPath(const SoPath *path) const;

  virtual void handleEvent(SoHandleEventAction * action);

protected: // unfortunately only protected in OIV

  SoPathList selectionList;

  SoCallbackList *selCBList;
  SoCallbackList *deselCBList;
  SoCallbackList *startCBList;
  SoCallbackList *finishCBList;

  SoSelectionPickCB *pickCBFunc;
  void *pickCBData;
  SbBool callPickCBOnlyIfSelectable;

  SoCallbackList *changeCBList;

  SoPath *mouseDownPickPath;
  SbBool pickMatching;

private:
  void init();
  SoPath *searchNode(SoNode * node) const;
  SoPath *getSelectionPath(SoHandleEventAction *action,
                           SbBool &ignorepick, SbBool &haltaction);
};

#endif // !COIN_SOSELECTION_H
