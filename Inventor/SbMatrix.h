#ifndef COIN_SBMATRIX_H
#define COIN_SBMATRIX_H

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

class SbLine;
class SbRotation;
class SbVec3f;
class SbVec4f;

typedef float SbMat[4][4];

#ifdef __PIVY__
%{
static void
convert_SbMat_array(PyObject *input, SbMat temp)
{
  if (PySequence_Check(input)) {
	if (!PyArg_ParseTuple(input, "(ffff)(ffff)(ffff)(ffff)",
						  &temp[0][0], &temp[0][1], &temp[0][2], &temp[0][3],
						  &temp[1][0], &temp[1][1], &temp[1][2], &temp[1][3],
						  &temp[2][0], &temp[2][1], &temp[2][2], &temp[2][3],
						  &temp[3][0], &temp[3][1], &temp[3][2], &temp[3][3])) {
	  PyErr_SetString(PyExc_TypeError, "sequence must contain 4 sequences where every sequence contains 4 float elements");
	  return;
	}
	return;
  } else {
	PyErr_SetString(PyExc_TypeError, "expected a sequence.");
    return;
  }  
}
%}

%typemap(in) SbMat * (SbMat temp) {
  convert_SbMat_array($input, temp);
  $1 = &temp;
}

%typemap(out) SbMat & {
  int i,j;
  $result = PyTuple_New(4);
  
  for (i=0; i<4; i++) {
	PyObject *oi = PyTuple_New(4);
	for (j=0; j<4; j++) {
	  PyObject *oj = PyFloat_FromDouble((double)(*$1)[i][j]);
	  PyTuple_SetItem(oi, j, oj);
	}
	PyTuple_SetItem($result, i, oi);	
  }
}

%rename(SbMatrix_f16) SbMatrix::SbMatrix(const float a11, const float a12, const float a13, const float a14,
										 const float a21, const float a22, const float a23, const float a24,
										 const float a31, const float a32, const float a33, const float a34,
										 const float a41, const float a42, const float a43, const float a44);
%rename(SbMatrix_SbMat) SbMatrix::SbMatrix(const SbMat * matrix);

%feature("shadow") SbMatrix::SbMatrix %{
def __init__(self,*args):
   if len(args) == 1:
      self.this = apply(_pivy.new_SbMatrix_SbMat,args)
      self.thisown = 1
      return
   elif len(args) == 16:
      self.this = apply(_pivy.new_SbMatrix_f16,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SbMatrix,args)
   self.thisown = 1
%}

%rename(det3_i6) SbMatrix::det3(int r1, int r2, int r3,
								int c1, int c2, int c3) const;

%feature("shadow") SbMatrix::setScale(const float s) %{
def det3(*args):
   if len(args) == 7:
      return apply(_pivy.SbMatrix_det3_i6,args)
   return apply(_pivy.SbMatrix_det3,args)
%}

%rename(setScale_vec3) SbMatrix::setScale(const SbVec3f & s);

%feature("shadow") SbMatrix::setScale(const float s) %{
def setScale(args):
  if type(args[1]) == type(0.0):
	return apply(_pivy.SbMatrix_setScale,args)
  return apply(_pivy.SbMatrix_setScale_vec3,args)
%}

%rename(setTransform_vec3_rot_vec3_rot) SbMatrix::setTransform(const SbVec3f & t, const SbRotation & r, const SbVec3f & s,
															   const SbRotation & so);
%rename(setTransform_vec3_rot_vec3_rot_vec3) SbMatrix::setTransform(const SbVec3f & translation,
																	const SbRotation & rotation, const SbVec3f & scaleFactor,
																	const SbRotation & scaleOrientation, const SbVec3f & center);

%feature("shadow") SbMatrix::setTransform(const SbVec3f & t, const SbRotation & r, const SbVec3f & s) %{
def setTransform(*args):
   if len(args) == 5:
      return apply(_pivy.SbMatrix_setTransform_vec3_rot_vec3_rot,args)
   elif len(args) == 6:
      return apply(_pivy.SbMatrix_setTransform_vec3_rot_vec3_rot_vec3,args)
   return apply(_pivy.SbMatrix_setTransform,args)
%}

%rename(getTransform_vec3) SbMatrix::getTransform(SbVec3f & translation, SbRotation & rotation,
												  SbVec3f & scaleFactor, SbRotation & scaleOrientation,
												  const SbVec3f & center) const;

%feature("shadow") SbMatrix::getTransform(SbVec3f & t, SbRotation & r, SbVec3f & s, SbRotation & so) %{
def getTransform(*args):
   if len(args) == 2:
      return apply(_pivy.SbMatrix_getTransform_vec3,args)
   return apply(_pivy.SbMatrix_getTransform,args)
%}

%rename(multVecMatrix_vec4) SbMatrix::multVecMatrix(const SbVec4f & src, SbVec4f & dst) const;

%feature("shadow") SbMatrix::multVecMatrix(const SbVec3f & src, SbVec3f & dst) %{
def multVecMatrix(*args):
   if isinstance(args[1], SbVec4f):
      return apply(_pivy.SbMatrix_multVecMatrix_vec4,args)
   return apply(_pivy.SbMatrix_multVecMatrix,args)
%}

/* the next 2 typemaps handle the return value for e.g. multMatrixVec() */
%typemap(argout) SbVec3f & dst, SbVec4f & dst {
  $result = SWIG_NewPointerObj((void *) $1, $1_descriptor, 1);
}
%typemap(in,numinputs=0) SbVec3f & dst, SbVec4f & dst {
    $1 = new $1_basetype();
}
#endif

class COIN_DLL_API SbMatrix {
public:
  SbMatrix(void);
  SbMatrix(const float a11, const float a12, const float a13, const float a14,
           const float a21, const float a22, const float a23, const float a24,
           const float a31, const float a32, const float a33, const float a34,
           const float a41, const float a42, const float a43, const float a44);
#ifndef __PIVY__
  SbMatrix(const SbMat & matrix);
#endif
  SbMatrix(const SbMat * matrix);

  ~SbMatrix(void);

  SbMatrix & operator =(const SbMat & m);

  operator float*(void);
  SbMatrix & operator =(const SbMatrix & m);

/**
 * workaround for swig generating an unnecessary cast
 * -> (SbMat const &)*arg);
 **/
#ifdef __PIVY__
%extend {
  void setValue(const SbMat * m) {
    self->setValue(*m);
  }
}
#else
  void setValue(const SbMat & m);
#endif
  const SbMat & getValue(void) const;

  void makeIdentity(void);
  void setRotate(const SbRotation & q);
  SbMatrix inverse(void) const;
  float det3(int r1, int r2, int r3,
             int c1, int c2, int c3) const;
  float det3(void) const;
  float det4(void) const;

  SbBool equals(const SbMatrix & m, float tolerance) const;


  operator SbMat&(void);
#ifdef __PIVY__
  // add a method for wrapping c++ operator[] access
  %extend {
	const float *__getitem__(int i) {
	  return (self->getValue())[i];
	}
  }
#else
  float * operator [](int i);
  const float * operator [](int i) const;
#endif
  SbMatrix & operator =(const SbRotation & q);
  SbMatrix & operator *=(const SbMatrix & m);
  friend COIN_DLL_API SbMatrix operator *(const SbMatrix & m1, const SbMatrix & m2);
  friend COIN_DLL_API int operator ==(const SbMatrix & m1, const SbMatrix & m2);
  friend COIN_DLL_API int operator !=(const SbMatrix & m1, const SbMatrix & m2);
  void getValue(SbMat & m) const;
  static SbMatrix identity(void);
  void setScale(const float s);
  void setScale(const SbVec3f & s);
  void setTranslate(const SbVec3f & t);
  void setTransform(const SbVec3f & t, const SbRotation & r, const SbVec3f & s);
  void setTransform(const SbVec3f & t, const SbRotation & r, const SbVec3f & s,
                    const SbRotation & so);
  void setTransform(const SbVec3f & translation,
                    const SbRotation & rotation, const SbVec3f & scaleFactor,
                    const SbRotation & scaleOrientation, const SbVec3f & center);
  void getTransform(SbVec3f & t, SbRotation & r,
                    SbVec3f & s, SbRotation & so) const;
  void getTransform(SbVec3f & translation, SbRotation & rotation,
                    SbVec3f & scaleFactor, SbRotation & scaleOrientation,
                    const SbVec3f & center) const;
  SbBool factor(SbMatrix & r, SbVec3f & s, SbMatrix & u, SbVec3f & t,
                SbMatrix & proj);
  SbBool LUDecomposition(int index[4], float & d);
  void LUBackSubstitution(int index[4], float b[4]) const;
  SbMatrix transpose(void) const;
  SbMatrix & multRight(const SbMatrix & m);
  SbMatrix & multLeft(const SbMatrix & m);
  void multMatrixVec(const SbVec3f & src, SbVec3f & dst) const;
  void multVecMatrix(const SbVec3f & src, SbVec3f & dst) const;
  void multDirMatrix(const SbVec3f & src, SbVec3f & dst) const;
  void multLineMatrix(const SbLine & src, SbLine & dst) const;
  void multVecMatrix(const SbVec4f & src, SbVec4f & dst) const;

  void print(FILE * fp) const;

private:
  float matrix[4][4];

  void operator /=(const float v);
  void operator *=(const float v);
};

COIN_DLL_API SbMatrix operator *(const SbMatrix & m1, const SbMatrix & m2);
COIN_DLL_API int operator ==(const SbMatrix & m1, const SbMatrix & m2);
COIN_DLL_API int operator !=(const SbMatrix & m1, const SbMatrix & m2);

#ifdef __PIVY__
%typemap(argout) SbVec3f & dst, SbVec4f & dst;
%typemap(in,numinputs=0) SbVec3f & dst, SbVec4f & dst;
#endif
#endif // !COIN_SBMATRIX_H
