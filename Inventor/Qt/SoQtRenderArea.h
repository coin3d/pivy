/**************************************************************************\
 *
 *  This file is part of the Coin family of 3D visualization libraries.
 *  Copyright (C) 1998-2002 by Systems in Motion.  All rights reserved.
 *
 *  This library is free software; you can redistribute it and / or
 *  modify it under the terms of the GNU General Public License
 *  version 2 as published by the Free Software Foundation.  See the
 *  file LICENSE.GPL at the root directory of this source distribution
 *  for more details.
 *
 *  If you desire to use this library in software that is incompatible
 *  with the GNU GPL, and / or you would like to take advantage of the
 *  additional benefits with regard to our support services, please
 *  contact Systems in Motion about acquiring a Coin Professional
 *  Edition License.  See <URL:http://www.coin3d.org> for more
 *  information.
 *
 *  Systems in Motion, Prof Brochs gate 6, 7030 Trondheim, NORWAY
 *  <URL:http://www.sim.no>, <mailto:support@sim.no>
 *
\**************************************************************************/

// src/Inventor/Qt/SoQtRenderArea.h.  Generated from SoGuiRenderArea.h.in by configure.

#ifndef SOQT_RENDERAREA_H
#define SOQT_RENDERAREA_H

#include <Inventor/SbColor.h>
#include <Inventor/SbViewportRegion.h>
#include <Inventor/actions/SoGLRenderAction.h>
#include <Inventor/SoSceneManager.h>

#include <Inventor/Qt/SoQtGLWidget.h>

class SbColor;
class SoNode;
class SoSelection;

class SoQtDevice;
// SoQtRenderAreaP is only used in the "friend class" statement in
// the class definition, so this shouldn't really be necessary. But
// the OSF1/cxx compiler complains if it's left out.
class SoQtRenderAreaP;

typedef SbBool SoQtRenderAreaEventCB(void * closure, QEvent * event);

// *************************************************************************

#ifdef __PIVY__
%{
static SbBool
SoQtRenderAreaEventPythonCB(void * closure, QEvent * event)
{
  PyObject *func, *arglist;
  PyObject *result, *qev;
  int ires = 0;

  qev = SWIG_NewPointerObj((void *) event, SWIGTYPE_p_QEvent, 1);

  /* the first item in the closure sequence is the python callback
   * function; the second is the supplied closure python object */
  func = PyTuple_GetItem((PyObject *)closure, 0);
  arglist = Py_BuildValue("OO", PyTuple_GetItem((PyObject *)closure, 1), qev);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
	printf("SoQtRenderAreaEventPythonCB(void * closure, QEvent * event) failed!\n");
  }
  else {
	ires = PyInt_AsLong(result);
  }

  Py_DECREF(arglist);
  Py_XDECREF(result);

  return ires;
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

class SOQT_DLL_API SoQtRenderArea : public SoQtGLWidget {
  SOQT_OBJECT_HEADER(SoQtRenderArea, SoQtGLWidget);

public:
  SoQtRenderArea(QWidget * parent = NULL,
                    const char * name = NULL,
                    SbBool embed = TRUE,
                    SbBool mouseInput = TRUE,
                    SbBool keyboardInput = TRUE);
  ~SoQtRenderArea();

  virtual void setSceneGraph(SoNode * scene);
  virtual SoNode * getSceneGraph(void);
  void setOverlaySceneGraph(SoNode * scene);
  SoNode * getOverlaySceneGraph(void);

  void setBackgroundColor(const SbColor & color);
  const SbColor & getBackgroundColor(void) const;
  void setBackgroundIndex(int idx);
  int getBackgroundIndex(void) const;
  void setOverlayBackgroundIndex(int idx);
  int getOverlayBackgroundIndex(void) const;
  void setColorMap(int start, int num, const SbColor * colors);
  void setOverlayColorMap(int start, int num, const SbColor * colors);
  void setViewportRegion(const SbViewportRegion & newRegion);
  const SbViewportRegion & getViewportRegion(void) const;
  void setTransparencyType(SoGLRenderAction::TransparencyType type);
  SoGLRenderAction::TransparencyType getTransparencyType(void) const;
  void setAntialiasing(SbBool smoothing, int numPasses);
  void getAntialiasing(SbBool & smoothing, int & numPasses) const;
  void setClearBeforeRender(SbBool enable, SbBool zbEnable = TRUE);
  SbBool isClearBeforeRender(void) const;
  SbBool isClearZBufferBeforeRender(void) const;
  void setClearBeforeOverlayRender(SbBool enable);
  SbBool isClearBeforeOverlayRender(void) const;
  void setAutoRedraw(SbBool enable);
  SbBool isAutoRedraw(void) const;
  void setRedrawPriority(uint32_t priority);
  uint32_t getRedrawPriority(void) const;
  static uint32_t getDefaultRedrawPriority(void);
  void render(void);
  void renderOverlay(void);
  void scheduleRedraw(void);
  void scheduleOverlayRedraw(void);
  void redrawOnSelectionChange(SoSelection * selection);
  void redrawOverlayOnSelectionChange(SoSelection * selection);
  void setEventCallback(SoQtRenderAreaEventCB * func, void * user = NULL);
#ifdef __PIVY__
  /* add python specific callback functions */
  %extend {
	void setPythonEventCallback(PyObject *pyfunc, PyObject *user = NULL) {
	  if (user == NULL) {
		Py_INCREF(Py_None);
		user = Py_None;
	  }
	  
	  PyObject *t = PyTuple_New(2);
	  PyTuple_SetItem(t, 0, pyfunc);
	  PyTuple_SetItem(t, 1, user);
	  Py_INCREF(pyfunc);
	  Py_INCREF(user);

	  self->setEventCallback(SoQtRenderAreaEventPythonCB, (void *) t);
	}
  }
#endif
  void setSceneManager(SoSceneManager * manager);
  SoSceneManager * getSceneManager(void) const;
  void setOverlaySceneManager(SoSceneManager * manager);
  SoSceneManager * getOverlaySceneManager(void) const;
  void setGLRenderAction(SoGLRenderAction * action);
  SoGLRenderAction * getGLRenderAction(void) const;
  void setOverlayGLRenderAction(SoGLRenderAction * action);
  SoGLRenderAction * getOverlayGLRenderAction(void) const;

  SbBool sendSoEvent(const SoEvent * event);

  void registerDevice(SoQtDevice * device);
  void unregisterDevice(SoQtDevice * device);


protected:
  SoQtRenderArea(QWidget * parent,
                    const char * name,
                    SbBool embed,
                    SbBool mouseInput,
                    SbBool keyboardInput,
                    SbBool build);

  virtual void redraw(void);
  virtual void actualRedraw(void);
  virtual void redrawOverlay(void);
  virtual void actualOverlayRedraw(void);

  virtual SbBool processSoEvent(const SoEvent * const event);
  virtual void processEvent(QEvent * event);
  virtual void initGraphic(void);
  virtual void initOverlayGraphic(void);
  virtual void sizeChanged(const SbVec2s & size);
  virtual void widgetChanged(QWidget * widget);
  virtual void afterRealizeHook(void);

  QWidget * buildWidget(QWidget * parent);

  virtual const char * getDefaultWidgetName(void) const;
  virtual const char * getDefaultTitle(void) const;
  virtual const char * getDefaultIconTitle(void) const;

  virtual SbBool glScheduleRedraw(void);

private:
  class SoQtRenderAreaP * pimpl;
#ifndef DOXYGEN_SKIP_THIS
  friend class SoQtRenderAreaP;
#endif // DOXYGEN_SKIP_THIS
};

// *************************************************************************

#endif // ! SOQT_RENDERAREA_H
