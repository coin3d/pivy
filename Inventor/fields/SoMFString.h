#ifndef COIN_SOMFSTRING_H
#define COIN_SOMFSTRING_H

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
#include <Inventor/SbString.h>

#ifdef __PIVY__
%typemap(in) const char * strings[] {
  int i;

  /* check if the sequence really matches the expected length */
  if (PySequence_Size(obj3) < arg3) {
    PyErr_SetString(PyExc_ValueError, "provided sequence is smaller than num");
    return NULL;
  }

  $1 = (char **)malloc(arg3*sizeof(char *));
  for (i=0; i < arg3; i++) {
    PyObject *item = PySequence_GetItem(obj3,i);
    if (!PyString_Check(item)) {
        free($1);
        PyErr_SetString(PyExc_ValueError, "list items must be strings");
        return NULL;
    }
    $1[i] = PyString_AsString(item);
  }
}

%rename(setValues_i_i_str) SoMFString::setValues(int const ,int const ,SbString const *);

%feature("shadow") SoMFString::setValues(const int start, const int num, const char * strings[]) %{
def setValues(*args):
   if isinstance(args[3], SbString):
      return apply(_pivy.SoMFString_setValues_i_i_str,args)
   return apply(_pivy.SoMFString_setValues,args)
%}
#endif

class COIN_DLL_API SoMFString : public SoMField {
  typedef SoMField inherited;

  SO_MFIELD_HEADER(SoMFString, SbString, const SbString &);

public:
  static void initClass(void);

#ifdef __PIVY__
  %extend {
	void __call__(char * str) {
	  self->setValue(str);
	}
  }
#endif

  void setValues(const int start, const int num, const char * strings[]);
  void setValue(const char * string);
  void deleteText(const int fromline, const int fromchar,
                  const int toline, const int tochar);
};

#endif // !COIN_SOMFSTRING_H
