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

#ifndef COIN_SOMFINT32_H
#define COIN_SOMFINT32_H

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

public:
  static void initClass(void);

#ifdef __PIVY__
  %addmethods {
        void __call__(int i) {
          self->setValue(i);
        }
  }
#endif

private:
  virtual int getNumValuesPerLine(void) const;
};

#endif // !COIN_SOMFINT32_H
