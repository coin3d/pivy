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

#ifndef COIN_SBNAME_H
#define COIN_SBNAME_H

#include <Inventor/SbBasic.h>

class SbString;

#ifdef __PIVY__
%rename(SbName_char) SbName::SbName(const char * nameString);
%rename(SbName_str) SbName::SbName(const SbString & str);
%rename(SbName_name) SbName::SbName(const SbName & name);

%feature("shadow") SbName::SbName %{
def __init__(self,*args):
   if len(args) == 1:
      if isinstance(args[0], SbString):
         self.this = apply(pivyc.new_SbName_str,args)
         self.thisown = 1
         return
      elif isinstance(args[0], SbName):
         self.this = apply(pivyc.new_SbName_name,args)
         self.thisown = 1
         return
      else:
         self.this = apply(pivyc.new_SbName_char,args)
         self.thisown = 1
         return
   self.this = apply(pivyc.new_SbName,args)
   self.thisown = 1
%}
#endif

class COIN_DLL_API SbName {
public:
  SbName(void);
  SbName(const char * nameString);
  SbName(const SbString & str);
  SbName(const SbName & name);
  ~SbName(void);

  const char * getString(void) const;
  int getLength(void) const;
  static SbBool isIdentStartChar(const char c);
  static SbBool isIdentChar(const char c);
  static SbBool isBaseNameStartChar(const char c);
  static SbBool isBaseNameChar(const char c);

#ifndef __PIVY__
  int operator ! (void) const;
  friend COIN_DLL_API int operator == (const SbName & lhs, const char * rhs);
  friend COIN_DLL_API int operator == (const char * lhs, const SbName & rhs);
  friend COIN_DLL_API int operator == (const SbName & lhs, const SbName & rhs);
  friend COIN_DLL_API int operator != (const SbName & lhs, const char * rhs);
  friend COIN_DLL_API int operator != (const char * lhs, const SbName & rhs);
  friend COIN_DLL_API int operator != (const SbName & lhs, const SbName & rhs);

  operator const char * (void) const;
#endif

private:
  const class SbNameEntry * entry;
};

#ifdef __PIVY__
COIN_DLL_API int operator == (const SbName & lhs, const char * rhs);
COIN_DLL_API int operator == (const char * lhs, const SbName & rhs);
COIN_DLL_API int operator == (const SbName & lhs, const SbName & rhs);
COIN_DLL_API int operator != (const SbName & lhs, const char * rhs);
COIN_DLL_API int operator != (const char * lhs, const SbName & rhs);
COIN_DLL_API int operator != (const SbName & lhs, const SbName & rhs);
#endif

#endif // !COIN_SBNAME_H
