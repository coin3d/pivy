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

#ifndef COIN_SOPATH_H
#define COIN_SOPATH_H

#include <Inventor/misc/SoBase.h>
#include <Inventor/lists/SbList.h>
#include <Inventor/lists/SoNodeList.h>

#ifndef COIN_INTERNAL
// For SGI / TGS Open Inventor compile-time compatibility.
#include <Inventor/SoLists.h>
#endif // !COIN_INTERNAL


class SoWriteAction;
class SoNotList;
class SoInput;
class SoPathList;

#ifdef __PIVY__
%rename(SoPath_nod) SoPath::SoPath(SoNode * const head);
%rename(SoPath_pat) SoPath::SoPath(const SoPath & rhs);

%feature("shadow") SoPath::SoPath %{
def __init__(self,*args):
   if isinstance(args[0], SoNode):
      self.this = apply(pivyc.new_SoPath_nod,args)
      self.thisown = 1
      return
   elif isinstance(args[0], SoPath):
      self.this = apply(pivyc.new_SoPath_pat,args)
      self.thisown = 1
      return
   self.this = apply(pivyc.new_SoPath,args)
   self.thisown = 1
%}

%rename(append_nod) SoPath::append(SoNode * const node);
%rename(append_pat) SoPath::append(const SoPath * const frompath);

%feature("shadow") SoPath::append(const int childindex) %{
def append(*args):
   if isinstance(args[1], SoNode):
      return apply(pivyc.SoPath_append_nod,args)
   elif isinstance(args[1], SoPath):
      return apply(pivyc.SoPath_append_pat,args)
   return apply(pivyc.SoPath_append,args)
%}

%rename(getByName_nam_pal) SoPath::getByName(const SbName name, SoPathList & l);

%feature("shadow") SoPath::getByName(const SbName name) %{
def getByName(*args):
   if len(args) == 3:
      return apply(pivyc.SoPath_getByName_nam_pal,args)
   return apply(pivyc.SoPath_getByName,args)
%}
#endif

class COIN_DLL_API SoPath : public SoBase {
  typedef SoBase inherited;

public:
  static void initClass(void);

  SoPath(const int approxlength = 4);
  SoPath(SoNode * const head);
  SoPath(const SoPath & rhs);

#ifndef __PIVY__
  SoPath & operator=(const SoPath & rhs);
#endif

  static SoType getClassTypeId(void);
  virtual SoType getTypeId(void) const;

  void setHead(SoNode * const head);
  SoNode * getHead(void) const;
  void append(const int childindex);
  void append(SoNode * const node);
  void append(const SoPath * const frompath);
  void push(const int childindex);
  void pop(void);
  SoNode * getTail(void) const;
  SoNode * getNode(const int index) const;
  SoNode * getNodeFromTail(const int index) const;
  int getIndex(const int index) const;
  int getIndexFromTail(const int index) const;
  int getLength(void) const;
  void truncate(const int length);

  int findFork(const SoPath * const path) const;
  int findNode(const SoNode * const node) const;

  SbBool containsNode(const SoNode * const node) const;
  SbBool containsPath(const SoPath * const path) const;
  SoPath * copy(const int startfromnodeindex = 0, int numnodes = 0) const;
  friend COIN_DLL_API SbBool operator==(const SoPath & lhs, const SoPath & rhs);
  friend COIN_DLL_API SbBool operator!=(const SoPath & lhs, const SoPath & rhs);

  static SoPath * getByName(const SbName name);
  static int getByName(const SbName name, SoPathList & l);

  void insertIndex(SoNode * const parent, const int newindex);
  void removeIndex(SoNode * const parent, const int oldindex);
  void replaceIndex(SoNode * const parent, const int index,
                    SoNode * const newchild);
  SbBool isRelevantNotification(SoNotList * const l) const;

  virtual void write(SoWriteAction * action);

protected:
  virtual ~SoPath();
  void auditPath(const SbBool flag);

private:
  static void * createInstance(void);
  void append(SoNode * const node, const int index);
  int getFullLength(void) const;
  void truncate(const int length, const SbBool donotify);
  virtual SbBool readInstance(SoInput * in, unsigned short flags);
  void setFirstHidden(void);

  SoNodeList nodes;
  SbList<int> indices;
  SbBool isauditing;
  int firsthidden;
  SbBool firsthiddendirty;
  static SoType classTypeId;

  friend class SoFullPath;
  friend class SoNodeKitPath;
  friend class SoAction;
  friend class SoTempPath;
};

/// inlined methods, block start //////////////////////////////////////////

inline int
SoPath::getFullLength(void) const
{
  return this->nodes.getLength();
}

inline void
SoPath::push(const int childindex)
{
  this->append(childindex);
}

inline void
SoPath::pop(void)
{
  this->truncate(this->getFullLength() - 1);
}

/// inlined methods, block end ////////////////////////////////////////////


#ifndef COIN_INTERNAL
// For SGI / TGS Open Inventor compile-time compatibility.
#include <Inventor/SoFullPath.h>
#include <Inventor/misc/SoLightPath.h>
#endif // COIN_INTERNAL

#endif // !COIN_SOPATH_H
