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
 *   as cheating from my side. very very very breakable, but works... *sigh*
 *   20030312 tamer.
 */
%typemap(in) (const unsigned char * pixels) {
  int i;

  short dim0=0; short dim1=0;
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
        PyErr_SetString(PyExc_ValueError, "list items must be strings");
        return NULL;
    }
    $1[i] = (unsigned char)PyInt_AsLong(item);
  }
}
/*
 * FIXME: find a way to supply a sequence as a return value for getValue().
 *   problems: how would one calculate the dimensions out of nothing and how
 *   would one apply the %typemap only for this case? muh? 20030312 tamer.
 */
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

  const unsigned char * getValue(SbVec2s & size, int & nc) const;
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

#endif // !COIN_SOSFIMAGE_H
