/**
 * Copyright (C) 2002-2005, Tamer Fahmy <tamer@tammura.at>
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met:
 *   * Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *   * Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in
 *     the documentation and/or other materials provided with the
 *     distribution.
 *   * Neither the name of the copyright holder nor the names of its
 *     contributors may be used to endorse or promote products derived
 *     from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 **/

#ifndef PIVY_SOPYSCRIPT_H
#define PIVY_SOPYSCRIPT_H

#if defined(_WIN32) && defined(PYSCRIPT_DLL)
  #ifdef PYSCRIPT_EXPORTS
    #define PYSCRIPT_API __declspec(dllexport)
  #else
    #define PYSCRIPT_API __declspec(dllimport)
  #endif
#else
  #define PYSCRIPT_API
#endif


#include <Inventor/fields/SoSFBool.h>
#include <Inventor/fields/SoSFString.h>
#include <Inventor/nodes/SoSubNode.h>

class SoPyScript;
class SoPyScriptP;
class SoSensor;

typedef void SoPyScriptEvaluateCB(void * closure, SoPyScript * node);

class PYSCRIPT_API SoPyScript : public SoNode {
  typedef SoNode inherited;
    
public:
  static void initClass(void);
  SoPyScript(void);
  
  static SoType getClassTypeId(void);
  virtual SoType getTypeId(void) const;

  SoSFString script;     // holds the Python script
  SoSFBool mustEvaluate; // immediate or delayed evaluation

protected:
  virtual ~SoPyScript();

  virtual void doAction(SoAction * action, const char * funcname = NULL);
  virtual void GLRender(SoGLRenderAction * action);
  virtual void GLRenderBelowPath(SoGLRenderAction * action);
  virtual void GLRenderInPath(SoGLRenderAction * action);
  virtual void GLRenderOffPath(SoGLRenderAction * action);
  virtual void callback(SoCallbackAction * action);
  virtual void getBoundingBox(SoGetBoundingBoxAction * action);
  virtual void getMatrix(SoGetMatrixAction * action);
  virtual void handleEvent(SoHandleEventAction * action);
  virtual void pick(SoPickAction * action);
  virtual void rayPick(SoRayPickAction * action);
  virtual void search(SoSearchAction * action);
  virtual void write(SoWriteAction * action);
  virtual void audioRender(SoAudioRenderAction * action);
  virtual void getPrimitiveCount(SoGetPrimitiveCountAction * action);

  virtual void copyContents(const SoFieldContainer * from, SbBool copyconn);
  virtual void notify(SoNotList * list);

private:
  static SoType classTypeId;
  static void * createInstance(void);

  virtual SbBool readInstance(SoInput * in, unsigned short flags);

  SoFieldData * fielddata;
  void initFieldData(void);
  virtual const SoFieldData * getFieldData(void) const;

  void executePyScript(void);

  static void eval_cb(void * data, SoSensor *);

  SoPyScriptP * pimpl;
  friend class SoPyScriptP;
};

#endif // !PIVY_SOPYSCRIPT_H
