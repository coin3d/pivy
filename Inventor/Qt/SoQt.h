/**************************************************************************\
 *
 *  This file is part of the Coin family of 3D visualization libraries.
 *  Copyright (C) 1998-2003 by Systems in Motion.  All rights reserved.
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
 *  Systems in Motion, Abels gate 5, Teknobyen, 7030 Trondheim, NORWAY
 *  <URL:http://www.sim.no>, <mailto:support@sim.no>
 *
\**************************************************************************/

// src/Inventor/Qt/SoQt.h.  Generated from SoGui.h.in by configure.

#ifndef SOQT_H
#define SOQT_H

#include <Inventor/Qt/SoQtBasic.h>

// FIXME: use configure defines for the header files.
// 20020613 mortene.

#ifdef __COIN_SOQT__
#include <qobject.h>
#endif // __COIN_SOQT__
#ifdef __COIN_SOXT__
#include <X11/Intrinsic.h>
#include <Xm/Xm.h>
#endif // __COIN_SOXT__
#ifdef __COIN_SOGTK__
// Fetch stdlib.h, so NULL is defined before glib.h is (indirectly)
// included. Otherwise we get a compile error with KCC on some
// systems.
#include <stdlib.h>
#include <gtk/gtk.h>
class SoGtkComponent;
class SbPList;
#endif // __COIN_SOGTK__
#ifdef __COIN_SOWIN__
#include <windows.h>
#endif // __COIN_SOWIN__

#include <Inventor/SbBasic.h>
#include <Inventor/SbLinear.h>
#include <Inventor/SbString.h>
#include <Inventor/SoDB.h>
#include <Inventor/errors/SoDebugError.h>

// *************************************************************************

#ifdef __PIVY__
%{
/* FIXME: there is a major pitfall reg. this solution. neither
 *   Python nor Qt are thread safe! reconsider! 20030626 tamer.
 */
static void *Pivy_PythonInteractiveLoop(void *data) {
  PyRun_InteractiveLoop(stdin, "<stdin>");
}
%}
#endif

class SOQT_DLL_API SoQt
{

public:
  static QWidget * init(const char * appname, const char * classname = "SoQt");
  static QWidget * init(int & argc, char ** argv,
                       const char * appname, const char * classname = "SoQt");
  static void init(QWidget * toplevelwidget);

#ifdef __PIVY__
%extend {
  static void mainLoop(void) {
    PyRun_SimpleString("import sys");
    PyObject *d = PyModule_GetDict(PyImport_AddModule("__main__"));
    PyObject *result = PyRun_String("sys.argv[0]", Py_eval_input, d, d);
    /* if we are calling from within an interactive python interpreter
     * session spawn a new InteractiveLoop in a new thread. determined
     * by sys.argv[0] == ''. otherwise proceed as usual.
     */
    if (!strcmp(PyString_AsString(result), "")) {
      cc_thread *py_thread = cc_thread_construct(Pivy_PythonInteractiveLoop, NULL);
      SoQt::mainLoop();
      void *retval = NULL;
      cc_thread_join(py_thread, &retval);
      cc_thread_destruct(py_thread);
      exit(0);
    } else {
      Py_BEGIN_ALLOW_THREADS
      SoQt::mainLoop();
      Py_END_ALLOW_THREADS
    }
  }
}
#else
  static void mainLoop(void);
#endif
  static void exitMainLoop(void);
  static void done(void);

  static QWidget * getTopLevelWidget(void);
  static QWidget * getShellWidget(const QWidget * w);

  static void show(QWidget * const widget);
  static void hide(QWidget * const widget);

  static void setWidgetSize(QWidget * const widget, const SbVec2s size);
  static SbVec2s getWidgetSize(const QWidget * widget);

  static void createSimpleErrorDialog(QWidget * widget,
                                      const char * title,
                                      const char * string1,
                                      const char * string2 = NULL);

  static void getVersionInfo(int * major = NULL,
                             int * minor = NULL,
                             int * micro = NULL);
  static const char * getVersionString(void);

  enum FatalErrors {
    UNSPECIFIED_ERROR = 0,
    NO_OPENGL_CANVAS,
    INTERNAL_ASSERT
  };
  typedef void FatalErrorCB(const SbString errmsg, SoQt::FatalErrors errcode,
                            void * userdata);
  static FatalErrorCB * setFatalErrorHandler(SoQt::FatalErrorCB * cb,
                                             void * userdata);

  static SbBool isDebugLibrary(void);
  static SbBool isCompatible(unsigned int major, unsigned int minor);

  enum ABIType { DLL, LIB, UNKNOWN };
  static ABIType getABIType(void);

private:
  // Since the class consists solely of static functions, hide the
  // default constructor and the destructor so nobody can instantiate
  // it.
  SoQt(void);
  virtual ~SoQt();

  friend class SoGuiP;
  friend class SoQtP;


  // FIXME!: audit and remove as much as possible of the remaining
  // toolkit specific parts below. 20020117 mortene.

#ifdef __COIN_SOXT__
public:
  static void nextEvent(XtAppContext, XEvent *);
  static Boolean dispatchEvent(XEvent * event);
  static XtAppContext getAppContext(void);
  static Display * getDisplay(void);
  static XmString encodeString(const char * const str);
  static char * decodeString(XmString xstring);
  static void getPopupArgs(Display * display, int screen,
                           ArgList args, int * n);

  static void registerColormapLoad(Widget widget, Widget shell);
  static void addColormapToShell(Widget widget, Widget shell);
  static void removeColormapFromShell(Widget widget, Widget shell);

  static void addExtensionEventHandler(Widget widget,
                                       int eventType, XtEventHandler proc,
                                       XtPointer clientData);
  static void removeExtensionEventHandler(Widget widget,
                                          int eventType, XtEventHandler proc,
                                          XtPointer clientData);

protected:
  static void getExtensionEventHandler(XEvent * event, Widget & widget,
                                       XtEventHandler & proc,
                                       XtPointer & clientData);
#endif // __COIN_SOXT__

#ifdef __COIN_SOGTK__
public:
  friend class SoGtkComponent;
  enum SoGtkComponentAction { CREATION, DESTRUCTION, CHANGE };
  typedef void SoGtkComponentActionCallback(SoGtkComponent *, SoGtk::SoGtkComponentAction, void *);

  static void addComponentActionCallback(SoGtkComponentActionCallback *, void *);
  static void removeComponentActionCallback(SoGtkComponentActionCallback *, void *);

  static int getComponents(SbPList & components);

protected:
  static void invokeComponentActionCallbacks(SoGtkComponent * component,
                                             SoGtkComponentAction action);

  static gint componentCreation(SoGtkComponent * component);
  static gint componentDestruction(SoGtkComponent * component);
  static gint componentChange(SoGtkComponent * component);

private:
  static gint timerSensorCB(gpointer data);
  static gint idleSensorCB(gpointer data);
  static gint delaySensorCB(gpointer data);

  static GtkWidget * mainWidget;
  static SbPList * components;
  static SbPList * component_callbacks;
#endif // __COIN_SOGTK__
};

// *************************************************************************

#endif // ! SOQT_H
