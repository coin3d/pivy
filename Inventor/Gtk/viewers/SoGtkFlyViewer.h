/**************************************************************************
 *
 *  This file is part of the Coin GUI binding libraries.
 *  Copyright (C) 2000-2001 by Systems in Motion.  All rights reserved.
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

// Generated automatically from SoGuiFlyViewer.h.in by configure.
// $Id: SoGtkFlyViewer.h,v 1.1 2002/03/12 22:15:14 tamer Exp $

#ifndef SOGTK_FLYVIEWER_H
#define SOGTK_FLYVIEWER_H

#include <Inventor/Gtk/viewers/SoGtkConstrainedViewer.h>

// ************************************************************************

class SOGTK_DLL_API SoGtkFlyViewer : public SoGtkConstrainedViewer {
  SOGTK_OBJECT_HEADER(SoGtkFlyViewer, SoGtkConstrainedViewer);
  

public:
  // swig - added SoGtkFullViewer:: and SoGtkViewer:: to right assignment
  SoGtkFlyViewer(
    GtkWidget * parent = NULL,
    const char * name = NULL, 
    SbBool embed = TRUE, 
	SoGtkFullViewer::BuildFlag flag = SoGtkFullViewer::BUILD_ALL,
	SoGtkViewer::Type type = SoGtkViewer::BROWSER);
  ~SoGtkFlyViewer();

  virtual void setViewing(SbBool enable);
  virtual void viewAll(void);
  virtual void resetToHomePosition(void);
  virtual void setCamera(SoCamera * camera);
  virtual void setCursorEnabled(SbBool enable);
  virtual void setCameraType(SoType type);

protected:
  SoGtkFlyViewer(
    GtkWidget * parent,
    const char * const name, 
    SbBool embed, 
    SoGtkFullViewer::BuildFlag flag, 
    SoGtkViewer::Type type, 
    SbBool build);

  virtual const char * getDefaultWidgetName(void) const;
  virtual const char * getDefaultTitle(void) const;
  virtual const char * getDefaultIconTitle(void) const;

  virtual SbBool processSoEvent(const SoEvent * const event);
  virtual void setSeekMode(SbBool enable);
  virtual void actualRedraw(void);

  virtual void rightWheelMotion(float value);

  virtual void createPrefSheet(void);
  virtual void openViewerHelpCard(void);

  virtual void afterRealizeHook(void);

private:
  void constructor(SbBool build);
  class SoGtkFlyViewerP * pimpl;

}; // class SoGtkFlyViewer

// ************************************************************************

#endif // ! SOGTK_FLYVIEWER_H
