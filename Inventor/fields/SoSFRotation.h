#ifndef COIN_SOSFROTATION_H
#define COIN_SOSFROTATION_H

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
      return apply(_pivy.SoSFRotation_setValue_ffff,args)
   if len(args) == 2:
      if isinstance(args[1], SbRotation):
         return apply(_pivy.SoSFRotation_setValue_rot,args)
      else:
         return apply(_pivy.SoSFRotation_setValue_array,args)
   return apply(_pivy.SoSFRotation_setValue,args)
%}
#endif

class COIN_DLL_API SoSFRotation : public SoSField {
  typedef SoSField inherited;

  SO_SFIELD_HEADER(SoSFRotation, SbRotation, const SbRotation &);

public:
  static void initClass(void);

#ifdef __PIVY__
  %extend {
	void __call__(SbVec3f & axis, float angle) {
	  self->setValue(axis, angle);
	}
  }
#endif

  void getValue(SbVec3f & axis, float & angle) const;
  void setValue(const float q0, const float q1, const float q2, const float q3);
  void setValue(const float q[4]);
  void setValue(const SbVec3f & axis, const float angle);
};

#endif // !COIN_SOSFROTATION_H
