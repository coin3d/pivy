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

#ifndef COIN_SOSFVEC2F_H
#define COIN_SOSFVEC2F_H

#include <Inventor/fields/SoSField.h>
#include <Inventor/fields/SoSubField.h>
#include <Inventor/SbVec2f.h>

#ifdef __PIVY__
%typemap(in) float xy[2] (float temp[2]) {
  convert_SbVec2f_array($input, temp);
  $1 = temp;
}

%rename(setValue_ff) SoSFVec2f::setValue(const float x, const float y);
%rename(setValue_vec) SoSFVec2f::setValue(SbVec2f const &);

%feature("shadow") SoSFVec2f::setValue(const float xy[2]) %{
def setValue(*args):
   if len(args) == 3:
      return apply(pivyc.SoSFVec2f_setValue_ff,args)
   elif isinstance(args[1],SbVec2f):
      return apply(pivyc.SoSFVec2f_setValue_vec,args)
   return apply(pivyc.SoSFVec2f_setValue,args)
%}
#endif

class COIN_DLL_API SoSFVec2f : public SoSField {
  typedef SoSField inherited;

  SO_SFIELD_HEADER(SoSFVec2f, SbVec2f, const SbVec2f &);

public:
  static void initClass(void);

#ifdef __PIVY__
  %addmethods {
        void __call__(float xy[2]) {
          self->setValue(xy);
        }
  }
#endif

  void setValue(const float x, const float y);
  void setValue(const float xy[2]);
};

#endif // !COIN_SOSFVEC2F_H
