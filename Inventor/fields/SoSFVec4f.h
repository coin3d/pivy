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

#ifndef COIN_SOSFVEC4F_H
#define COIN_SOSFVEC4F_H

#include <Inventor/fields/SoSField.h>
#include <Inventor/fields/SoSubField.h>
#include <Inventor/SbVec4f.h>

#ifdef __PIVY__
%typemap(in) float xyzw[4] (float temp[4]) {
  convert_SbVec4f_array($input, temp);
  $1 = temp;
}

%rename(setValue_ffff) SoSFVec4f::setValue(const float x, const float y, const float z, const float w);
%rename(setValue_vec) SoSFVec4f::setValue(SbVec4f const &);

%feature("shadow") SoSFVec4f::setValue(const float xyzw[4]) %{
def setValue(*args):
   if len(args) == 5:
      return apply(pivyc.SoSFVec4f_setValue_ffff,args)
   elif isinstance(args[1],SbVec4f):
      return apply(pivyc.SoSFVec4f_setValue_vec,args)
   return apply(pivyc.SoSFVec4f_setValue,args)
%}
#endif

class COIN_DLL_API SoSFVec4f : public SoSField {
  typedef SoSField inherited;

  SO_SFIELD_HEADER(SoSFVec4f, SbVec4f, const SbVec4f &);

public:
  static void initClass(void);

  void setValue(const float x, const float y, const float z, const float w);
  void setValue(const float xyzw[4]);
};

#endif // !COIN_SOSFVEC4F_H
