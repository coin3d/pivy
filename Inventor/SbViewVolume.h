#ifndef COIN_SBVIEWVOLUME_H
#define COIN_SBVIEWVOLUME_H

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

#include <stdio.h>

#include <Inventor/SbBasic.h>
#include <Inventor/SbVec3f.h>
#include <Inventor/SbDPViewVolume.h>

class SbBox3f;
class SbLine;
class SbMatrix;
class SbPlane;
class SbRotation;
class SbVec2f;
class SbVec3f;

#ifdef __PIVY__
%typemap(in) (const SbVec2f& pt, SbVec3f& line0, SbVec3f& line1) {
  if ((SWIG_ConvertPtr(obj1,(void **) &arg2, SWIGTYPE_p_SbVec2f,SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
  if (arg2 == NULL) {
    PyErr_SetString(PyExc_TypeError,"null reference"); SWIG_fail; 
  }
  $2 = new SbVec3f();
  $3 = new SbVec3f();
}

%typemap(argout) (SbVec3f& line0, SbVec3f& line1) {
  PyObject *o1, *o2;
  o1 = SWIG_NewPointerObj((void *) $1, $1_descriptor, 1);
  o2 = SWIG_NewPointerObj((void *) $2, $2_descriptor, 1);

  $result = PyTuple_New(2);
  PyTuple_SetItem($result, 0, o1);
  PyTuple_SetItem($result, 1, o2);
}

%typemap(in) (const SbVec3f& src, SbVec3f& dst) {
  if ((SWIG_ConvertPtr(obj1,(void **) &arg2, SWIGTYPE_p_SbVec3f,SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
  if (arg2 == NULL) {
    PyErr_SetString(PyExc_TypeError,"null reference"); SWIG_fail; 
  }
  $2 = new SbVec3f();
}

%typemap(argout) (const SbVec3f& src, SbVec3f& dst) {
  $result = SWIG_NewPointerObj((void *) $1, $1_descriptor, 1);
}
#endif

class COIN_DLL_API SbViewVolume {
public:
  enum ProjectionType { ORTHOGRAPHIC = 0, PERSPECTIVE = 1 };

public:
  SbViewVolume(void);
  ~SbViewVolume(void);
  void getMatrices(SbMatrix& affine, SbMatrix& proj) const;
  SbMatrix getMatrix(void) const;
  SbMatrix getCameraSpaceMatrix(void) const;
#ifndef __PIVY__
  void projectPointToLine(const SbVec2f& pt, SbLine& line) const;
#endif
  void projectPointToLine(const SbVec2f& pt,
                          SbVec3f& line0, SbVec3f& line1) const;
  void projectToScreen(const SbVec3f& src, SbVec3f& dst) const;
  SbPlane getPlane(const float distFromEye) const;
  SbVec3f getSightPoint(const float distFromEye) const;
  SbVec3f getPlanePoint(const float distFromEye,
                        const SbVec2f& normPoint) const;
  SbRotation getAlignRotation(SbBool rightAngleOnly = FALSE) const;
  float getWorldToScreenScale(const SbVec3f& worldCenter,
                              float normRadius) const;
  SbVec2f projectBox(const SbBox3f& box) const;
  SbViewVolume narrow(float left, float bottom,
                      float right, float top) const;
  SbViewVolume narrow(const SbBox3f& box) const;
  void ortho(float left, float right,
             float bottom, float top,
             float nearval, float farval);
  void perspective(float fovy, float aspect,
                   float nearval, float farval);
  void frustum(float left, float right,
               float bottom, float top,
               float nearval, float farval);
  void rotateCamera(const SbRotation& q);
  void translateCamera(const SbVec3f& v);
  SbVec3f zVector(void) const;
  SbViewVolume zNarrow(float nearval, float farval) const;
  void scale(float factor);
  void scaleWidth(float ratio);
  void scaleHeight(float ratio);
  ProjectionType getProjectionType(void) const;
  const SbVec3f& getProjectionPoint(void) const;
  const SbVec3f& getProjectionDirection(void) const;
  float getNearDist(void) const;
  float getWidth(void) const;
  float getHeight(void) const;
  float getDepth(void) const;

  void print(FILE * fp) const;
  void getViewVolumePlanes(SbPlane planes[6]) const;
  void transform(const SbMatrix &matrix);
  SbVec3f getViewUp(void) const;

public:
  // Warning! It's extremely bad design to keep these data members
  // public, but we have no choice since this is how it's done in
  // the original SGI Open Inventor. We've seen example code that
  // use these variables directly so we'll have to be compatible
  // here. Please don't use these variables directly unless you're
  // very sure about what you're doing.
  ProjectionType type;
  SbVec3f projPoint;
  SbVec3f projDir;
  float nearDist;
  float nearToFar;
  SbVec3f llf;
  SbVec3f lrf;
  SbVec3f ulf;

private:
  
  SbDPViewVolume dpvv;
};

#endif // !COIN_SBVIEWVOLUME_H
