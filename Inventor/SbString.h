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

#ifndef COIN_SBSTRING_H
#define COIN_SBSTRING_H

#include <Inventor/system/inttypes.h>
#include <Inventor/SbBasic.h>

#include <stdio.h>
#include <stdarg.h>

#define SB_STRING_STATIC_STORAGE_SIZE 128

#ifdef __PIVY__
%rename(SbString_str) SbString::SbString(const char * str);
%rename(SbString_str_i_i) SbString::SbString(const char * str, int start, int end);
%rename(SbString_i) SbString::SbString(const int digits);

%feature("shadow") SbString::SbString %{
def __init__(self,*args):
   if len(args) == 1:
      if type(args[0]) == type(1):
         self.this = apply(pivyc.new_SbString_i,args)
         self.thisown = 1
         return
      else:
         self.this = apply(pivyc.new_SbString_str,args)
         self.thisown = 1
         return
   elif len(args) == 3:
      self.this = apply(pivyc.new_SbString_str_i_i,args)
      self.thisown = 1
      return
   self.this = apply(pivyc.new_SbString,args)
   self.thisown = 1
%}

%rename(hash_str) SbString::hash(const char * s);

%feature("shadow") SbString::hash(void) %{
def hash(*args):
   if len(args) == 2:
      return apply(pivyc.SbString_hash_str,args)
   return apply(pivyc.SbString_hash,args)
%}
#endif

class COIN_DLL_API SbString {
public:
  SbString(void);
  SbString(const char * str);
  SbString(const char * str, int start, int end);

#ifndef __PIVY__
  SbString(const SbString & str);
#endif

  SbString(const int digits);
  ~SbString();

  uint32_t hash(void);
  int getLength(void) const;
  void makeEmpty(SbBool freeold = TRUE);
  const char * getString(void) const;
  SbString getSubString(int startidx, int endidx = -1) const;
  void deleteSubString(int startidx, int endidx = -1);

  void addIntString(const int value);

#ifdef __PIVY__
  // add a method for wrapping c++ operator[] access
  %extend {
	float __getitem__(int i) {
	  return (self->getString())[i];
	}
  }
#else
  char operator [](int index) const;
  SbString & operator = (const char * str);
  SbString & operator = (const SbString & str);
  SbString & operator += (const char * str);
  SbString & operator += (const SbString & str);
  int operator ! (void) const;
  friend COIN_DLL_API int operator == (const SbString & str, const char * s);
  friend COIN_DLL_API int operator == (const char * s, const SbString & str);
  friend COIN_DLL_API int operator == (const SbString & str1, const SbString & str2);
  friend COIN_DLL_API int operator != (const SbString & str, const char * s);
  friend COIN_DLL_API int operator != (const char * s, const SbString & str);
  friend COIN_DLL_API int operator != (const SbString & str1, const SbString & str2);
#endif

  static uint32_t hash(const char * s);

  SbString & operator += (const char c);

#ifndef __PIVY__
  SbString & sprintf(const char * formatstr, ...);
  SbString & vsprintf(const char * formatstr, va_list args);
#endif

  void print(FILE * file = stdout) const;

private:
  char * sstring;
  int storagesize;
  char staticstorage[SB_STRING_STATIC_STORAGE_SIZE];
  void expand(int additional);
};

#ifndef __PIVY__
COIN_DLL_API int operator == (const SbString & str, const char * s);
COIN_DLL_API int operator == (const char * s, const SbString & str);
COIN_DLL_API int operator == (const SbString & str1, const SbString & str2);
COIN_DLL_API int operator != (const SbString & str, const char * s);
COIN_DLL_API int operator != (const char * s, const SbString & str);
COIN_DLL_API int operator != (const SbString & str1, const SbString & str2);
#endif

#ifndef COIN_INTERNAL
// For Open Inventor compatibility.
#include <Inventor/SbName.h>
#endif // !COIN_INTERNAL

#endif // !COIN_SBSTRING_H
