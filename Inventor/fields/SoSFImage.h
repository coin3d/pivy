#ifndef COIN_SOSFIMAGE_H
#define COIN_SOSFIMAGE_H

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

#include <Inventor/fields/SoSField.h>
#include <Inventor/fields/SoSubField.h>
#include <Inventor/SbVec2s.h>

#ifdef __PIVY__
/**
 * FIXME: this %typemap is relying on the fact that it really applies only
 *   for setValue(). we are lucky this time but it is certainly not clean
 *   and relies on the deep knowledge in how SWIG generates its code aka
 *   cheating from my side. very very very breakable, but works... *sigh*
 *   20030312 tamer.
 */
%typemap(in) const unsigned char * pixels {
  int i;

  short dim0, dim1;
  arg2->getValue(dim0,dim1);

  /* check if the sequence really matches the expected length */
  if (PySequence_Size(obj3) != dim0 * dim1 * arg3) {
    PyErr_SetString(PyExc_ValueError, "provided sequence does not match calculated length");
    return NULL;
  }

  $1 = (unsigned char *)malloc(dim0 * dim1 * arg3);
  for (i=0; i < dim0 * dim1 * arg3; i++) {
    PyObject *item = PySequence_GetItem(obj3,i);
    if (!PyInt_Check(item)) {
        free($1);
        PyErr_SetString(PyExc_ValueError, "list items must be integers");
        return NULL;
    }
    $1[i] = (unsigned char)PyInt_AsLong(item);
  }
}
/*
 * FIXME: the following %typemaps share the same problems like the one for
 *   setValue() and they are ugly as hell! shame on me, but it works! *eg*
 *   20030312 tamer.
 */
%typemap(in) (SbVec2s & size_output, int & OUTPUT) {
  int i = 0;
  $1 = new SbVec2s();
  $2 = &i;
}
%typemap(argout) SbVec2s & size_output {
  PyObject *o, *o2, *o3;

  o = SWIG_NewPointerObj((void *) $1, $1_descriptor, 1);

  if ((!$result) || ($result == Py_None)) {
        $result = o;
  } 
  else {
        if (!PyTuple_Check($result)) {
          PyObject *o2 = $result;
          $result = PyTuple_New(1);
          PyTuple_SetItem($result,0,o2);
        }
        o3 = PyTuple_New(1);
        PyTuple_SetItem(o3,0,o);
        o2 = $result;
        $result = PySequence_Concat(o2,o3);
        Py_DECREF(o2);
        Py_DECREF(o3);
  }
}
%typemap(out) const unsigned char * {
  int i;

  short dim0, dim1;
  arg2->getValue(dim0,dim1);

  $result = PyTuple_New(dim0 * dim1 * *arg3);
  
  for (i=0; i< dim0 * dim1 * *arg3; i++) {
	PyList_SetItem($result, i, PyInt_FromLong((long)(*($1+i))));
  }
}
#endif

class COIN_DLL_API SoSFImage : public SoSField {
  typedef SoSField inherited;

  SO_SFIELD_CONSTRUCTOR_HEADER(SoSFImage);
  SO_SFIELD_REQUIRED_HEADER(SoSFImage);

public:
  enum CopyPolicy {
    COPY,
    NO_COPY,
    NO_COPY_AND_DELETE,
    NO_COPY_AND_FREE
  };

  static void initClass(void);

#ifdef __PIVY__
  const unsigned char * getValue(SbVec2s & size_output, int & OUTPUT) const;
#else
  const unsigned char * getValue(SbVec2s & size, int & nc) const;
#endif
  void setValue(const SbVec2s & size, const int nc,
                const unsigned char * pixels, CopyPolicy copypolicy = COPY);

  int operator==(const SoSFImage & field) const;
  int operator!=(const SoSFImage & field) const { return ! operator == (field); }

  unsigned char * startEditing(SbVec2s & size, int & nc);
  void finishEditing(void);

  void setSubValue(const SbVec2s & dims, const SbVec2s & offset, unsigned char * pixels);
  void setSubValues(const SbVec2s * dims, const SbVec2s * offsets, int num, unsigned char ** pixelblocks);
  unsigned char * getSubTexture(int idx, SbVec2s & dims, SbVec2s & offset) const;
  SbBool hasSubTextures(int & numsubtextures);

  void setNeverWrite(SbBool flag);
  SbBool isNeverWrite(void) const;

  SbBool hasTransparency(void) const;

private:
  virtual SbBool readValue(SoInput * in);
  virtual void writeValue(SoOutput * out) const;

  class SoSFImageP * pimpl;
};

#ifdef __PIVY__
%typemap(in) const unsigned char * pixels;
%typemap(out) const unsigned char *;
#endif

#endif // !COIN_SOSFIMAGE_H
