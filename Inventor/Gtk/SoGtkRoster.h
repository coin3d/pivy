/**************************************************************************
 *
 *  This file is part of the Coin SoGtk GUI binding library.
 *  Copyright (C) 2000 by Systems in Motion.  All rights reserved.
 *
 *  This library is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU Lesser General Public License
 *  version 2.1 as published by the Free Software Foundation.  See the
 *  file LICENSE.LGPL at the root directory of the distribution for
 *  more details.
 *
 *  If you want to use Coin SoGtk for applications not compatible with the
 *  LGPL, please contact SIM to acquire a Professional Edition License.
 *
 *  Systems in Motion, Prof Brochs gate 6, N-7030 Trondheim, NORWAY
 *  http://www.sim.no/ support@sim.no Voice: +47 22114160 Fax: +47 22207097
 *
 **************************************************************************/

// $Id: SoGtkRoster.h,v 1.1 2002/03/12 22:15:13 tamer Exp $

#ifndef SOGTK_ROSTER_H
#define SOGTK_ROSTER_H

#include <Inventor/Gtk/SoGtk.h>
#include <Inventor/Gtk/SoGtkComponent.h>

// *************************************************************************

class SOGTK_DLL_API SoGtkRoster : public SoGtkComponent {
  SOGTK_OBJECT_HEADER(SoGtkRoster, SoGtkComponent);

public:
  enum BuildFlags {
    MENUBAR = 0x01,
    ROSTERLIST = 0x02,
    STATUSBAR = 0x04,
    BUILD_ALL = 0x07
  };

  // swig
  SoGtkRoster(
    GtkWidget * parent = NULL,
    const char * const name = NULL,
    const SbBool embed = TRUE,
    const int flags = BUILD_ALL);

/*   SoGtkRoster( */
/*     GtkWidget * parent = (GtkWidget *) NULL, */
/*     const char * const name = (char *) NULL, */
/*     const SbBool embed = TRUE, */
/*     const int flags = BUILD_ALL); */
  ~SoGtkRoster(void);

protected:
  SoGtkRoster(GtkWidget * parent, const char * const name,
    const SbBool embed, const int flags, const SbBool build);

  GtkWidget * buildWidget(GtkWidget * parent);
  virtual GtkWidget * buildMenuBarWidget(GtkWidget * parent);
  virtual GtkWidget * buildRosterListWidget(GtkWidget * parent);
  virtual GtkWidget * buildStatusBarWidget(GtkWidget * parent);

  virtual void sizeChanged(const SbVec2s & size);

  virtual void componentCreated(SoGtkComponent * component);
  virtual void componentDestroyed(SoGtkComponent * component);
  virtual void componentChanged(SoGtkComponent * component);

  void buildRosterList(void);

  virtual const char * getDefaultWidgetName(void) const;
  virtual const char * getDefaultTitle(void) const;
  virtual const char * getDefaultIconTitle(void) const;

private:
  void constructor(const SbBool build);

  int buildflags;
  GtkAdjustment * horizontal;
  GtkAdjustment * vertical;
  GtkWidget * rosterbase;
  GtkWidget * menubar;
  GtkWidget * rosterlist;
  GtkWidget * statusbar;
  GtkWidget * listwidget;

  static void componentActionCB(SoGtkComponent * component,
    SoGtk::SoGtkComponentAction action, void * closure);

}; // class SoGtkRoster

// *************************************************************************

#endif // ! SOGTK_ROSTER_H
