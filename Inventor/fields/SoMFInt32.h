#ifndef COIN_SOMFINT32_H
#define COIN_SOMFINT32_H

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
convert_SoMFInt32_array(PyObject *input, int len, int32_t *temp)
{
  int i;

  for (i=0; i<len; i++) {
	PyObject *oi = PySequence_GetItem(input,i);
	if (PyNumber_Check(oi)) {
	  temp[i] = (int32_t) PyInt_AsLong(oi);
	} else {
	  PyErr_SetString(PyExc_ValueError,"Sequence elements must be numbers");
	  free(temp);       
	  return;
	}
  }
  return;
}
%}

%typemap(in) int32_t * (int32_t *temp) {
  int len;

  if (PySequence_Check($input)) {
	len = PySequence_Length($input);
	temp = (int32_t *) malloc(len*sizeof(int32_t));
	convert_SoMFInt32_array($input, len, temp);
  
	$1 = temp;
  } else {
	PyErr_SetString(PyExc_TypeError, "expected a sequence.");
  }
}
#endif

class COIN_DLL_API SoMFInt32 : public SoMField {
  typedef SoMField inherited;

  SO_MFIELD_HEADER(SoMFInt32, int32_t, int32_t);

  SO_MFIELD_SETVALUESPOINTER_HEADER(int32_t);

public:
  static void initClass(void);

#ifdef __PIVY__
  %extend {
        void __call__(int i) {
          self->setValue(i);
        }
  }
#endif

private:
  virtual int getNumValuesPerLine(void) const;
};

#endif // !COIN_SOMFINT32_H
