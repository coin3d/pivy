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
%typemap(in) (SbVec2s & size, int & nc) {
  $1 = new SbVec2s();
  $2 = (int *)malloc(sizeof(int));
}
%typemap(out) const unsigned char * {
  PyObject *o;
  short dim0, dim1;
  arg2->getValue(dim0,dim1);

  o = SWIG_NewPointerObj((void *)arg2, SWIGTYPE_p_SbVec2s, 1);

  $result = PyTuple_New(2);
  PyTuple_SetItem($result, 0, PyString_FromStringAndSize((char *)$1, dim0 * dim1 * *arg3));
  PyTuple_SetItem($result, 1, o);
  free(arg3);
}

/* fake an input argument */
%feature("shadow") SoSFImage::getValue(SbVec2s & size, int & nc) const %{
def getValue(self):
   return apply(_pivy.SoSFImage_getValue,(self,0))
%}

%feature("shadow") SoSFImage::startEditing(SbVec2s & size, int & nc) %{
def startEditing(self):
   return apply(_pivy.SoSFImage_startEditing,(self,0))
%}
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

#ifdef __PIVY__
%typemap(in) const unsigned char * pixels;
%typemap(out) const unsigned char *;
#endif

#endif // !COIN_SOSFIMAGE_H