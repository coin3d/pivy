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

// $Id: SoGtkExaminerViewer.h,v 1.1 2002/03/12 22:15:13 tamer Exp $

#ifndef SOGTK_EXAMINERVIEWER_H
#define SOGTK_EXAMINERVIEWER_H

#include <Inventor/SbLinear.h>
#include <Inventor/Gtk/viewers/SoGtkFullViewer.h>

class SoSeparator;
class SoSwitch;
class SoTranslation;
class SoScale;

class SoGtkThumbWheel;

// *************************************************************************

class SOGTK_DLL_API SoGtkExaminerViewer : public SoGtkFullViewer {
  SOGTK_OBJECT_HEADER(SoGtkExaminerViewer, SoGtkFullViewer);
  

public:
  // swig - added SoGtkFullViewer:: and SoGtkViewer:: to right assignment
  SoGtkExaminerViewer(GtkWidget * parent = NULL,
                        const char * name = NULL,
                        SbBool embed = TRUE,
                        SoGtkFullViewer::BuildFlag flag = SoGtkFullViewer::BUILD_ALL,
                        SoGtkViewer::Type type = SoGtkViewer::BROWSER);
  ~SoGtkExaminerViewer();

  void setAnimationEnabled(const SbBool enable);
  SbBool isAnimationEnabled(void) const;

  void stopAnimating(void);
  SbBool isAnimating(void) const;

  void setFeedbackVisibility(const SbBool enable);
  SbBool isFeedbackVisible(void) const;

  void setFeedbackSize(const int size);
  int getFeedbackSize(void) const;

  virtual void setViewing(SbBool enable);
  virtual void setCamera(SoCamera * camera);
  virtual void setCursorEnabled(SbBool enable);

protected:
  SoGtkExaminerViewer(GtkWidget * parent,
                        const char * name,
                        SbBool embed,
                        SoGtkFullViewer::BuildFlag flag,
                        SoGtkViewer::Type type,
                        SbBool build);

  virtual void leftWheelMotion(float val);
  virtual void bottomWheelMotion(float val);
  virtual void rightWheelMotion(float val);

  virtual GtkWidget * makeSubPreferences(GtkWidget * parent);
  virtual void createViewerButtons(GtkWidget * parent, SbPList * buttonlist);

  virtual const char * getDefaultWidgetName(void) const;
  virtual const char * getDefaultTitle(void) const;
  virtual const char * getDefaultIconTitle(void) const;

  virtual void openViewerHelpCard(void);

  virtual SbBool processSoEvent(const SoEvent * const event);
  virtual void setSeekMode(SbBool enable);
  virtual void actualRedraw(void);

  virtual void afterRealizeHook(void);


private:
  void genericConstructor(void);
  void genericDestructor(void);

  void setGenericAnimationEnabled(const SbBool enable);
  void setGenericFeedbackSize(const int size);
  void actualGenericRedraw(void);

  void setMotion3OnCamera(SbBool enable);
  SbBool getMotion3OnCamera(void) const;

  float rotXWheelMotion(float value, float old);
  float rotYWheelMotion(float value, float old);

  void reorientCamera(const SbRotation & rotation);
  void spin(const SbVec2f & mousepos);
  void pan(const SbVec2f & mousepos, const SbVec2f & prevpos);
  void zoom(const float diffvalue);
  void zoomByCursor(const SbVec2f & mousepos, const SbVec2f & prevpos);

  SbVec2f lastmouseposition;
  SbPlane panningplane;

  SbBool spinanimating;
  SbBool spinanimatingallowed;
  SbVec2f lastspinposition;
  int spinsamplecounter;
  SbRotation spinincrement;
  class SbSphereSheetProjector * spinprojector;

  SbRotation spinRotation;

  SbBool axiscrossEnabled;
  int axiscrossSize;

  void drawAxisCross(void);
  static void drawArrow(void);

  struct { // tracking mouse movement in a log
    short size;
    short historysize;
    SbVec2s * position;
    SbTime * time;
  } log;

  // The Microsoft Visual C++ v6.0 compiler needs a name on this class
  // to be able to generate a constructor (which it wants to have for
  // running the the SbVec2s constructors). So don't try to be clever
  // and make it anonymous.
  struct Pointer {
    SbVec2s now, then;
  } pointer;

  SbBool button1down;
  SbBool button2down;
  SbBool button3down;
  SbBool controldown;

  void clearLog(void);
  void addToLog(const SbVec2s pos, const SbTime time);

  SbTime prevRedrawTime;

  SbBool motion3OnCamera;

  SbVec2s canvas;

  enum ViewerMode {
    IDLE,
    INTERACT,
    EXAMINE,
    DRAGGING,
    WAITING_FOR_SEEK,
    ZOOMING,
    WAITING_FOR_PAN,
    PANNING
  } mode;

  ViewerMode currentmode;
  void setMode(const ViewerMode mode);




//// FIXME!: merge the So*ExaminerViewer defines properly. 20020109 mortene.

#ifdef __COIN_SOQT__

private:
  QPixmap * orthopixmap, * perspectivepixmap;

  void constructor(SbBool buildNow);
  void visibilityCallback(SbBool visible);
  static void visibilityCB(void * data, SbBool visible);

  QTimer * spindetecttimer;

  void setCursorRepresentation(int mode);
  QCursor * defaultcursor;

  class QPushButton * cameratogglebutton;
  class QLabel * feedbacklabel1, * feedbacklabel2;
  SoQtThumbWheel * feedbackwheel;
  class QLineEdit * feedbackedit;
  void setEnableFeedbackControls(const SbBool flag);

private slots:

// preferences window:
  void spinAnimationToggled(bool);
  void feedbackVisibilityToggle(bool);
  void feedbackEditPressed(void);
  void feedbackWheelPressed(void);
  void feedbackSizeChanged(float val);
  void feedbackWheelReleased(void);

// viewer buttons row:
  void cameratoggleClicked(void);
#endif // ! __COIN_SOQT__


#ifdef __COIN_SOWIN__
protected:
  virtual LRESULT onCommand(HWND window, UINT message, WPARAM wparam, LPARAM lparam);
  virtual void buildViewerButtonsEx(HWND parent, int x, int y, int size);
  virtual void createPrefSheet(void);
  
private:
  void setCursorRepresentation(int mode);

  class SoWinExaminerViewerP * pimpl;
  friend class SoWinExaminerViewerP;
#endif // ! __COIN_SOWIN__


#ifdef __COIN_SOGTK__
protected:
  virtual void leftWheelStart(void);
  virtual void bottomWheelStart(void);

private:
  void constructor(const SbBool build);
  void setCursorRepresentation(int mode);

  // friends and family
  class SoGtkExaminerViewerP * pimpl;
  friend class SoGtkExaminerViewerP;
#endif // ! __COIN_SOGTK__

#ifdef __COIN_SOXT__
  virtual void leftWheelStart(void);
  virtual void bottomWheelStart(void);

  void camerabuttonClicked(void);
  static void camerabuttonCB(Widget, XtPointer, XtPointer);

  virtual void createPrefSheet(void);

  Widget createFramedSpinAnimPrefSheetGuts(Widget parent);
  Widget createSpinAnimPrefSheetGuts(Widget parent);
  Widget spinanimtoggle;
  void spinanimtoggled(void);
  static void spinanimtoggledCB(Widget, XtPointer, XtPointer);

  Widget createRotAxisPrefSheetGuts(Widget parent);
  Widget createFramedRotAxisPrefSheetGuts(Widget parent);
  Widget rotpointaxestoggle, rotaxesoverlaytoggle, axessizewheel, axessizefield;
  void rotpointtoggled(void);
  static void rotpointtoggledCB(Widget, XtPointer, XtPointer);
  void rotaxesoverlaytoggled(void);
  static void rotaxesoverlaytoggledCB(Widget, XtPointer, XtPointer);
  void axeswheelmoved(int ticks);
  static void axeswheelmovedCB(Widget, XtPointer, XtPointer);
  void axesfieldchanged(void);
  static void axesfieldchangedCB(Widget, XtPointer, XtPointer);

private:
  void constructor(const SbBool build);

  void setCursorRepresentation(int mode);

  Widget camerabutton;
  struct {
    Pixmap ortho, ortho_ins;
    Pixmap perspective, perspective_ins;
    Pixmap nocam, nocam_ins;
  } camerapixmaps;

  Widget * prefparts;
  int numprefparts;
#endif // ! __COIN_SOXT__
};

#endif // ! SOGTK_EXAMINERVIEWER_H
