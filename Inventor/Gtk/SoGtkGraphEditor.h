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

// $Id: SoGtkGraphEditor.h,v 1.1 2002/03/12 22:15:13 tamer Exp $

#ifndef SOGTK_GRAPHEDITOR_H
#define SOGTK_GRAPHEDITOR_H

#include <Inventor/Gtk/SoGtkComponent.h>

class SoNode;
class SoField;

// *************************************************************************

class SOGTK_DLL_API SoGtkGraphEditor : public SoGtkComponent {
  SOGTK_OBJECT_HEADER(SoGtkGraphEditor, SoGtkComponent);

public:
  enum BuildFlag {
    MENUBAR =       0x01,
    GRAPHEDITOR =   0x02,
    STATUSBAR =     0x04,
    EVERYTHING =    0x07
  };

  // swig
  SoGtkGraphEditor(GtkWidget * const parent = NULL,
                   const char * const name = NULL,
                   const SbBool embed = TRUE,
                   const int parts = EVERYTHING);

/*   SoGtkGraphEditor(GtkWidget * const parent = (GtkWidget *) NULL, */
/*                    const char * const name = (char *) NULL, */
/*                    const SbBool embed = TRUE, */
/*                    const int parts = EVERYTHING); */
  ~SoGtkGraphEditor(void);

  virtual void setSceneGraph(SoNode * root);
  SoNode * getSceneGraph(void) const;

protected:
  SoGtkGraphEditor(GtkWidget * const parent, const char * const name,
                   const SbBool embed, const int parts, const SbBool build);

  GtkWidget * buildWidget(GtkWidget * parent);
  virtual GtkWidget * buildMenuBarWidget(GtkWidget * parent);
  virtual GtkWidget * buildGraphEditorWidget(GtkWidget * parent);
  virtual GtkWidget * buildStatusBarWidget(GtkWidget * parent);

  virtual void sizeChanged(const SbVec2s & size);

  virtual void buildSceneGraphTree(void);
  virtual void clearSceneGraphTree(void);

  virtual void saveSceneGraph(void);

  virtual void setStatusMessage(const char * message);

  virtual void nodeSelection(GtkWidget * item, SoNode * node);
  virtual void fieldSelection(GtkWidget * item, SoNode * node, SoField * field);

  virtual const char * getDefaultWidgetName(void) const;
  virtual const char * getDefaultTitle(void) const;
  virtual const char * getDefaultIconTitle(void) const;

private:
  void constructor(const SbBool build, const int parts);

  static void saveCB(GtkObject * obj, gpointer closure);
  static void closeCB(GtkObject * obj, gpointer closure);
  static void selectionCB(GtkObject * obj, gpointer closure);

  GtkWidget * buildSubGraph(GtkWidget * parent, SoNode * node);

  SoNode * scenegraph;

  int buildflags;
  GtkWidget * editorbase;
  GtkWidget * menubar;
  GtkWidget * grapheditor;
  GtkWidget * graphroot;
  GtkWidget * statusbar;
  GtkWidget * statusmessage;

  GtkAdjustment * vertical;
  GtkAdjustment * horizontal;

}; // class SoGtkGraphEditor

// *************************************************************************

#endif // ! SOGTK_H
