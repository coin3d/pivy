/**************************************************************************
 *
 *  This file is part of the Coin GUI binding libraries.
 *  Copyright (C) 2000 by Systems in Motion.  All rights reserved.
 *
 *  The libraries this file is part of is free software; you can
 *  redistribute them and/or modify them under the terms of the GNU
 *  Lesser General Public License version 2.1 as published by the
 *  Free Software Foundation.  See the file LICENSE.LGPL at the root
 *  directory of the distribution for all the details.
 *
 *  If you want to use the Coin GUI binding libraries for applications
 *  not compatible with the LGPL, contact SIM about acquiring a
 *  Professional Edition License.
 *
 *  Systems in Motion, Prof Brochs gate 6, N-7030 Trondheim, NORWAY
 *  http://www.sim.no/ support@sim.no Voice: +47 22114160 Fax: +47 22207097
 *
 **************************************************************************/

// Generated automatically from SoGuiRenderArea.h.in by configure.
// $Id: SoGtkRenderArea.h,v 1.1 2002/04/01 06:20:16 tamer Exp $

#ifndef SOGTK_RENDERAREA_H
#define SOGTK_RENDERAREA_H

#include <Inventor/SbColor.h>
#include <Inventor/SbViewportRegion.h>
#include <Inventor/actions/SoGLRenderAction.h>
#include <Inventor/SoSceneManager.h>

#include <Inventor/Gtk/SoGtkGLWidget.h>

class SbColor;
class SoNode;
class SoSelection;

class SoGtkDevice;

typedef SbBool SoGtkRenderAreaEventCB(void * closure, GdkEvent * event);

#ifdef __PIVY__
%{
static SbBool
SoGtkRenderAreaEventPythonCB(void * closure, GdkEvent * event)
{
  PyObject *func, *arglist;
  PyObject *result, *gdkev;
  int ires = 0;

  gdkev = SWIG_NewPointerObj((void *) event, SWIGTYPE_p_GdkEvent, 1);

  /* the first item in the closure sequence is the python callback
   * function; the second is the supplied closure python object */
  func = PyTuple_GetItem((PyObject *)closure, 0);
  arglist = Py_BuildValue("OO", PyTuple_GetItem((PyObject *)closure, 1), gdkev);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
	printf("SoGtkRenderAreaEventPythonCB(void * closure, GdkEvent * event) failed!\n");
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

// *************************************************************************

class SOGTK_DLL_API SoGtkRenderArea : public SoGtkGLWidget {
  SOGTK_OBJECT_HEADER(SoGtkRenderArea, SoGtkGLWidget);
  

public:
  SoGtkRenderArea(
    GtkWidget * parent = NULL,
    const char * name = NULL,
    SbBool embed = TRUE,
    SbBool mouseInput = TRUE,
    SbBool keyboardInput = TRUE);
  ~SoGtkRenderArea(void);

  virtual void setSceneGraph(SoNode * scene);
  virtual SoNode * getSceneGraph(void);
  void setOverlaySceneGraph(SoNode * scene);
  SoNode * getOverlaySceneGraph(void);

  void registerDevice(SoGtkDevice * device);
  void unregisterDevice(SoGtkDevice * device);
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
  void setEventCallback(SoGtkRenderAreaEventCB * func, void * user = NULL);

#ifdef __PIVY__
  /* add python specific callback functions */
  %addmethods {
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

	  self->setEventCallback(SoGtkRenderAreaEventPythonCB, (void *) t);
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

protected:
  SoGtkRenderArea(
    GtkWidget * parent,
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
  virtual void processEvent(GdkEvent * event);
  virtual void initGraphic(void);
  virtual void initOverlayGraphic(void);
  virtual void sizeChanged(const SbVec2s & size);
  virtual void widgetChanged(GtkWidget * widget);
  virtual void afterRealizeHook(void);

  GtkWidget * buildWidget(GtkWidget * parent);

  virtual const char * getDefaultWidgetName(void) const;
  virtual const char * getDefaultTitle(void) const;
  virtual const char * getDefaultIconTitle(void) const;

  virtual SbBool glScheduleRedraw(void);

  SbBool invokeAppCB(GdkEvent * event);

  const SoEvent * getSoEvent(GdkEvent * event);

  SbPList * deviceList;

  SoGtkRenderAreaEventCB * appEventHandler;
  void * appEventHandlerData;

private:
  friend class SoGtkRenderAreaP;
  class SoGtkRenderAreaP * priv;

  void constructor(SbBool mouseInput, SbBool keyboardInput, SbBool build);
  static void renderCB(void * user, SoSceneManager * manager);
  static void selection_redraw_cb(void * data, SoSelection * sel);
  void setDevicesWindowSize(const SbVec2s size);
}; // class SoGtkRenderArea

// *************************************************************************

#endif // ! SOGTK_RENDERAREA_H
