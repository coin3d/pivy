#ifndef COIN_SBROTATION_H
#define COIN_SBROTATION_H

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
#include <Inventor/SbVec4f.h>

class SbMatrix;
class SbVec3f;

#ifdef __PIVY__
%typemap(in) float q[4] (float temp[4]) {
  convert_SbVec4f_array($input, temp);
  $1 = temp;
}

%typemap(out) float * {
  int i;
  $result = PyTuple_New(4);
  
  for (i=0; i<4; i++) {
	PyTuple_SetItem($result, i, PyFloat_FromDouble((double)(*($1+i))));
  }
}

%rename(SbRotation_vec_f) SbRotation::SbRotation(const SbVec3f & axis, const float radians);
%rename(SbRotation_arr) SbRotation::SbRotation(const float q[4]);
%rename(SbRotation_ffff) SbRotation::SbRotation(const float q0, const float q1, const float q2, const float q3);
%rename(SbRotation_mat) SbRotation::SbRotation(const SbMatrix & m);
%rename(SbRotation_vec_vec) SbRotation::SbRotation(const SbVec3f & rotateFrom, const SbVec3f & rotateTo);

%feature("shadow") SbRotation::SbRotation %{
def __init__(self,*args):
   if len(args) == 1:
      if isinstance(args[0], SbMatrix):
         self.this = apply(_pivy.new_SbRotation_mat,args)
         self.thisown = 1
         return
      else:
         self.this = apply(_pivy.new_SbRotation_arr,args)
         self.thisown = 1
         return
   elif len(args) == 2:
      if isinstance(args[1], SbVec3f):
         self.this = apply(_pivy.new_SbRotation_vec_vec,args)
         self.thisown = 1
         return
      else:
         self.this = apply(_pivy.new_SbRotation_vec_f,args)
         self.thisown = 1
         return
   elif len(args) == 4:
      self.this = apply(_pivy.new_SbRotation_ffff,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SbRotation,args)
   self.thisown = 1
%}

%rename(setValue_arr) SbRotation::setValue(const float q[4]);
%rename(setValue_mat) SbRotation::setValue(const SbMatrix & m);
%rename(setValue_vec_f) SbRotation::setValue(const SbVec3f & axis, const float radians);
%rename(setValue_vec_vec) SbRotation::setValue(const SbVec3f & rotateFrom, const SbVec3f & rotateTo);

%feature("shadow") SbRotation::setValue(const float q0, const float q1, const float q2, const float q3) %{
def setValue(*args):
   if len(args) == 2:
      if isinstance(args[1], SbMatrix):
         return apply(_pivy.SbRotation_setValue_mat,args)
      else:
         return apply(_pivy.SbRotation_setValue_arr,args)
   elif len(args) == 3:
      if isinstance(args[2], SbVec3f):
         return apply(_pivy.SbRotation_setValue_vec_vec,args)
      else:
         return apply(_pivy.SbRotation_setValue_vec_f,args)
   return apply(_pivy.SbRotation_setValue,args)
%}

%rename(SbRotation_eq) operator ==(const SbRotation & q1, const SbRotation & q2);
%rename(SbRotation_neq) operator !=(const SbRotation & q1, const SbRotation & q2);
%rename(SbRotation_mul) operator *(const SbRotation & q1, const SbRotation & q2);
#endif

class COIN_DLL_API SbRotation {
public:
  SbRotation(void);
  SbRotation(const SbVec3f & axis, const float radians);
  SbRotation(const float q[4]);
  SbRotation(const float q0, const float q1, const float q2, const float q3);
  SbRotation(const SbMatrix & m);
  SbRotation(const SbVec3f & rotateFrom, const SbVec3f & rotateTo);
  const float * getValue(void) const;
  SbRotation & setValue(const float q0, const float q1,
                        const float q2, const float q3);
#ifndef __PIVY__
  void getValue(float & q0, float & q1, float & q2, float & q3) const;
  void getValue(SbVec3f & axis, float & radians) const;
  void getValue(SbMatrix & matrix) const;
#endif
  SbRotation & invert(void);
  SbRotation inverse(void) const;
  SbRotation & setValue(const float q[4]);
  SbRotation & setValue(const SbMatrix & m);
  SbRotation & setValue(const SbVec3f & axis, const float radians);
  SbRotation & setValue(const SbVec3f & rotateFrom, const SbVec3f & rotateTo);
  SbRotation & operator*=(const SbRotation & q);
  SbRotation & operator*=(const float s);
  friend COIN_DLL_API int operator==(const SbRotation & q1, const SbRotation & q2);
  friend COIN_DLL_API int operator!=(const SbRotation & q1, const SbRotation & q2);
  SbBool equals(const SbRotation & r, const float tolerance) const;
  friend COIN_DLL_API SbRotation operator *(const SbRotation & q1, const SbRotation & q2);
  void multVec(const SbVec3f & src, SbVec3f & dst) const;

  void scaleAngle(const float scaleFactor);
  static SbRotation slerp(const SbRotation & rot0, const SbRotation & rot1,
                          float t);
  static SbRotation identity(void);

  void print(FILE * fp) const;

private:
  SbVec4f quat;
};

COIN_DLL_API int operator ==(const SbRotation & q1, const SbRotation & q2);
COIN_DLL_API int operator !=(const SbRotation & q1, const SbRotation & q2);
COIN_DLL_API SbRotation operator *(const SbRotation & q1, const SbRotation & q2);

#endif // !COIN_SBROTATION_H
