#ifndef COIN_SOMFVEC3F_H
#define COIN_SOMFVEC3F_H

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

#include <Inventor/fields/SoMField.h>
#include <Inventor/fields/SoSubField.h>
#include <Inventor/SbVec3f.h>

#ifdef __PIVY__
%{
static void
convert_SoMFVec3f_array(PyObject *input, int len, float temp[][3])
{
  int i,j;

  for (i=0; i<len; i++) {
	PyObject *oi = PySequence_GetItem(input,i);

	for (j=0; j<3; j++) {
	  PyObject *oj = PySequence_GetItem(oi,j);

	  if (PyNumber_Check(oj)) {
		temp[i][j] = (float) PyFloat_AsDouble(oj);
	  } else {
		PyErr_SetString(PyExc_ValueError,"Sequence elements must be numbers");
		free(temp);       
		return;
	  }
	}
  }
  return;
}
%}

%typemap(in) float xyz[][3] (float (*temp)[3]) {
  int len;

  if (PySequence_Check($input)) {
	len  = PySequence_Length($input);

	temp = (float (*)[3]) malloc(len*3*sizeof(float));
	convert_SoMFVec3f_array($input, len, temp);
  
	$1 = temp;
  } else {
	PyErr_SetString(PyExc_TypeError, "expected a sequence.");
  }
}

%typemap(in) float xyz[3] (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%rename(setValue_vec) SoMFVec3f::setValue(SbVec3f const &);
%rename(setValue_fff) SoMFVec3f::setValue(const float x, const float y, const float z);

%feature("shadow") SoMFVec3f::setValue(const float xyz[3]) %{
def setValue(*args):
   if isinstance(args[1], SbVec3f):
      return apply(_pivy.SoMFVec3f_setValue_vec,args)
   elif len(args) == 4:
      return apply(_pivy.SoMFVec3f_setValue_fff,args)
   return apply(_pivy.SoMFVec3f_setValue,args)
%}

%rename(set1Value_i_vec) SoMFVec3f::set1Value(int const ,SbVec3f const &);
%rename(set1Value_i_fff) SoMFVec3f::set1Value(const int idx, const float x, const float y, const float z);

%feature("shadow") SoMFVec3f::set1Value(const int idx, const float xyz[3]) %{
def set1Value(*args):
   if isinstance(args[2], SbVec3f):
      return apply(_pivy.SoMFVec3f_set1Value_i_vec,args)
   elif len(args) == 5:
      return apply(_pivy.SoMFVec3f_set1Value_i_fff,args)
   return apply(_pivy.SoMFVec3f_set1Value,args)
%}

%rename(setValues_i_i_vec) SoMFVec3f::setValues(int const ,int const ,SbVec3f const *);

%feature("shadow") SoMFVec3f::setValues(const int start, const int num, const float xyz[][3]) %{
def setValues(*args):
   if isinstance(args[3], SbVec3f):
      return apply(_pivy.SoMFVec3f_setValues_i_i_vec,args)
   return apply(_pivy.SoMFVec3f_setValues,args)
%}
#endif

class COIN_DLL_API SoMFVec3f : public SoMField {
  typedef SoMField inherited;

  SO_MFIELD_HEADER(SoMFVec3f, SbVec3f, const SbVec3f &);

  SO_MFIELD_SETVALUESPOINTER_HEADER(float);
  SO_MFIELD_SETVALUESPOINTER_HEADER(SbVec3f);

public:
  static void initClass(void);

  void setValues(const int start, const int num, const float xyz[][3]);
  void set1Value(const int idx, const float x, const float y, const float z);
  void set1Value(const int idx, const float xyz[3]);
  void setValue(const float x, const float y, const float z);

#ifdef __PIVY__
  %extend {
        void __call__(float xyz[3]) {
          self->setValue(xyz);
        }
  }
#endif

  void setValue(const float xyz[3]);
};

#endif // !COIN_SOMFVEC3F_H
