#ifndef COIN_SOPIVYSCRIPT_H
#define COIN_SOPIVYSCRIPT_H

#include <Inventor/fields/SoSFString.h>
#include <Inventor/fields/SoSFVec3f.h>
#include <Inventor/nodes/SoSubNode.h>

class COIN_DLL_API SoPyScript : public SoNode {
  typedef SoNode inherited;
    
public:
  static void initClass(void);
  SoPyScript(void);
  
  static SoType getClassTypeId(void);
  virtual SoType getTypeId(void) const;

  SoSFString script; // holds the Python script

  static SoPyScript * soPyScriptInstance;

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

private:
  static SoType classTypeId;
  static void * createInstance(void);
  virtual SbBool readInstance(SoInput * in, unsigned short flags);
  virtual const SoFieldData * getFieldData(void) const;

  SoFieldData * fielddata;
  void * thread_state;
  void * globalModuleDict;
};

#endif // !COIN_SOPIVYSCRIPT_H
