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

#ifndef COIN_SBCOLOR_H
#define COIN_SBCOLOR_H

#include <Inventor/system/inttypes.h>
#include <Inventor/SbVec3f.h>

#ifdef __PIVY__

%typemap(in) float hsv[3] (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%typemap(in) float *rgb (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%rename(SbColor_vec) SbColor::SbColor(const SbVec3f &v);
%rename(SbColor_rgb) SbColor::SbColor(const float *const rgb);
%rename(SbColor_fff) SbColor::SbColor(const float r, const float g, const float b);

%feature("shadow") SbColor::SbColor %{
def __init__(self,*args):
   if len(args) == 1:
      if isinstance(args[0], SbVec3f):
         self.this = apply(pivyc.new_SbColor_vec,args)
         self.thisown = 1
         return
      else:
         self.this = apply(pivyc.new_SbColor_rgb,args)
         self.thisown = 1
         return
   elif len(args) == 3:
      self.this = apply(pivyc.new_SbColor_fff,args)
      self.thisown = 1
      return
   self.this = apply(pivyc.new_SbColor,args)
   self.thisown = 1
%}

%rename(setHSVValue_fff) SbColor::setHSVValue(float h, float s, float v);

%feature("shadow") SbColor::setHSVValue(const float hsv[3]) %{
def setHSVValue(*args):
   if len(args) == 4:
      return apply(pivyc.SbColor_setHSVValue_fff,args)
   return apply(pivyc.SbColor_setHSVValue,args)
%}

%apply float *OUTPUT { float & h, float & s, float & v };

#endif


class COIN_DLL_API SbColor : public SbVec3f {
public:
  SbColor(void);
  SbColor(const SbVec3f& v);
  SbColor(const float* const rgb);
  SbColor(const float r, const float g, const float b);

  SbColor & setHSVValue(float h, float s, float v);
  SbColor & setHSVValue(const float hsv[3]);
  void getHSVValue(float &h, float &s, float &v) const;

#ifndef __PIVY__
  void getHSVValue(float hsv[3]) const;
#endif

  SbColor & setPackedValue(const uint32_t rgba, float& transparency);
  uint32_t getPackedValue(const float transparency = 0.0f) const;

private:
  float red(void) const { return (*this)[0]; }
  float green(void) const { return (*this)[1]; }
  float blue(void) const { return (*this)[2]; }
  uint32_t convertToUInt(const float val) { return (uint32_t)(val*255.0f);}
};

#ifdef __PIVY__
%clear float & h, float & s, float & v;
#endif

#endif // !COIN_SBCOLOR_H
