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

#ifndef COIN_SOSFVEC3F_H
#define COIN_SOSFVEC3F_H

#include <Inventor/fields/SoSField.h>
#include <Inventor/fields/SoSubField.h>
#include <Inventor/SbVec3f.h>

#ifdef __PIVY__
%typemap(in) float xyz[3] (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%rename(setValue_fff) SoSFVec3f::setValue(const float x, const float y, const float z);
%rename(setValue_vec) SoSFVec3f::setValue(SbVec3f const &);

%feature("shadow") SoSFVec3f::setValue(const float xyz[3]) %{
def setValue(*args):
   if len(args) == 4:
      return apply(pivyc.SoSFVec3f_setValue_fff,args)
   elif isinstance(args[1],SbVec3f):
      return apply(pivyc.SoSFVec3f_setValue_vec,args)
   return apply(pivyc.SoSFVec3f_setValue,args)
%}
#endif

class COIN_DLL_API SoSFVec3f : public SoSField {
  typedef SoSField inherited;

  SO_SFIELD_HEADER(SoSFVec3f, SbVec3f, const SbVec3f &);

public:
  static void initClass(void);

#ifdef __PIVY__
  %extend {
        void __call__(float xyz[3]) {
          self->setValue(xyz);
        }
  }
#endif

  void setValue(const float x, const float y, const float z);
  void setValue(const float xyz[3]);
};

#endif // !COIN_SOSFVEC3F_H
