/**
 * Copyright (C) 2002-2004, Tamer Fahmy <tamer@tammura.at>
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

#include <Python.h>
#include <assert.h>

#include <Inventor/C/tidbits.h>
#include <Inventor/actions/SoAudioRenderAction.h>
#include <Inventor/actions/SoCallbackAction.h>
#include <Inventor/actions/SoGetBoundingBoxAction.h>
#include <Inventor/actions/SoGetMatrixAction.h>
#include <Inventor/actions/SoGLRenderAction.h>
#include <Inventor/actions/SoHandleEventAction.h>
#include <Inventor/actions/SoPickAction.h>
#include <Inventor/actions/SoGetPrimitiveCountAction.h>
#include <Inventor/actions/SoRayPickAction.h>
#include <Inventor/actions/SoSearchAction.h>
#include <Inventor/actions/SoWriteAction.h>
#include <Inventor/errors/SoDebugError.h>
#include <Inventor/errors/SoReadError.h>
#include <Inventor/sensors/SoOneShotSensor.h>

#include "SoPyScript.h"

/* SWIG runtime definitions */
typedef void *(*swig_converter_func)(void *);
typedef struct swig_type_info *(*swig_dycast_func)(void **);

typedef struct swig_type_info {
  const char * name;
  swig_converter_func converter;
  const char * str;
  void * clientdata;
  swig_dycast_func dcast;
  struct swig_type_info * next;
  struct swig_type_info * prev;
} swig_type_info;

#define SWIG_NewPointerObj SWIG_Python_NewPointerObj
#define SWIG_TypeQuery SWIG_Python_TypeQuery

extern "C" {
PyObject * SWIG_Python_NewPointerObj(void *, swig_type_info *,int own);
swig_type_info * SWIG_TypeQuery(const char *);
}

class SoPyScriptP {
public:
  SoPyScriptP(SoPyScript * master) {
    this->oneshotsensor = new SoOneShotSensor(SoPyScript::eval_cb, master);
    this->isReading = FALSE;
  }
  ~SoPyScriptP() {
    delete this->oneshotsensor;
  }

  PyObject *
  createPySwigType(SbString typeVal, void * obj) {
    swig_type_info * swig_type = NULL;
    
    typeVal += " *";
    if ((swig_type = SWIG_TypeQuery(typeVal.getString())) == NULL) {
      /* try again by prefixing the typename with So */
      SbString soTypeVal("So");
      soTypeVal += typeVal;
      if ((swig_type = SWIG_TypeQuery(soTypeVal.getString())) == NULL) {
        return NULL;
      }
    }

    return SWIG_NewPointerObj(obj, swig_type, 0);
  }

  SbBool isReading;
  SoOneShotSensor * oneshotsensor;
  PyThreadState * thread_state;
  PyObject * globalModuleDict;
};

#define PRIVATE(_this_) (_this_)->pimpl

SoType SoPyScript::classTypeId;

void
SoPyScript::initClass(void)
{
  SoPyScript::classTypeId =
    SoType::createType(SoNode::getClassTypeId(),
                       SbName("SoPyScript"),
                       SoPyScript::createInstance,
                       SoNode::nextActionMethodIndex++);
  SoNode::setCompatibilityTypes(SoPyScript::getClassTypeId(),
                                SoNode::COIN_2_0|SoNode::COIN_2_2|SoNode::COIN_2_3|SoNode::COIN_2_4);

  Py_Initialize();
}

SoPyScript::SoPyScript(void)
  : fielddata(NULL)
{
  PRIVATE(this) = new SoPyScriptP(this);
  this->isBuiltIn = FALSE;
  assert(SoPyScript::classTypeId != SoType::badType());

  this->script.setValue(NULL);
  this->script.setContainer(this);

  this->mustEvaluate.setValue(FALSE);
  this->mustEvaluate.setContainer(this);

  this->initFieldData();
 
  if (!(PRIVATE(this)->thread_state = Py_NewInterpreter())) {
    SoDebugError::postWarning("SoPyScript::initClass",
                              "Creation of new sub-interpreter failed!");
  }

  if (PyRun_SimpleString("from pivy import *")) {
    SoDebugError::postWarning("SoPyScript::initClass",
                              "\n*Yuk!* The box containing a fierce looking python snake to drive\n"
                              "this node has arrived but was found to be empty! The Pivy module\n"
                              "required for the Python Scripting Node could not be successfully\n"
                              "imported! Check your setup and fix it so that the python snake can\n"
                              "happily wiggle and byte you in the ass...");
  }

  PyThreadState * tstate = PyThreadState_Swap(PRIVATE(this)->thread_state);
  Py_SetProgramName("SoPyScript");
  PRIVATE(this)->globalModuleDict = PyModule_GetDict(PyImport_AddModule("__main__"));

  /* shovel the the node itself on to the Python interpreter as self instance */
  swig_type_info * swig_type = 0;

  if ((swig_type = SWIG_TypeQuery("SoNode *")) == 0) {
    SoDebugError::post("SoPyScript::SoPyScript",
                       "SoNode type could not be found!");
  }

  /* add the field to the global dict */
  PyDict_SetItemString(PRIVATE(this)->globalModuleDict, 
                       "self",
                       SWIG_NewPointerObj(this, swig_type, 0));

  PyThreadState_Swap(tstate);
}

// Doc in parent
SoType
SoPyScript::getClassTypeId(void)
{
  return SoPyScript::classTypeId;
}

// Doc in parent
SoType
SoPyScript::getTypeId(void) const
{
  return SoPyScript::classTypeId;
}

SoPyScript::~SoPyScript()
{
  delete PRIVATE(this);

  Py_EndInterpreter(PRIVATE(this)->thread_state);

  const int n = this->fielddata->getNumFields();
  for (int i = 0; i < n; i++) {
    SoField * f = this->fielddata->getField(this, i);
    if (f != &this->script || f != &this->mustEvaluate) { delete f; }
  }
  delete this->fielddata;
}

// Doc in parent
void
SoPyScript::doAction(SoAction * action, const char * funcname)
{
  if (funcname && !script.isIgnored()) {
    PyThreadState * tstate = PyThreadState_Swap(PRIVATE(this)->thread_state);

    if (coin_getenv("PIVY_DEBUG")) {
      SoDebugError::postInfo("SoPyScript::doAction",
                             "%s called!", action->getTypeId().getName().getString());
    }

    /* convert the action instance to a Python object */
    SbString typeVal(action->getTypeId().getName().getString());

    PyObject * pyAction = NULL;
    if ((pyAction = PRIVATE(this)->createPySwigType(typeVal, action)) == NULL) {
      SoDebugError::post("SoPyScript::doAction",
                         "%s could not be created!",
                         typeVal.getString());
      inherited::doAction(action);
      return;
    }

    PyObject * func = PyDict_GetItemString(PRIVATE(this)->globalModuleDict, funcname);

    if (func) {
      if (!PyCallable_Check(func)) {
        SbString errMsg(funcname);
        errMsg += " is not a callable object!";
        PyErr_SetString(PyExc_TypeError, errMsg.getString());
      } else {
        PyObject * result;
        PyObject * argtuple = Py_BuildValue("(O)", pyAction);

        if ((result = PyEval_CallObject(func, argtuple)) == NULL) {
          PyErr_Print();
        }
        Py_XDECREF(result);
        Py_DECREF(argtuple);
      }
    }

    if (coin_getenv("PIVY_DEBUG")) {
      SoDebugError::postInfo("SoPyScript::doAction",
                             "funcname: %s, func: %p",
                             funcname, func);
    }

    Py_DECREF(pyAction);
    PyThreadState_Swap(tstate);
  }
  inherited::doAction(action);
}

// Doc in parent
void
SoPyScript::GLRender(SoGLRenderAction * action)
{
  SoPyScript::doAction(action, "GLRender");
  inherited::GLRender(action);
}

// Doc in parent
void
SoPyScript::GLRenderBelowPath(SoGLRenderAction * action)
{
  SoPyScript::doAction(action, "GLRenderBelowPath");
  inherited::GLRenderBelowPath(action);
}

// Doc in parent
void
SoPyScript::GLRenderInPath(SoGLRenderAction * action)
{
  SoPyScript::doAction(action, "GLRenderInPath");
  inherited::GLRenderInPath(action);
}

// Doc in parent
void
SoPyScript::GLRenderOffPath(SoGLRenderAction * action)
{
  SoPyScript::doAction(action, "GLRenderOffPath");
  inherited::GLRenderOffPath(action);
}

// Doc in parent
void
SoPyScript::callback(SoCallbackAction * action)
{
  SoPyScript::doAction(action, "callback");
  inherited::callback(action);
}

// Doc in parent
void
SoPyScript::getBoundingBox(SoGetBoundingBoxAction * action)
{
  SoPyScript::doAction(action, "getBoundingBox");
  inherited::getBoundingBox(action);
}

// Doc in parent
void
SoPyScript::getMatrix(SoGetMatrixAction * action)
{
  SoPyScript::doAction(action, "getMatrix");
  inherited::getMatrix(action);
}

// Doc in parent
void
SoPyScript::handleEvent(SoHandleEventAction * action)
{
  SoPyScript::doAction(action, "handleEvent");
  inherited::handleEvent(action);
}

// Doc in parent
void
SoPyScript::pick(SoPickAction * action)
{
  SoPyScript::doAction(action, "pick");
  inherited::pick(action);
}

// Doc in parent
void
SoPyScript::rayPick(SoRayPickAction * action)
{
  SoPyScript::doAction(action, "rayPick");
  inherited::rayPick(action);
}

// Doc in parent
void
SoPyScript::search(SoSearchAction * action)
{
  SoPyScript::doAction(action, "search");
  inherited::search(action);
}

// Doc in parent
void
SoPyScript::write(SoWriteAction * action)
{
  SoPyScript::doAction(action, "write");
  inherited::write(action);
}

// Doc in parent
void
SoPyScript::audioRender(SoAudioRenderAction * action)
{
  SoPyScript::doAction(action, "audioRender");
  inherited::audioRender(action);
}

// Doc in parent
void
SoPyScript::getPrimitiveCount(SoGetPrimitiveCountAction * action)
{
  SoPyScript::doAction(action, "getPrimitiveCount");
  inherited::getPrimitiveCount(action);
}

// Doc in parent
void
SoPyScript::copyContents(const SoFieldContainer * from,
                         SbBool copyConn)
{
  assert(from->isOfType(SoPyScript::getClassTypeId()));
  this->initFieldData();

  const SoPyScript * fromnode = (SoPyScript*) from;

  const SoFieldData * src = from->getFieldData();
  const int n = src->getNumFields();
  for (int i = 0; i < n; i++) {
    const SoField * f = src->getField(from, i);
    if (f != &fromnode->script &&
        f != &fromnode->mustEvaluate) {
      SoField * cp = (SoField*) f->getTypeId().createInstance();
      cp->setContainer(this);
      this->fielddata->addField(this, src->getFieldName(i), cp);
    }
  }
  inherited::copyContents(from, copyConn);
}

// Doc in parent
void 
SoPyScript::notify(SoNotList * list)
{
  if (!PRIVATE(this)->isReading) {
    SoField * f = list->getLastField();

    if (f == &this->mustEvaluate) {
      int pri = this->mustEvaluate.getValue() ? 0 : 
        SoDelayQueueSensor::getDefaultPriority();
      PRIVATE(this)->oneshotsensor->setPriority(pri);
    }
    else if (f == &this->script) {
      PyThreadState * tstate = PyThreadState_Swap(PRIVATE(this)->thread_state);

      /* strip out possible \r's that could come from win32 line endings */
      SbString src = script.getValue();
      SbString pyString;
      for (int i=0; i < script.getValue().getLength(); i++) {
        if (src[i] != '\r') { pyString += src[i]; }
      }

      PyRun_SimpleString((char *)pyString.getString());

      if (coin_getenv("PIVY_DEBUG")) {
        SoDebugError::postInfo("SoPyScript::readInstance",
                             "script executed at full length!");
      }

      PyThreadState_Swap(tstate);
    }
    else {
      PRIVATE(this)->oneshotsensor->schedule();
    }
  }
  inherited::notify(list);
}

// Doc in parent
void *
SoPyScript::createInstance(void)
{
  return (void*) new SoPyScript;
}

SbBool
SoPyScript::readInstance(SoInput * in, unsigned short flags)
{
  // avoid triggering the eval cb while reading the file.
  PRIVATE(this)->isReading = TRUE;

  SbString name, typeVal;

  /* read in the first string */
  if (in->read(typeVal) && typeVal == "fields") {
    if (in->read(typeVal) && typeVal == "[") {
    
      while (in->read(typeVal) && typeVal != "]") {
        SoType type = SoType::fromName(typeVal);
        
        /* if it denotes a valid type and is derived from SoField then
           read in the next string representing the name of the
           field */
        if (type != SoType::badType() && 
            type.isDerivedFrom(SoField::getClassTypeId()) &&
            in->read(name))
        {
          // check for a comma at the end and strip it off
          const SbString fieldname = 
            (name[name.getLength()-1] == ',') ? name.getSubString(0, name.getLength()-2) : name;

          /* skip the static fields */
          if (fieldname == "script" || fieldname == "mustEvaluate") { continue; }
          
          /* instantiate the field and conduct similar actions as the
             SO_NODE_ADD_FIELD macro */
          SoField * field = (SoField *)type.createInstance();
          field->setContainer(this);
          this->fielddata->addField(this, fieldname.getString(), field);

          PyThreadState * tstate = PyThreadState_Swap(PRIVATE(this)->thread_state);

          /* shovel the field instance on to the Python interpreter */
          PyObject * pyField = NULL;
          if ((pyField = PRIVATE(this)->createPySwigType(typeVal, field)) == NULL) {
            SoDebugError::post("SoPyScript::readInstance",
                               "field type %s could not be created!",
                               typeVal.getString());
            
            return FALSE;
          }

          /* add the field to the global dict */
          PyDict_SetItemString(PRIVATE(this)->globalModuleDict, 
                               fieldname.getString(),
                               pyField);

          PyThreadState_Swap(tstate);
        }
      }
    }
  }

  /* ...and let the regular readInstance() method parse the rest */
  SbBool ok = inherited::readInstance(in, flags);

  if (!ok) {
    // evaluate script
    PRIVATE(this)->oneshotsensor->schedule();
  }

  PyThreadState * tstate = PyThreadState_Swap(PRIVATE(this)->thread_state);

  /* strip out possible \r's that could come from win32 line endings */
  SbString src = script.getValue();
  SbString pyString;
  for (int i=0; i < script.getValue().getLength(); i++) {
    if (src[i] != '\r') { pyString += src[i]; }
  }
  
  PyRun_SimpleString((char *)pyString.getString());

  if (coin_getenv("PIVY_DEBUG")) {
    SoDebugError::postInfo("SoPyScript::readInstance",
                           "script executed at full length!");
  }

  PyThreadState_Swap(tstate);

  PRIVATE(this)->isReading = FALSE;

  return ok;
}

// Initializes the field data and adds the default fields.
void
SoPyScript::initFieldData(void)
{
  if (this->fielddata) delete this->fielddata;
  this->fielddata = new SoFieldData;
  this->fielddata->addField(this, "script", &this->script);
  this->fielddata->addField(this, "mustEvaluate", &this->mustEvaluate);
}

// Doc in parent
const SoFieldData *
SoPyScript::getFieldData(void) const
{
  return this->fielddata;
}

// callback for oneshotsensor
void 
SoPyScript::eval_cb(void * data, SoSensor *)
{
  SoPyScript * self = (SoPyScript*)data;
 
  PyThreadState * tstate = PyThreadState_Swap(PRIVATE(self)->thread_state);

  if (coin_getenv("PIVY_DEBUG")) {
    SoDebugError::postInfo("SoPyScript::eval_cb",
                           "eval_cb called!");
  }

  for (int i = 0; i < self->fielddata->getNumFields(); i++) {
    SoField * f = self->fielddata->getField(self, i);
    if (f != &self->script || f != &self->mustEvaluate) {
 
      if (f->getDirty()) {
        SbString funcname("handle_");
        funcname += self->fielddata->getFieldName(i).getString();
      
        PyObject * func = PyDict_GetItemString(PRIVATE(self)->globalModuleDict, 
                                               funcname.getString());
      
        if (coin_getenv("PIVY_DEBUG")) {
          SoDebugError::postInfo("SoPyScript::eval_cb",
                                 "funcname: %s, func: %p",
                                 funcname.getString(), func);
        }
      
        if (func) {
          if (!PyCallable_Check(func)) {
            SbString errMsg(funcname);
            errMsg += " is not a callable object!";
            PyErr_SetString(PyExc_TypeError, errMsg.getString());
          } else {
            PyObject * result;
            if ((result = PyEval_CallObject(func, NULL)) == NULL) {
              PyErr_Print();
            }
            Py_XDECREF(result);
          }
        }        
      }
    }
  }

  PyThreadState_Swap(tstate);
}

#undef PRIVATE
