#ifndef COIN_SOOFFSCREENRENDERER_H
#define COIN_SOOFFSCREENRENDERER_H

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

#include <Inventor/SbViewportRegion.h>
#include <Inventor/SbColor.h>
#include <Inventor/lists/SbList.h>
#include <Inventor/SbString.h>
#include <Inventor/SbName.h>

#include <stdio.h>

class SoBase;
class SoGLRenderAction;
class SoNode;
class SoPath;

// This shouldn't strictly be necessary, but the OSF1/cxx compiler
// complains if this is left out, while using the "friend class
// SoExtSelectionP" statement in the class definition.
class SoOffscreenRendererP;

#ifdef __PIVY__
%rename(SoOffscreenRenderer_gl) SoOffscreenRenderer::SoOffscreenRenderer(SoGLRenderAction * action);

%feature("shadow") SoOffscreenRenderer::SoOffscreenRenderer %{
def __init__(self,*args):
   if isinstance(args[0], SoGLRenderAction):
      self.this = apply(_pivy.new_SoOffscreenRenderer_gl,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SoOffscreenRenderer,args)
   self.thisown = 1
%}

%rename(render_nod) SoOffscreenRenderer::render(SoNode * scene);

%feature("shadow") SoOffscreenRenderer::render(SoPath * scene) %{
def render(*args):
   if isinstance(args[1], SoNode):
      return apply(_pivy.SoOffscreenRenderer_render_nod,args)
   return apply(_pivy.SoOffscreenRenderer_render,args)
%}

%rename(writeToPostScript_fil_vec) SoOffscreenRenderer::writeToPostScript(FILE * fp, const SbVec2f & printsize) const;
%rename(writeToPostScript_chr) SoOffscreenRenderer::writeToPostScript(const char * filename) const;
%rename(writeToPostScript_chr_vec) SoOffscreenRenderer::writeToPostScript(const char * filename, const SbVec2f & printsize) const;

%feature("shadow") SoOffscreenRenderer::writeToPostScript(FILE * fp) const %{
def writeToPostScript(*args):
   if len(args) == 3:
      if isinstance(args[2], SbVec2f):
         return apply(_pivy.SoOffscreenRenderer_writeToPostScript_fil_vec,args)
      else:
         return apply(_pivy.SoOffscreenRenderer_writeToPostScript_chr_vec,args)
   elif type(args[1]) == type(""):
         return apply(_pivy.SoOffscreenRenderer_writeToPostScript_chr,args)
   return apply(_pivy.SoOffscreenRenderer_writeToPostScript,args)
%}

%rename(writeToRGB_chr) SoOffscreenRenderer::writeToRGB(FILE * fp) const;

%feature("shadow") SoOffscreenRenderer::writeToRGB(const char * filename) const %{
def writeToRGB(*args):
   if type(args[1]) == type(""):
         return apply(_pivy.SoOffscreenRenderer_writeToRGB_chr,args)
   return apply(_pivy.SoOffscreenRenderer_writeToRGB,args)
%}
#endif

class COIN_DLL_API SoOffscreenRenderer {
public:
  enum Components {
    LUMINANCE = 1,
    LUMINANCE_TRANSPARENCY = 2,
    RGB = 3,
    RGB_TRANSPARENCY = 4
  };

  SoOffscreenRenderer(const SbViewportRegion & viewportregion);
  SoOffscreenRenderer(SoGLRenderAction * action);
  ~SoOffscreenRenderer();

  static float getScreenPixelsPerInch(void);
  static SbVec2s getMaximumResolution(void);
  void setComponents(const Components components);
  Components getComponents(void) const;
  void setViewportRegion(const SbViewportRegion & region);
  const SbViewportRegion & getViewportRegion(void) const;
  void setBackgroundColor(const SbColor & color);
  const SbColor & getBackgroundColor(void) const;
  void setGLRenderAction(SoGLRenderAction * action);
  SoGLRenderAction * getGLRenderAction(void) const;
  SbBool render(SoNode * scene);
  SbBool render(SoPath * scene);
  unsigned char * getBuffer(void) const;

  SbBool writeToRGB(FILE * fp) const;
  SbBool writeToPostScript(FILE * fp) const;
  SbBool writeToPostScript(FILE * fp, const SbVec2f & printsize) const;

  SbBool writeToRGB(const char * filename) const;
  SbBool writeToPostScript(const char * filename) const;
  SbBool writeToPostScript(const char * filename, const SbVec2f & printsize) const;
  
  SbBool isWriteSupported(const SbName & filetypeextension) const;
  int getNumWriteFiletypes(void) const;
  void getWriteFiletypeInfo(const int idx,
                            SbList <SbName> & extlist,
                            SbString & fullname,
                            SbString & description);
  SbBool writeToFile(const SbString & filename, const SbName & filetypeextension) const; 

private:
  friend class SoOffscreenRendererP;
  class SoOffscreenRendererP * pimpl;
};

#endif // !COIN_SOOFFSCREENRENDERER_H
