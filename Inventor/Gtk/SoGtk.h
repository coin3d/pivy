/**************************************************************************
 *
 *  This file is part of the Coin GUI binding libraries.
 *  Copyright (C) 1998-2001 by Systems in Motion.  All rights reserved.
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

#ifndef SOGTK_H
#define SOGTK_H

#include <Inventor/Gtk/SoGtkBasic.h>

#ifdef __COIN_SOQT__
#include <qevent.h>
#include <qobject.h>
#endif // __COIN_SOQT__
#ifdef __COIN_SOXT__
#include <X11/Intrinsic.h>
#include <Xm/Xm.h>
#endif // __COIN_SOXT__
#ifdef __COIN_SOGTK__
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
%ignore SoGtk::init(int argc, char ** argv, const char * appname, const char * classname = "SoGtk");
%ignore SoGtk::init(GtkWidget * toplevelwidget);
#endif

class SOGTK_DLL_API SoGtk
#ifdef __COIN_SOQT__
  : public QObject
#endif // __COIN_SOQT__
{
  

public:
  static GtkWidget * init(const char * appname, const char * classname = "SoGtk")
  {
    SOGTK_SANITY_CHECK(GtkWidget * retval = SoGtk::internal_init(appname, classname));
    return retval;
  }

  static GtkWidget * init(int argc, char ** argv,
                       const char * appname, const char * classname = "SoGtk")
  {
    SOGTK_SANITY_CHECK(GtkWidget * retval = SoGtk::internal_init(argc, argv, appname, classname));
    return retval;
  }

  static void init(GtkWidget * toplevelwidget) { SOGTK_SANITY_CHECK(SoGtk::internal_init(toplevelwidget)); }

  static void mainLoop(void);
  static void exitMainLoop(void);

  static GtkWidget * getTopLevelWidget(void);
  static GtkWidget * getShellWidget(const GtkWidget * w);

  static void show(GtkWidget * const widget);
  static void hide(GtkWidget * const widget);

  static void setWidgetSize(GtkWidget * const widget, const SbVec2s size);
  static SbVec2s getWidgetSize(const GtkWidget * widget);

  static void createSimpleErrorDialog(GtkWidget * widget,
                                      const char * dialogTitle,
                                      const char * errorStr1,
                                      const char * errorStr2 = NULL);

  static void getVersionInfo(int * major = NULL,
                             int * minor = NULL,
                             int * micro = NULL);
  static const char * getVersionString(void);

  enum FatalErrors {
    NO_OPENGL_CANVAS = 0,
    INTERNAL_ASSERT,
    UNSPECIFIED_ERROR
  };
  typedef void FatalErrorCB(const SbString errmsg, SoGtk::FatalErrors errcode,
                            void * userdata);
  static FatalErrorCB * setFatalErrorHandler(SoGtk::FatalErrorCB * cb,
                                             void * userdata);

protected:
  static SbBool isDebugLibrary(void);
  static SbBool isCompatible(unsigned int major, unsigned int minor);
  static SoGtkABIType getABIType(void);
  static void abort(SoGtkABIError error);

private:
  // Since the class consists solely of static functions, hide the
  // default constructor and the destructor so nobody can instantiate
  // it.
  SoGtk(void);
  ~SoGtk();
  friend class SoGtkP; // SoQtP needs this to set up an object for the slots.

  static void sensorQueueChanged(void * cbdata);

  static GtkWidget * internal_init(const char * appname, const char * classname);
  static GtkWidget * internal_init(int & argc, char ** argv,
                                const char * appname, const char * classname);
  static void internal_init(GtkWidget * toplevelwidget);


/// FIXME!: merge the remaining toolkit specific parts properly. 20020117 mortene. ////

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

  static void selectBestVisual(Display * dpy, Visual * & visual,
                               Colormap & cmap, int & depth);

  static const char * getAppName(void);
  static const char * getAppClass(void);

protected:
  static void getExtensionEventHandler(XEvent * event, Widget & widget,
                                       XtEventHandler & proc,
                                       XtPointer & clientData);
#endif // __COIN_SOXT__

#ifdef __COIN_SOWIN__
public:
  static BOOL dispatchEvent(MSG * msg);
  static SbBool nextEvent(int appContext, MSG * msg);
  static void setInstance(HINSTANCE instance);
  static HINSTANCE getInstance(void);
  static void errorHandlerCB(const class SoError * error, void * data);
  static void doIdleTasks(void);

protected:
  friend class SoWinP;

  static void registerWindowClass(const char * const className);
  static void unRegisterWindowClass(const char * const className);

  static HWND createWindow(char * title, char * className,
                           SIZE size, HWND parent = NULL, HMENU menu = NULL);

  static LRESULT CALLBACK eventHandler(HWND window, UINT message,
                                       WPARAM wparam, LPARAM lparam);

#endif // __COIN_SOWIN__

#ifdef __COIN_SOQT__
public:
  enum CustomEventId { SPACEBALL_EVENT = QEvent::User };
  static class QApplication * getApplication(void);

protected:
  bool eventFilter(QObject *, QEvent *);

private slots:
  void slot_timedOutSensor(void);
  void slot_idleSensor(void);
  void slot_delaytimeoutSensor(void);
#endif // __COIN_SOQT__

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

#endif // ! SOGTK_H
