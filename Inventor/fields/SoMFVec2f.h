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

#ifndef COIN_SOMFVEC2F_H
#define COIN_SOMFVEC2F_H

#include <Inventor/fields/SoMField.h>
#include <Inventor/fields/SoSubField.h>
#include <Inventor/SbVec2f.h>

#ifdef __PIVY__
%{
static void
convert_SoMFVec2f_array(PyObject *input, int len, float temp[][2])
{
  int i,j;

  for (i=0; i<len; i++) {
	PyObject *oi = PySequence_GetItem(input,i);

	for (j=0; j<2; j++) {
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

%typemap(in) float xy[][2] (float (*temp)[2]) {
  int len;

  if (PySequence_Check($input)) {
	len  = PySequence_Length($input);

	temp = (float (*)[2]) malloc(len*2*sizeof(float));
	convert_SoMFVec2f_array($input, len, temp);
  
	$1 = temp;
  } else {
	PyErr_SetString(PyExc_TypeError, "expected a sequence.");
  }
}

%typemap(in) float xy[2] (float temp[2]) {
  convert_SbVec2f_array($input, temp);
  $1 = temp;
}

%rename(setValue_vec) SoMFVec2f::setValue(SbVec2f const &);
%rename(setValue_ff) SoMFVec2f::setValue(const float x, const float y);

%feature("shadow") SoMFVec2f::setValue(const float xy[2]) %{
def setValue(*args):
   if isinstance(args[1], SbVec2f):
      return apply(pivyc.SoMFVec2f_setValue_vec,args)
   elif len(args) == 3:
      return apply(pivyc.SoMFVec2f_setValue_ff,args)
   return apply(pivyc.SoMFVec2f_setValue,args)
%}

%rename(set1Value_i_vec) SoMFVec2f::set1Value(int const ,SbVec2f const &);
%rename(set1Value_i_ff) SoMFVec2f::set1Value(const int idx, const float x, const float y);

%feature("shadow") SoMFVec2f::set1Value(const int idx, const float xy[2]) %{
def set1Value(*args):
   if isinstance(args[2], SbVec2f):
      return apply(pivyc.SoMFVec2f_set1Value_i_vec,args)
   elif len(args) == 4:
      return apply(pivyc.SoMFVec2f_set1Value_i_ff,args)
   return apply(pivyc.SoMFVec2f_set1Value,args)
%}

%rename(setValues_i_i_vec) SoMFVec2f::setValues(int const ,int const ,SbVec2f const *);

%feature("shadow") SoMFVec2f::setValues(const int start, const int num, const float xyz[][2]) %{
def setValues(*args):
   if isinstance(args[3], SbVec2f):
      return apply(pivyc.SoMFVec2f_setValues_i_i_vec,args)
   return apply(pivyc.SoMFVec2f_setValues,args)
%}
#endif

class COIN_DLL_API SoMFVec2f : public SoMField {
  typedef SoMField inherited;

  SO_MFIELD_HEADER(SoMFVec2f, SbVec2f, const SbVec2f &);

public:
  static void initClass(void);

  void setValues(const int start, const int num, const float xy[][2]);
  void set1Value(const int idx, const float x, const float y);
  void set1Value(const int idx, const float xy[2]);
  void setValue(const float x, const float y);

#ifdef __PIVY__
  %extend {
        void __call__(float xy[2]) {
          self->setValue(xy);
        }
  }
#endif

  void setValue(const float xy[2]);
};

#endif // !COIN_SOMFVEC2F_H
