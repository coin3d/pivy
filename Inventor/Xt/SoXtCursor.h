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

#ifndef SOXT_CURSOR_H
#define SOXT_CURSOR_H

#include <Inventor/SbLinear.h>
#include <Inventor/Xt/SoXtBasic.h>

#ifdef __PIVY__
%rename(SoXtCursor_sha) SoXtCursor::SoXtCursor(const Shape shape);
%rename(SoXtCursor_cc) SoXtCursor::SoXtCursor(const SoXtCursor::CustomCursor * cc);

%feature("shadow") SoXtCursor::SoXtCursor %{
def __init__(self,*args):
   if len(args) == 1:
      if isinstance(args[0], CustomCursor):
         self.this = apply(_pivy.new_SoXtCursor_cc,args)
         self.thisown = 1
         return
      else:
         self.this = apply(_pivy.new_SoXtCursor_sha,args)
         self.thisown = 1
         return
   self.this = apply(_pivy.new_SoXtCursor,args)
   self.thisown = 1
%}
#endif

class SOXT_DLL_API SoXtCursor {
public:
#ifdef __PIVY__
  typedef struct CustomCursor CustomCursor;
#endif
  struct CustomCursor {
    SbVec2s dim;
    SbVec2s hotspot;
    unsigned char * bitmap;
    unsigned char * mask;
  };


  // FIXME: add more default shapes. 20011119 pederb.
  enum Shape {
    CUSTOM_BITMAP = -1,
    DEFAULT = 0,
    BUSY,
    CROSSHAIR,
    UPARROW
  };
  
  SoXtCursor(void);
  SoXtCursor(const Shape shape);
#ifdef __PIVY__
  SoXtCursor(const SoXtCursor::CustomCursor * cc);
#else
  SoXtCursor(const CustomCursor * cc);
#endif
  SoXtCursor(const SoXtCursor & cursor);
  ~SoXtCursor();

  SoXtCursor & operator=(const SoXtCursor & c);

  Shape getShape(void) const;
  void setShape(const Shape shape);

#ifdef __PIVY__
  const SoXtCursor::CustomCursor & getCustomCursor(void) const;
#else
  const CustomCursor & getCustomCursor(void) const;
#endif

  static const SoXtCursor & getZoomCursor(void);
  static const SoXtCursor & getPanCursor(void);
  static const SoXtCursor & getRotateCursor(void);
  static const SoXtCursor & getBlankCursor(void);
  
private:
  void commonConstructor(const Shape shape, const CustomCursor * cc);

  Shape shape;
  CustomCursor * cc;
};

#endif // ! SOXT_CURSOR_H
