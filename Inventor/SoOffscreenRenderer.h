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

#ifndef COIN_SOOFFSCREENRENDERER_H
#define COIN_SOOFFSCREENRENDERER_H

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

#ifdef __PIVY__
%rename(SoOffscreenRenderer_gl) SoOffscreenRenderer::SoOffscreenRenderer(SoGLRenderAction * action);

%feature("shadow") SoOffscreenRenderer::SoOffscreenRenderer %{
def __init__(self,*args):
   if isinstance(args[0], SoGLRenderAction):
      self.this = apply(pivyc.new_SoOffscreenRenderer_gl,args)
      self.thisown = 1
      return
   self.this = apply(pivyc.new_SoOffscreenRenderer,args)
   self.thisown = 1
%}

%rename(render_nod) SoOffscreenRenderer::render(SoNode * scene);

%feature("shadow") SoOffscreenRenderer::render(SoPath * scene) %{
def render(*args):
   if isinstance(args[1], SoNode):
      return apply(pivyc.SoOffscreenRenderer_render_nod,args)
   return apply(pivyc.SoOffscreenRenderer_render,args)
%}

%rename(writeToPostScript_fil_vec) SoOffscreenRenderer::writeToPostScript(FILE * fp, const SbVec2f & printsize) const;
%rename(writeToPostScript_chr) SoOffscreenRenderer::writeToPostScript(const char * filename) const;
%rename(writeToPostScript_chr_vec) SoOffscreenRenderer::writeToPostScript(const char * filename, const SbVec2f & printsize) const;

%feature("shadow") SoOffscreenRenderer::writeToPostScript(FILE * fp) const %{
def writeToPostScript(*args):
   if len(args) == 3:
      if isinstance(args[2], SbVec2f):
         return apply(pivyc.SoOffscreenRenderer_writeToPostScript_fil_vec,args)
      else:
         return apply(pivyc.SoOffscreenRenderer_writeToPostScript_chr_vec,args)
   elif type(args[1]) == type(""):
         return apply(pivyc.SoOffscreenRenderer_writeToPostScript_chr,args)
   return apply(pivyc.SoOffscreenRenderer_writeToPostScript,args)
%}

%rename(writeToRGB_chr) SoOffscreenRenderer::writeToRGB(FILE * fp) const;

%feature("shadow") SoOffscreenRenderer::writeToRGB(const char * filename) const %{
def writeToRGB(*args):
   if type(args[1]) == type(""):
         return apply(pivyc.SoOffscreenRenderer_writeToRGB_chr,args)
   return apply(pivyc.SoOffscreenRenderer_writeToRGB,args)
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
  SbBool renderFromBase(SoBase * base);
  void convertBuffer(void);

  SbViewportRegion viewport;
  SbColor backgroundcolor;
  Components components;
  SoGLRenderAction * renderaction;
  SbBool didallocaction;
  class SoOffscreenInternalData * internaldata;
  unsigned char * buffer;
};


#endif // !COIN_SOOFFSCREENRENDERER_H
