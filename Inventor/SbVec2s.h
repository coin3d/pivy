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

#ifndef COIN_SBVEC2S_H
#define COIN_SBVEC2S_H

#include <stdio.h>
#include <Inventor/SbBasic.h>
#include <Inventor/system/inttypes.h>

#ifdef __PIVY__
%{
static void
convert_SbVec2s_array(PyObject *input, short temp[2])
{
  if (PySequence_Check(input)) {
	if (!PyArg_ParseTuple(input, "hh", temp+0, temp+1)) {
	  PyErr_SetString(PyExc_TypeError, "sequence must contain 2 short int elements");
	  return;
	}
	return;
  } else {
	PyErr_SetString(PyExc_TypeError, "expected a sequence.");
    return;
  }  
}
%}

%typemap(in) short v[2] (short temp[2]) {
  convert_SbVec2s_array($input, temp);
  $1 = temp;
}

%rename(SbVec2s_vec) SbVec2s::SbVec2s(const short v[2]);
%rename(SbVec2s_ss) SbVec2s::SbVec2s(const short x, const short y);

%feature("shadow") SbVec2s::SbVec2s %{
def __init__(self,*args):
   if len(args) == 1:
      self.this = apply(pivyc.new_SbVec2s_vec,args)
      self.thisown = 1
      return
   elif len(args) == 2:
      self.this = apply(pivyc.new_SbVec2s_ss,args)
      self.thisown = 1
      return
   self.this = apply(pivyc.new_SbVec2s,args)
   self.thisown = 1
%}

%rename(setValue_ss) SbVec2s::setValue(short x, short y);

%feature("shadow") SbVec2s::setValue(const short v[2]) %{
def setValue(*args):
   if len(args) == 3:
      return apply(pivyc.SbVec2s_setValue_ss,args)
   return apply(pivyc.SbVec2s_setValue,args)
%}

%apply short *OUTPUT { short &x, short &y };
#endif

class COIN_DLL_API SbVec2s {
public:
  SbVec2s(void);
  SbVec2s(const short v[2]);
  SbVec2s(const short x, const short y);
  int32_t dot(const SbVec2s& v) const;

#ifndef __PIVY__
  const short * getValue(void) const;
#endif

  void getValue(short& x, short& y) const;
  void negate(void);

  SbVec2s& setValue(const short v[2]);
  SbVec2s& setValue(short x, short y);

#ifdef __PIVY__
  // add a method for wrapping c++ operator[] access
  %extend {
	short __getitem__(int i) {
	  return (self->getValue())[i];
	}
  }
#else
  short& operator [](const int i);
  const short& operator [](const int i) const;

  SbVec2s& operator *=(int d);
  SbVec2s& operator /=(int d);
#endif

  SbVec2s& operator *=(double d);
  SbVec2s& operator /=(double d);
  SbVec2s& operator +=(const SbVec2s& u);
  SbVec2s& operator -=(const SbVec2s& u);
  SbVec2s operator -(void) const;
  friend COIN_DLL_API SbVec2s operator *(const SbVec2s& v, int d);
  friend COIN_DLL_API SbVec2s operator *(const SbVec2s& v, double d);
  friend COIN_DLL_API SbVec2s operator *(int d, const SbVec2s& v);
  friend COIN_DLL_API SbVec2s operator *(double d, const SbVec2s& v);
  friend COIN_DLL_API SbVec2s operator /(const SbVec2s& v, int d);
  friend COIN_DLL_API SbVec2s operator /(const SbVec2s& v, double d);
  friend COIN_DLL_API SbVec2s operator +(const SbVec2s& v1, const SbVec2s& v2);
  friend COIN_DLL_API SbVec2s operator -(const SbVec2s& v1, const SbVec2s& v2);
  friend COIN_DLL_API int operator ==(const SbVec2s& v1, const SbVec2s& v2);
  friend COIN_DLL_API int operator !=(const SbVec2s& v1, const SbVec2s& v2);

  void print(FILE * fp) const;

private:
  short vec[2];
};

#ifdef __PIVY__
%clear short &x, short &y;
#endif

#ifndef __PIVY__
COIN_DLL_API SbVec2s operator *(const SbVec2s& v, int d);
COIN_DLL_API SbVec2s operator *(const SbVec2s& v, double d);
COIN_DLL_API SbVec2s operator *(int d, const SbVec2s& v);
COIN_DLL_API SbVec2s operator *(double d, const SbVec2s& v);
COIN_DLL_API SbVec2s operator /(const SbVec2s& v, int d);
COIN_DLL_API SbVec2s operator /(const SbVec2s& v, double d);
COIN_DLL_API SbVec2s operator +(const SbVec2s& v1, const SbVec2s& v2);
COIN_DLL_API SbVec2s operator -(const SbVec2s& v1, const SbVec2s& v2);
COIN_DLL_API int operator ==(const SbVec2s& v1, const SbVec2s& v2);
COIN_DLL_API int operator !=(const SbVec2s& v1, const SbVec2s& v2);
#endif

#endif // !COIN_SBVEC2S_H
