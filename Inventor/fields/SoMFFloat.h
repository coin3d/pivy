#ifndef COIN_SOMFFLOAT_H
#define COIN_SOMFFLOAT_H

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

#ifdef __PIVY__
%{
static void
convert_SoMFFloat_array(PyObject *input, int len, float *temp)
{
  int i;

  for (i=0; i<len; i++) {
	PyObject *oi = PySequence_GetItem(input,i);
	if (PyNumber_Check(oi)) {
	  temp[i] = (float) PyFloat_AsDouble(oi);
	} else {
	  PyErr_SetString(PyExc_ValueError,"Sequence elements must be floats");
	  free(temp);       
	  return;
	}
  }
  return;
}
%}

%typemap(in) float * (float *temp) {
  int len;

  if (PySequence_Check($input)) {
	len = PySequence_Length($input);
	temp = (float *) malloc(len*sizeof(float));
	convert_SoMFFloat_array($input, len, temp);
  
	$1 = temp;
  } else {
	PyErr_SetString(PyExc_TypeError, "expected a sequence.");
  }
}
#endif

class COIN_DLL_API SoMFFloat : public SoMField {
  typedef SoMField inherited;

  SO_MFIELD_HEADER(SoMFFloat, float, float);

  SO_MFIELD_SETVALUESPOINTER_HEADER(float);

public:
  static void initClass(void);

#ifdef __PIVY__
  %extend {
	void __call__(float i) {
	  self->setValue(i);
	}
  }
#endif

private:
  virtual int getNumValuesPerLine(void) const;
};

#endif // !COIN_SOMFFLOAT_H
