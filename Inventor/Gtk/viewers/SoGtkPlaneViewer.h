/**************************************************************************
 *
 *  This file is part of the Coin SoGtk GUI binding library.
 *  Copyright (C) 1998-2000 by Systems in Motion.  All rights reserved.
 *
 *  This library is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU Lesser General Public License version
 *  2.1 as published by the Free Software Foundation.  See the file
 *  LICENSE.LGPL at the root directory of the distribution for all the
 *  details.
 *
 *  If you want to use Coin SoGtk for applications not compatible with the
 *  LGPL, please contact SIM to acquire a Professional Edition License.
 *
 *  Systems in Motion, Prof Brochs gate 6, N-7030 Trondheim, NORWAY
 *  http://www.sim.no/ support@sim.no Voice: +47 22114160 Fax: +47 22207097
 *
 **************************************************************************/

// $Id: SoGtkPlaneViewer.h,v 1.1 2002/03/12 22:15:14 tamer Exp $

#ifndef SOGTK_PLANEVIEWER_H
#define SOGTK_PLANEVIEWER_H

class SbPlaneProjector;
class SoAnyPlaneViewer;

#include <Inventor/Gtk/viewers/SoGtkFullViewer.h>

// ************************************************************************

class SOGTK_DLL_API SoGtkPlaneViewer : public SoGtkFullViewer {
  SOGTK_OBJECT_HEADER(SoGtkPlaneViewer, SoGtkFullViewer);
  

public:
  // swig - added SoGtkFullViewer:: and SoGtkViewer:: to right assignment
  SoGtkPlaneViewer(GtkWidget * parent = NULL,
                     const char * const name = NULL, 
                     SbBool embed = TRUE, 
				     SoGtkFullViewer::BuildFlag flag = SoGtkFullViewer::BUILD_ALL,
				     SoGtkViewer::Type type = SoGtkViewer::BROWSER);
  ~SoGtkPlaneViewer();

  virtual void setViewing(SbBool enable);
  virtual void setCamera(SoCamera * camera);
  virtual void setCursorEnabled(SbBool enable);

protected:
  SoGtkPlaneViewer(GtkWidget * parent,
                     const char * const name, 
                     SbBool embed, 
                     SoGtkFullViewer::BuildFlag flag, 
                     SoGtkViewer::Type type, 
                     SbBool build);

  GtkWidget * buildWidget(GtkWidget * parent);

  virtual const char * getDefaultWidgetName(void) const;
  virtual const char * getDefaultTitle(void) const;
  virtual const char * getDefaultIconTitle(void) const;

  virtual SbBool processSoEvent(const SoEvent * const event);
  virtual void processEvent(GdkEvent * event);
  virtual void setSeekMode(SbBool enable);
  virtual void actualRedraw(void);

  virtual void bottomWheelMotion(float value);
  virtual void leftWheelMotion(float value);
  virtual void rightWheelMotion(float value);

  virtual void createPrefSheet(void);

  virtual void createViewerButtons(GtkWidget * parent, SbPList * buttons);
  virtual void openViewerHelpCard(void);

private:
  void commonConstructor(void);

  void translateX(const float delta) const;
  void translateY(const float delta) const;
  void rotateZ(const float angle) const;

  void viewPlaneX(void) const;
  void viewPlaneY(void) const;
  void viewPlaneZ(void) const;

  void zoom(const float difference) const;

  void setCanvasSize(const SbVec2s size);
  void setPointerLocation(const SbVec2s location);
  int getPointerXMotion(void) const;
  int getPointerYMotion(void) const;
  float getPointerOrigoAngle(void) const;
  float getPointerOrigoMotionAngle(void) const;

  void drawRotateGraphics(void) const;

  enum PlaneViewerMode {
    IDLE_MODE,

    DOLLY_MODE,
    TRANSLATE_MODE,

    ROTZ_WAIT_MODE,
    ROTZ_MODE,

    SEEK_WAIT_MODE,
    SEEK_MODE
  } mode;

  struct pointerdata {
    SbVec2s now;
    SbVec2s then;
  } pointer;
  SbVec2s canvas;

  SbBool controldown;
  SbBool button1down;
  SbBool button2down;
  SbBool button3down;


//// FIXME!: merge the So*PlaneViewer definitions. 20020111 mortene. ////

#ifdef __COIN_SOQT__

private:
  void constructor(SbBool buildNow);

  void setModeFromState(unsigned int state);
  void setMode(PlaneViewerMode mode);

  SbVec2f prevMousePosition;

  SbPlaneProjector * projector;

  struct {
    class QPushButton * x, * y, * z;
    class QPushButton * camera;
  } buttons;

  struct {
    class QPixmap * orthogonal, * perspective;
  } pixmaps;

  static void visibilityCB(void * data, SbBool visible);

private slots:
  void xClicked(void);
  void yClicked(void);
  void zClicked(void);
  void cameraToggleClicked(void);

#endif // ! __COIN_SOQT__


#ifdef __COIN_SOXT__
private:
  void constructor(SbBool build);

  static struct SoXtViewerButton SoXtPlaneViewerButtons[];
  struct SoXtViewerButton * buttons;
  int findButton(Widget button) const;
  
  static void buttonCB(Widget, XtPointer, XtPointer);

  Widget prefshell, prefsheet, * prefparts;
  int numprefparts;

  struct {
    Pixmap ortho, ortho_ins;
    Pixmap perspective, perspective_ins;
  } pixmaps;

#endif // ! __COIN_SOXT__

#ifdef __COIN_SOGTK__
private:
  void constructor(const SbBool build);
  void setCursorRepresentation(int mode);

  // friends and family
  class SoGtkPlaneViewerP * pimpl;
  friend class SoGtkPlaneViewerP;
#endif // ! __COIN_SOGTK__

#ifdef __COIN_SOWIN__
protected:
  virtual LRESULT onCommand(HWND window,UINT message,
                            WPARAM wparam, LPARAM lparam);
  virtual void buildViewerButtonsEx(HWND parent, int x, int y, int size);  

private:
  friend class SoWinPlaneViewerP;
  class SoWinPlaneViewerP * pimpl;
#endif // ! __COIN_SOWIN__

};

#endif // ! SOGTK_PLANEVIEWER_H
