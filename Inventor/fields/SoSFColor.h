/**************************************************************************\
 *
 *  This file is part of the Coin 3D visualization library.
 *  Copyright (C) 1998-2002 by Systems in Motion. All rights reserved.
 *
 *  This library is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU Lesser General Public License
 *  version 2.1 as published by the Free Software Foundation. See the
 *  file LICENSE.LGPL at the root directory of the distribution for
 *  more details.
 *
 *  If you want to use Coin for applications not compatible with the
 *  LGPL, please contact SIM to acquire a Professional Edition license.
 *
 *  Systems in Motion, Prof Brochs gate 6, 7030 Trondheim, NORWAY
 *  http://www.sim.no support@sim.no Voice: +47 22114160 Fax: +47 22207097
 *
\**************************************************************************/

#ifndef COIN_SOSFCOLOR_H
#define COIN_SOSFCOLOR_H

#include <Inventor/fields/SoSField.h>
#include <Inventor/fields/SoSubField.h>
#include <Inventor/SbColor.h>

#ifdef __PIVY__

%typemap(in) float hsv[3] (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%typemap(in) float rgb[3] (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%rename(setValue_col) SoSFColor::setValue(SbColor const &);
%rename(setValue_vec) SoSFColor::setValue(const SbVec3f &vec);
%rename(setValue_fff) SoSFColor::setValue(const float red, const float green, const float blue);

%feature("shadow") SoSFColor::setValue(const float rgb[3]) %{
def setValue(*args):
   if len(args) == 2:
      if isinstance(args[1], SbVec3f):
         return apply(pivyc.SoSFColor_setValue_vec,args)
      else:
         return apply(pivyc.SoSFColor_setValue_col,args)
   elif len(args) == 4:
      return apply(pivyc.SoSFColor_setValue_fff,args)
   return apply(pivyc.SoSFColor_setValue,args)
%}

%rename(setHSVValue_fff) SoSFColor::setHSVValue(const float h, const float s, const float v);

%feature("shadow") SoSFColor::setHSVValue(const float hsv[3]) %{
def setHSVValue(*args):
   if len(args) == 4:
      return apply(pivyc.SoSFColor_setHSVValue_fff,args)
   return apply(pivyc.SoSFColor_setHSVValue,args)
%}

#endif

class COIN_DLL_API SoSFColor : public SoSField {
  typedef SoSField inherited;

  SO_SFIELD_HEADER(SoSFColor, SbColor, const SbColor &);

public:
  static void initClass(void);

  void setValue(const SbVec3f & vec);
  void setValue(const float red, const float green, const float blue);
  void setValue(const float rgb[3]);
  void setHSVValue(const float h, const float s, const float v);
  void setHSVValue(const float hsv[3]);
};

#endif // !COIN_SOSFCOLOR_H
