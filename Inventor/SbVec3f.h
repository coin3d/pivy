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

#ifndef COIN_SBVEC3F_H
#define COIN_SBVEC3F_H

#include <stdio.h>

#include <Inventor/SbBasic.h>

class SbPlane;

#ifdef __PIVY__
%{
static void
convert_SbVec3f_array(PyObject *input, float temp[3])
{
  if (PySequence_Check(input)) {
	if (!PyArg_ParseTuple(input, "fff", temp+0, temp+1, temp+2)) {
	  PyErr_SetString(PyExc_TypeError, "sequence must contain 3 float elements");
	  return;
	}
	return;
  } else {
	PyErr_SetString(PyExc_TypeError, "expected a sequence.");
    return;
  }  
}
%}

%typemap(in) float v[3] (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%rename(SbVec3f_vec) SbVec3f::SbVec3f(const float v[3]);
%rename(SbVec3f_fff) SbVec3f::SbVec3f(const float x, const float y, const float z);
%rename(SbVec3f_pl_pl_pl) SbVec3f::SbVec3f(const SbPlane & p0, const SbPlane & p1, const SbPlane & p2);

%feature("shadow") SbVec3f::SbVec3f %{
def __init__(self,*args):
   if len(args) == 1:
      self.this = apply(pivyc.new_SbVec3f_vec,args)
      self.thisown = 1
      return
   elif len(args) == 3:
      if type(args[0]) == type(1.0):
         self.this = apply(pivyc.new_SbVec3f_fff,args)
         self.thisown = 1
         return
      else:
         self.this = apply(pivyc.new_SbVec3f_pl_pl_pl,args)
         self.thisown = 1
         return
   self.this = apply(pivyc.new_SbVec3f,args)
   self.thisown = 1
%}

%rename(setValue_fff) SbVec3f::setValue(const float x, const float y, const float z);
%rename(setValue_vec_vec_vec_vec) SbVec3f::setValue(const SbVec3f & barycentric, const SbVec3f & v0, const SbVec3f & v1, const SbVec3f & v2);

%feature("shadow") SbVec3f::setValue(const float vec[3]) %{
def setValue(*args):
   if len(args) == 4:
      return apply(pivyc.SbVec3f_setValue_fff,args)
   elif len(args) == 5:
      return apply(pivyc.SbVec3f_setValue_vec_vec_vec_vec,args)
   return apply(pivyc.SbVec3f_setValue,args)
%}

%apply float *OUTPUT { float & x, float & y, float & z };
#endif

class COIN_DLL_API SbVec3f {
public:
  SbVec3f(void);
  SbVec3f(const float v[3]);
  SbVec3f(const float x, const float y, const float z);
  SbVec3f(const SbPlane & p0, const SbPlane & p1, const SbPlane & p2);

  SbVec3f cross(const SbVec3f & v) const;

  float dot(const SbVec3f & v) const;
  SbBool equals(const SbVec3f & v, const float tolerance) const;
  SbVec3f getClosestAxis(void) const;

#ifndef __PIVY__
  const float * getValue(void) const;
#endif

  void getValue(float & x, float & y, float & z) const;
  float length(void) const;
  float sqrLength() const;
  void negate(void);
  float normalize(void);

  SbVec3f & setValue(const float v[3]);
  SbVec3f & setValue(const float x, const float y, const float z);
  SbVec3f & setValue(const SbVec3f & barycentric,
                     const SbVec3f & v0,
                     const SbVec3f & v1,
                     const SbVec3f & v2);

#ifdef __PIVY__
  // add a method for wrapping c++ operator[] access
  %addmethods {
	float __getitem__(int i) {
	  return (self->getValue())[i];
	}
  }
#else
  float & operator [](const int i);
  const float & operator [](const int i) const;
#endif

  SbVec3f & operator *=(const float d);
  SbVec3f & operator /=(const float d);
  SbVec3f & operator +=(const SbVec3f & u);
  SbVec3f & operator -=(const SbVec3f & u);
  SbVec3f operator -(void) const;
  friend COIN_DLL_API SbVec3f operator *(const SbVec3f & v, const float d);
  friend COIN_DLL_API SbVec3f operator *(const float d, const SbVec3f & v);
  friend COIN_DLL_API SbVec3f operator /(const SbVec3f & v, const float d);
  friend COIN_DLL_API SbVec3f operator +(const SbVec3f & v1, const SbVec3f & v2);
  friend COIN_DLL_API SbVec3f operator -(const SbVec3f & v1, const SbVec3f & v2);
  friend COIN_DLL_API int operator ==(const SbVec3f & v1, const SbVec3f & v2);
  friend COIN_DLL_API int operator !=(const SbVec3f & v1, const SbVec3f & v2);

  void print(FILE * fp) const;

private:
  float vec[3];
};

#ifdef __PIVY__
%clear float & x, float & y, float & z;
#endif

#ifndef __PIVY__
COIN_DLL_API SbVec3f operator *(const SbVec3f & v, const float d);
COIN_DLL_API SbVec3f operator *(const float d, const SbVec3f & v);
COIN_DLL_API SbVec3f operator /(const SbVec3f & v, const float d);
COIN_DLL_API SbVec3f operator +(const SbVec3f & v1, const SbVec3f & v2);
COIN_DLL_API SbVec3f operator -(const SbVec3f & v1, const SbVec3f & v2);
COIN_DLL_API int operator ==(const SbVec3f & v1, const SbVec3f & v2);
COIN_DLL_API int operator !=(const SbVec3f & v1, const SbVec3f & v2);

/* inlined methods ********************************************************/

inline float &
SbVec3f::operator [](const int i)
{
  return this->vec[i];
}

inline const float &
SbVec3f::operator [](const int i) const
{
  return this->vec[i];
}
#endif

#endif // !COIN_SBVEC3F_H
