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
#include "sopyscript_wrap.cxx"

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
#include <Inventor/C/tidbits.h>

#include "SoPyScript.h"

SoPyScript * SoPyScript::soPyScriptInstance = NULL;

static PyObject *
pyscript_getFieldNames(PyObject * self, PyObject * args)
{
  PyObject * foo = PyString_FromString("pyscript_getFieldNames");

#if 0
  for (int i=0, numFields = SoPyScript::soPyScriptInstance->getFieldData()->getNumFields(); i < numFields; i++) {
    SoPyScript::soPyScriptInstance->getFieldData()->getField(SoPyScript::soPyScriptInstance, i);
  }  
#endif

  return foo;
}

static PyMethodDef PyScriptMethods[] = {
  {"getFieldNames", pyscript_getFieldNames, METH_VARARGS,
   "Return the field names defined in the SoPyScript node."},
  {NULL, NULL, 0, NULL}
};

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
  SWIG_init();
}

SoPyScript::SoPyScript(void)
  : fielddata(NULL)
{
  this->isBuiltIn = FALSE;
  assert(SoPyScript::classTypeId != SoType::badType());

  this->script.setValue(NULL);
  this->script.setContainer(this);

  if (this->fielddata) delete this->fielddata;
  this->fielddata = new SoFieldData;
  this->fielddata->addField(this, "script", &this->script);
 
  if (!(thread_state = Py_NewInterpreter())) {
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

  PyThreadState * tstate = PyThreadState_Swap((PyThreadState*)thread_state);
  soPyScriptInstance = this;
  Py_InitModule("SoPyScript", PyScriptMethods);
  Py_SetProgramName("SoPyScript");
  this->globalModuleDict = PyModule_GetDict(PyImport_AddModule("__main__"));


  /* shovel the the node itself on to the Python interpreter as self instance */
  swig_type_info * swig_type = 0;

  if ((swig_type = SWIG_TypeQuery("SoPyScript *")) == 0) {
    SoDebugError::post("SoPyScript::SoPyScript",
                       "No SoPyscript SWIG type found!");        
  }

  /* add the field to the global dict */
  PyDict_SetItemString((PyObject*)this->globalModuleDict, 
                       "self",
                       SWIG_NewPointerObj((void *)this, swig_type, 0));

  PyThreadState_Swap(tstate);
}

SoPyScript::~SoPyScript()
{
  Py_EndInterpreter((PyThreadState*)thread_state);

  const int n = this->fielddata->getNumFields();
  for (int i = 0; i < n; i++) {
    SoField * f = this->fielddata->getField(this, i);
    if (f != &this->script) delete f;
  }
  delete this->fielddata;
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

// Doc in parent
void *
SoPyScript::createInstance(void)
{
  return (void*) new SoPyScript;
}

// Doc in parent
const SoFieldData *
SoPyScript::getFieldData(void) const
{
  return this->fielddata;
}

SbBool
SoPyScript::readInstance(SoInput * in, unsigned short flags)
{
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
          const char * fieldname = 
            (name[name.getLength()-1] == ',') ? name.getSubString(0, name.getLength()-2).getString() : name.getString();

          /* skip the script field */
          if (!strcmp(fieldname, "script")) { continue; }
          
          /* instantiate the field and conduct similar actions as the
             SO_NODE_ADD_FIELD macro */
          SoField * field = (SoField *)type.createInstance();
          field->setContainer(this);
          this->fielddata->addField(this, fieldname, field);

          /* shovel the field instance on to the Python interpreter */
          swig_type_info * swig_type = 0;

          /* FIXME: query if the So prefix is needed or not by calling
             the node->getIsBuiltIn() method. 20041012 tamer. */
          typeVal += " *";
          if ((swig_type = SWIG_TypeQuery(typeVal.getString())) == 0) {
            /* FIXME: if soTypeVal is created on the stack, the stack
               gets corrupted. why is this so, by the big fat ass of
               teutates??? 20041012 tamer. */
            /* try again by prefixing the typename with So */
            SbString * soTypeVal = new SbString("So");
            *soTypeVal += typeVal;
            if ((swig_type = SWIG_TypeQuery(soTypeVal->getString())) == 0) {
              SoDebugError::post("SoPyScript::readInstance",
                                 "%s unknown to Pivy!", typeVal.getString());
              
              return FALSE;
            }
            delete soTypeVal;
          }
          PyThreadState * tstate = PyThreadState_Swap((PyThreadState*)thread_state);
          soPyScriptInstance = this;

          /* add the field to the global dict */
          PyDict_SetItemString((PyObject*)this->globalModuleDict, 
                               fieldname,
                               SWIG_NewPointerObj((void *)field, swig_type, 0));
          PyThreadState_Swap(tstate);
        }
      }
    }
  }

  /* ...and let the regular readInstance() method parse the rest */
  SbBool ok = inherited::readInstance(in, flags);

  PyThreadState * tstate = PyThreadState_Swap((PyThreadState*)thread_state);
  soPyScriptInstance = this;
  PyRun_SimpleString((char *)script.getValue().getString());
  if (coin_getenv("PIVY_DEBUG")) {
    SoDebugError::postInfo("SoPyScript::readInstance",
                           "script executed at full length!");
  }
  PyThreadState_Swap(tstate);

  return ok;
}

void
SoPyScript::doAction(SoAction * action, const char * funcname)
{
  if (funcname && !script.isIgnored()) {
    PyThreadState * tstate = PyThreadState_Swap((PyThreadState*)thread_state);
    soPyScriptInstance = this;

    if (coin_getenv("PIVY_DEBUG")) {
      SoDebugError::postInfo("SoPyScript::doAction",
                             "%s called!", action->getTypeId().getName().getString());
      SoDebugError::postInfo("SoPyScript::doAction",
                             "threadstate=%p:%p", tstate, thread_state);
    }

    /* convert the action instance to a Python object */
    swig_type_info * swig_type = 0;

    SbString typeVal(action->getTypeId().getName().getString());

    /* FIXME: query if the So prefix is needed or not by calling
       the node->getIsBuiltIn() method. 20041012 tamer. */
    typeVal += " *";
    if ((swig_type = SWIG_TypeQuery(typeVal.getString())) == 0) {
      /* FIXME: if soTypeVal is created on the stack, the stack gets
         corrupted. why is this so, by the big fat ass of teutates??? 
         20041012 tamer. */
      /* try again by prefixing the typename with So */
      SbString * soTypeVal = new SbString("So");
      *soTypeVal += typeVal;
      if ((swig_type = SWIG_TypeQuery(soTypeVal->getString())) == 0) {
        SoDebugError::post("SoPyScript::doAction",
                           "%s unknown to Pivy!", typeVal.getString());        
      }
      delete soTypeVal;
    }

    if (coin_getenv("PIVY_DEBUG")) {
      SoDebugError::postInfo("SoPyScript::doAction",
                             "typeVal: %s", typeVal.getString());
    }

    PyObject * func = PyDict_GetItemString((PyObject*)this->globalModuleDict, funcname);
    PyObject * pyAction = NULL;

    if (swig_type) {
      pyAction = SWIG_NewPointerObj((void *) action, swig_type, 0);
    }

    PyObject * argtuple = NULL;
    argtuple = Py_BuildValue("(O)", pyAction);

    if (coin_getenv("PIVY_DEBUG")) {
      SoDebugError::postInfo("SoPyScript::doAction",
                             "funcname: %s, func: %p, argtuple: %p",
                             funcname, func, argtuple);
    }

    if (func && argtuple) {
      if (!PyCallable_Check(func)) {
        SbString errMsg(funcname);
        errMsg += " is not a callable object!";
        PyErr_SetString(PyExc_TypeError, errMsg.getString());
      } else {
        PyObject * result;
        if ((result = PyEval_CallObject(func, argtuple)) == NULL) {
          PyErr_Print();
        }
        Py_XDECREF(result);
      }

      Py_DECREF(argtuple);
      Py_DECREF(pyAction);
    }

    // PyRun_SimpleString((char *)script.getValue().getString());
    PyThreadState_Swap(tstate);
  }
  inherited::doAction(action);
}

void
SoPyScript::GLRender(SoGLRenderAction * action)
{
  SoPyScript::doAction(action, "GLRender");
  inherited::GLRender(action);
}

void
SoPyScript::GLRenderBelowPath(SoGLRenderAction * action)
{
  SoPyScript::doAction(action, "GLRenderBelowPath");
  inherited::GLRenderBelowPath(action);
}

void
SoPyScript::GLRenderInPath(SoGLRenderAction * action)
{
  SoPyScript::doAction(action, "GLRenderInPath");
  inherited::GLRenderInPath(action);
}

void
SoPyScript::GLRenderOffPath(SoGLRenderAction * action)
{
  SoPyScript::doAction(action, "GLRenderOffPath");
  inherited::GLRenderOffPath(action);
}

void
SoPyScript::callback(SoCallbackAction * action)
{
  SoPyScript::doAction(action, "callback");
  inherited::callback(action);
}

void
SoPyScript::getBoundingBox(SoGetBoundingBoxAction * action)
{
  SoPyScript::doAction(action, "getBoundingBox");
  inherited::getBoundingBox(action);
}

void
SoPyScript::getMatrix(SoGetMatrixAction * action)
{
  SoPyScript::doAction(action, "getMatrix");
  inherited::getMatrix(action);
}

void
SoPyScript::handleEvent(SoHandleEventAction * action)
{
  SoPyScript::doAction(action, "handleEvent");
  inherited::handleEvent(action);
}

void
SoPyScript::pick(SoPickAction * action)
{
  SoPyScript::doAction(action, "pick");
  inherited::pick(action);
}

void
SoPyScript::rayPick(SoRayPickAction * action)
{
  SoPyScript::doAction(action, "rayPick");
  inherited::rayPick(action);
}

void
SoPyScript::search(SoSearchAction * action)
{
  SoPyScript::doAction(action, "search");
  inherited::search(action);
}

void
SoPyScript::write(SoWriteAction * action)
{
  SoPyScript::doAction(action, "write");
  inherited::write(action);
}

void
SoPyScript::audioRender(SoAudioRenderAction * action)
{
  SoPyScript::doAction(action, "audioRender");
  inherited::audioRender(action);
}

void
SoPyScript::getPrimitiveCount(SoGetPrimitiveCountAction * action)
{
  SoPyScript::doAction(action, "getPrimitiveCount");
  inherited::getPrimitiveCount(action);
}
