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

#ifndef COIN_SOSFROTATION_H
#define COIN_SOSFROTATION_H

#include <Inventor/fields/SoSField.h>
#include <Inventor/fields/SoSubField.h>
#include <Inventor/SbRotation.h>

#ifdef __PIVY__
%typemap(in) float q[4] (float temp[4]) {
  convert_SbVec4f_array($input, temp);
  $1 = temp;
}

%rename(setValue_rot) SoSFRotation::setValue(SbRotation const &);
%rename(setValue_ffff) SoSFRotation::setValue(const float q0, const float q1, const float q2, const float q3);
%rename(setValue_array) SoSFRotation::setValue(const float q[4]);

%feature("shadow") SoSFRotation::setValue(const SbVec3f & axis, const float angle) %{
def setValue(*args):
   if len(args) == 5:
      return apply(pivyc.SoSFRotation_setValue_ffff,args)
   if len(args) == 2:
      if isinstance(args[1], SbRotation):
         return apply(pivyc.SoSFRotation_setValue_rot,args)
      else:
         return apply(pivyc.SoSFRotation_setValue_array,args)
   return apply(pivyc.SoSFRotation_setValue,args)
%}
#endif

class COIN_DLL_API SoSFRotation : public SoSField {
  typedef SoSField inherited;

  SO_SFIELD_HEADER(SoSFRotation, SbRotation, const SbRotation &);

public:
  static void initClass(void);

#ifdef __PIVY__
  %addmethods {
	void __call__(float q[4]) {
	  self->setValue(q);
	}
  }
#endif

  void getValue(SbVec3f & axis, float & angle) const;
  void setValue(const float q0, const float q1, const float q2, const float q3);
  void setValue(const float q[4]);
  void setValue(const SbVec3f & axis, const float angle);
};

#endif // !COIN_SOSFROTATION_H
