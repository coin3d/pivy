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

#ifndef COIN_SBCOLOR4F_H
#define COIN_SBCOLOR4F_H

#include <Inventor/system/inttypes.h>
#include <Inventor/SbColor.h>

class SbVec4f;

#ifdef __PIVY__
%typemap(in) float col[4] (float temp[4]) {
  convert_SbVec4f_array($input, temp);
  $1 = temp;
}

%typemap(in) float * rgba (float temp[4]) {
  convert_SbVec4f_array($input, temp);
  $1 = temp;
}

%typemap(in) float hsv[3] (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%typemap(in) float *rgb (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%rename(SbColor4f_col_f) SbColor4f::SbColor4f(const SbColor &rgb, const float alpha);
%rename(SbColor4f_vec) SbColor4f::SbColor4f(const SbVec4f &v);
%rename(SbColor4f_rgb) SbColor4f::SbColor4f(const float *const rgba);
%rename(SbColor4f_ffff) SbColor4f::SbColor4f(const float r, const float g, const float b, const float a=1.0f);

%feature("shadow") SbColor4f::SbColor4f %{
def __init__(self,*args):
   if len(args) == 1:
      if isinstance(args[0], SbVec4f):
         self.this = apply(pivyc.new_SbColor4f_vec,args)
         self.thisown = 1
         return
      else:
         self.this = apply(pivyc.new_SbColor4f_rgb,args)
         self.thisown = 1
         return
   elif len(args) == 2:
      self.this = apply(pivyc.new_SbColor4f_col_f,args)
      self.thisown = 1
      return
   elif len(args) == 3:
      self.this = apply(pivyc.new_SbColor4f_ffff,args)
      self.thisown = 1
      return
   self.this = apply(pivyc.new_SbColor4f,args)
   self.thisown = 1
%}

%rename(setValue_ffff) SbColor4f::setValue(const float r, const float g, const float b, const float a=1.0f);

%feature("shadow") SbColor4f::setValue(const float col[4]) %{
def setValue(*args):
   if len(args) == 5:
      return apply(pivyc.SbColor4f_setValue_ffff,args)
   return apply(pivyc.SbColor4f_setValue,args)
%}

%rename(setHSVValue_ffff) SbColor4f::setHSVValue(float h, float s, float v, float a=1.0f);

%feature("shadow") SbColor4f::setHSVValue(const float hsv[3], float alpha=1.0f) %{
def setHSVValue(*args):
   if len(args) == 5:
      return apply(pivyc.SbColor4f_setHSVValue_ffff,args)
   return apply(pivyc.SbColor4f_setHSVValue,args)
%}

%apply float *OUTPUT { float &r, float &g, float &b, float &a };
%apply float *OUTPUT { float &h, float &s, float &v };

#endif


class COIN_DLL_API SbColor4f {
public:
  SbColor4f(void);
  SbColor4f(const SbColor &rgb, const float alpha);
  SbColor4f(const SbVec4f& v);
  SbColor4f(const float* const rgba);
  SbColor4f(const float r, const float g, const float b, const float a = 1.0f);

  void setValue(const float r, const float g, const float b,
                const float a = 1.0f);
  void setValue(const float col[4]);

#ifndef __PIVY__
  const float *getValue() const;
#endif

  void getValue(float &r, float &g, float &b, float &a);


  SbColor4f& setRGB(const SbColor &col);
  void getRGB(SbColor &color);
  SbColor4f& setHSVValue(float h, float s, float v, float a = 1.0f);
  SbColor4f& setHSVValue(const float hsv[3], float alpha = 1.0f);
  void getHSVValue(float &h, float &s, float &v) const;

#ifndef __PIVY__
  void getHSVValue(float hsv[3]) const;
#endif

  SbColor4f& setPackedValue(const uint32_t rgba);
  uint32_t getPackedValue() const;

#ifdef __PIVY__
  // add a method for wrapping c++ operator[] access
  %addmethods {
        float __getitem__(int i) {
          return (self->getValue())[i];
        }
  }
#else
  float operator[](const int idx) const;
  float &operator[](const int idx);
#endif

  SbColor4f &operator*=(const float d);
  SbColor4f &operator/=(const float d);
  SbColor4f &operator+=(const SbColor4f &c);
  SbColor4f &operator-=(const SbColor4f &c);

  friend COIN_DLL_API SbColor4f operator *(const SbColor4f &c, const float d);
  friend COIN_DLL_API SbColor4f operator *(const float d, const SbColor4f &c);
  friend COIN_DLL_API SbColor4f operator /(const SbColor4f &c, const float d);
  friend COIN_DLL_API SbColor4f operator +(const SbColor4f &v1, const SbColor4f &v2);
  friend COIN_DLL_API SbColor4f operator -(const SbColor4f &v1, const SbColor4f &v2);
  friend COIN_DLL_API int operator ==(const SbColor4f &v1, const SbColor4f &v2);
  friend COIN_DLL_API int operator !=(const SbColor4f &v1, const SbColor4f &v2);

private:
  float vec[4];
  float red() const { return this->vec[0]; }
  float green() const { return this->vec[1]; }
  float blue() const { return this->vec[2]; }
  float alpha() const { return this->vec[3]; }
};

#ifdef __PIVY__
%clear float &r, float &g, float &b, float &a;
%clear float &h, float &s, float &v;
#endif

#ifndef __PIVY__
COIN_DLL_API SbColor4f operator *(const SbColor4f &c, const float d);
COIN_DLL_API SbColor4f operator *(const float d, const SbColor4f &c);
COIN_DLL_API SbColor4f operator /(const SbColor4f &c, const float d);
COIN_DLL_API SbColor4f operator +(const SbColor4f &v1, const SbColor4f &v2);
COIN_DLL_API SbColor4f operator -(const SbColor4f &v1, const SbColor4f &v2);
COIN_DLL_API int operator ==(const SbColor4f &v1, const SbColor4f &v2);
COIN_DLL_API int operator !=(const SbColor4f &v1, const SbColor4f &v2);
#endif

#endif // !COIN_SBCOLOR4F_H
