#ifndef COIN_SBVEC3D_H
#define COIN_SBVEC3D_H

/**************************************************************************\
 *
 *  This file is part of the Coin 3D visualization library.
 *  Copyright (C) 1998-2003 by Systems in Motion.  All rights reserved.
 *
 *  This library is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU General Public License
 *  ("GPL") version 2 as published by the Free Software Foundation.
 *  See the file LICENSE.GPL at the root directory of this source
 *  distribution for additional information about the GNU GPL.
 *
 *  For using Coin with software that can not be combined with the GNU
 *  GPL, and for taking advantage of the additional benefits of our
 *  support services, please contact Systems in Motion about acquiring
 *  a Coin Professional Edition License.
 *
 *  See <URL:http://www.coin3d.org> for  more information.
 *
 *  Systems in Motion, Teknobyen, Abels Gate 5, 7030 Trondheim, NORWAY.
 *  <URL:http://www.sim.no>.
 *
\**************************************************************************/

#include <stdio.h>
#include <Inventor/SbBasic.h>

class SbVec3f;

#ifdef __PIVY__
%{
static void
convert_SbVec3d_array(PyObject *input, double temp[3])
{
  if (PySequence_Check(input)) {
	if (!PyArg_ParseTuple(input, "ddd", temp+0, temp+1, temp+2)) {
	  PyErr_SetString(PyExc_TypeError, "sequence must contain 3 double elements");
	  return;
	}
	return;
  } else {
	PyErr_SetString(PyExc_TypeError, "expected a sequence.");
    return;
  }  
}
%}

%typemap(in) double v[3] (double temp[3]) {
  convert_SbVec3d_array($input, temp);
  $1 = temp;
}

/* for some strange reason the %apply directive below doesn't work 
 * for this class on getValue(f,f,f)...
 * created this typemap for getValue(void) instead as a workaround.
 */
%typemap(out) double * {
  int i;
  $result = PyTuple_New(3);
  
  for (i=0; i<3; i++) {
	PyTuple_SetItem($result, i, PyFloat_FromDouble((double)(*($1+i))));
  }
}

%rename(SbVec3d_vec) SbVec3d::SbVec3d(const double v[3]);
%rename(SbVec3d_fff) SbVec3d::SbVec3d(const double x, const double y, const double z);
%rename(SbVec3d_pl_pl_pl) SbVec3d::SbVec3d(const SbPlane & p0, const SbPlane & p1, const SbPlane & p2);

%feature("shadow") SbVec3d::SbVec3d %{
def __init__(self,*args):
   if len(args) == 1:
      self.this = apply(_pivy.new_SbVec3d_vec,args)
      self.thisown = 1
      return
   elif len(args) == 3:
      if isinstance(args[0], SbPlane):
         self.this = apply(_pivy.new_SbVec3d_pl_pl_pl,args)
         self.thisown = 1
         return
      else:
         self.this = apply(_pivy.new_SbVec3d_fff,args)
         self.thisown = 1
         return
   self.this = apply(_pivy.new_SbVec3d,args)
   self.thisown = 1
%}

%rename(setValue_fff) SbVec3d::setValue(const double x, const double y, const double z);
%rename(setValue_vec_vec_vec_vec) SbVec3d::setValue(const SbVec3d & barycentric, const SbVec3d & v0, const SbVec3d & v1, const SbVec3d & v2);
%rename(setValue_vec) SbVec3d::setValue(const SbVec3d & v);

%feature("shadow") SbVec3d::setValue(const double vec[3]) %{
def setValue(*args):
   if len(args) == 4:
      return apply(_pivy.SbVec3d_setValue_fff,args)
   elif len(args) == 5:
      return apply(_pivy.SbVec3d_setValue_vec_vec_vec_vec,args)
   elif len(args) == 2:
      return apply(_pivy.SbVec3d_setValue_vec,args)
   return apply(_pivy.SbVec3d_setValue,args)
%}

%rename(SbVec3d_mult) operator *(const SbVec3d & v, const float d);
%rename(SbVec3d_d_mult) operator *(const float d, const SbVec3d & v);
%rename(SbVec3d_add) operator+(const SbVec3d & v1, const SbVec3d & v2);
%rename(SbVec3d_sub) operator-(const SbVec3d & v1, const SbVec3d & v2);
%rename(SbVec3d_div) operator /(const SbVec3d & v, const float d);
%rename(SbVec3d_eq) operator ==(const SbVec3d & v1, const SbVec3d & v2);
%rename(SbVec3d_neq) operator !=(const SbVec3d & v1, const SbVec3d & v2);

%apply double *OUTPUT { double & x, double & y, double & z };
#endif

class COIN_DLL_API SbVec3d {
public:
  SbVec3d(void) { }
  SbVec3d(const double v[3]);
  SbVec3d(const double x, const double y, const double z);
  SbVec3d(const SbVec3f & v);
  SbVec3d cross(const SbVec3d & v) const;
  double dot(const SbVec3d & v) const;
  SbBool equals(const SbVec3d & v, const double tolerance) const;
  SbVec3d getClosestAxis(void) const;
  const double * getValue(void) const;
#ifndef __PIVY__
  void getValue(double & x, double & y, double & z) const;
#endif
  double length(void) const;
  double sqrLength() const;
  void negate(void);
  double normalize(void);
  SbVec3d & setValue(const double v[3]);
  SbVec3d & setValue(const double x, const double y, const double z);
  SbVec3d & setValue(const SbVec3d & barycentric,
                     const SbVec3d & v0,
                     const SbVec3d & v1,
                     const SbVec3d & v2);
  SbVec3d & setValue(const SbVec3f & v);
#ifdef __PIVY__
  // add a method for wrapping c++ operator[] access
  %extend {
	float __getitem__(int i) {
	  return (self->getValue())[i];
	}
	void  __setitem__(int i, float value) {
	  (*self)[i] = value;
	}
  }
#else
  double & operator [](const int i);
  const double & operator [](const int i) const;
#endif
  SbVec3d & operator *=(const double d);
  SbVec3d & operator /=(const double d);
  SbVec3d & operator +=(const SbVec3d & u);
  SbVec3d & operator -=(const SbVec3d & u);
  SbVec3d operator -(void) const;
  friend COIN_DLL_API SbVec3d operator *(const SbVec3d & v, const double d);
  friend COIN_DLL_API SbVec3d operator *(const double d, const SbVec3d & v);
  friend COIN_DLL_API SbVec3d operator /(const SbVec3d & v, const double d);
  friend COIN_DLL_API SbVec3d operator +(const SbVec3d & v1, const SbVec3d & v2);
  friend COIN_DLL_API SbVec3d operator -(const SbVec3d & v1, const SbVec3d & v2);
  friend COIN_DLL_API int operator ==(const SbVec3d & v1, const SbVec3d & v2);
  friend COIN_DLL_API int operator !=(const SbVec3d & v1, const SbVec3d & v2);

  void print(FILE * fp) const;

private:
  double vec[3];
};

#ifdef __PIVY__
%clear double & x, double & y, double & z;
#endif

COIN_DLL_API SbVec3d operator *(const SbVec3d & v, const double d);
COIN_DLL_API SbVec3d operator *(const double d, const SbVec3d & v);
COIN_DLL_API SbVec3d operator /(const SbVec3d & v, const double d);
COIN_DLL_API SbVec3d operator +(const SbVec3d & v1, const SbVec3d & v2);
COIN_DLL_API SbVec3d operator -(const SbVec3d & v1, const SbVec3d & v2);
COIN_DLL_API int operator ==(const SbVec3d & v1, const SbVec3d & v2);
COIN_DLL_API int operator !=(const SbVec3d & v1, const SbVec3d & v2);


/* inlined methods ********************************************************/

inline double &
SbVec3d::operator [](const int i)
{
  return this->vec[i];
}

inline const double &
SbVec3d::operator [](const int i) const
{
  return this->vec[i];
}

#endif // !COIN_SBVEC3D_H
