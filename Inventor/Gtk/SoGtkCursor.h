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

#ifndef SOGTK_CURSOR_H
#define SOGTK_CURSOR_H

#include <Inventor/SbLinear.h>
#include <Inventor/Gtk/SoGtkBasic.h>

class SOGTK_DLL_API SoGtkCursor {
public:
  // swig
  typedef struct {
    SbVec2s dim;
    SbVec2s hotspot;
    unsigned char * bitmap;
    unsigned char * mask;
  } CustomCursor;

/*   struct CustomCursor { */
/*     SbVec2s dim; */
/*     SbVec2s hotspot; */
/*     unsigned char * bitmap; */
/*     unsigned char * mask; */
/*   }; */

  // FIXME: add more default shapes. 20011119 pederb.
  enum Shape {
    CUSTOM_BITMAP = -1,
    DEFAULT = 0,
    BUSY,
    CROSSHAIR,
    UPARROW
  };
  
  SoGtkCursor(void);
  SoGtkCursor(const Shape shape);
  // swig
  SoGtkCursor(const SoGtkCursor::CustomCursor * cc);
/*   SoGtkCursor(const CustomCursor * cc); */
  ~SoGtkCursor();

  Shape getShape(void) const;
  void setShape(const Shape shape);

  // swig
  const SoGtkCursor::CustomCursor & getCustomCursor(void) const;
/*   const CustomCursor & getCustomCursor(void) const; */

  static const SoGtkCursor & getZoomCursor(void);
  static const SoGtkCursor & getPanCursor(void);
  static const SoGtkCursor & getRotateCursor(void);
  static const SoGtkCursor & getBlankCursor(void);
  
private:
  // swig
  void commonConstructor(const Shape shape, const SoGtkCursor::CustomCursor * cc);
/*   void commonConstructor(const Shape shape, const CustomCursor * cc); */

  Shape shape;
  // swig
  SoGtkCursor::CustomCursor * cc;
/*   CustomCursor * cc; */
};

#endif // ! SOGTK_CURSOR_H
