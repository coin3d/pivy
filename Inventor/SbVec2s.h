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
%apply short *OUTPUT { short &x, short &y };
#endif

class COIN_DLL_API SbVec2s {
public:
#ifndef __PIVY__
  SbVec2s(void);
  SbVec2s(const short v[2]);
#endif

  SbVec2s(const short x, const short y);
  int32_t dot(const SbVec2s& v) const;

#ifndef __PIVY__
  const short * getValue(void) const;
#endif

  void getValue(short& x, short& y) const;
  void negate(void);

#ifndef __PIVY__
  SbVec2s& setValue(const short v[2]);
#endif

  SbVec2s& setValue(short x, short y);

#ifdef __PIVY__
  // add a method for wrapping c++ operator[] access
  %addmethods {
	short __getitem__(int i) {
	  return (self->getValue())[i];
	}
  }
#endif

#ifndef __PIVY__
  short& operator [](const int i);
  const short& operator [](const int i) const;
#endif

  SbVec2s& operator *=(int d);
#ifndef __PIVY__
  SbVec2s& operator *=(double d);
#endif
  SbVec2s& operator /=(int d);
#ifndef __PIVY__
  SbVec2s& operator /=(double d);
#endif
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
