%{
static SoCallbackAction::Response
SoIntersectionVisitationPythonCB(void * closure, 
                                 const SoPath * where)
{
  PyObject *func, *arglist;
  PyObject *result, *path;
  int iresult = 0;

  path = SWIG_NewPointerObj((void *) where, SWIGTYPE_p_SoPath, 1);

  /* the first item in the userdata sequence is the python callback
   * function; the second is the supplied userdata python object */
  func = PyTuple_GetItem((PyObject *)closure, 0);
  arglist = Py_BuildValue("OO", PyTuple_GetItem((PyObject *)closure, 1), path);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }
  else {
    iresult = PyInt_AsLong(result);
  }
  
  Py_DECREF(arglist);
  Py_XDECREF(result);

  return (SoCallbackAction::Response)iresult;
}


static SbBool
SoIntersectionFilterPythonCB(void * closure,
                             const SoPath * p1,
                             const SoPath * p2)
{   
  PyObject *func, *arglist;
  PyObject *result, *path1, *path2;
  int iresult = 0;

  path1 = SWIG_NewPointerObj((void *) p1, SWIGTYPE_p_SoPath, 1);
  path2 = SWIG_NewPointerObj((void *) p2, SWIGTYPE_p_SoPath, 1);

  /* the first item in the userdata sequence is the python callback
   * function; the second is the supplied userdata python object */
  func = PyTuple_GetItem((PyObject *)closure, 0);
  arglist = Py_BuildValue("OOO", PyTuple_GetItem((PyObject *)closure, 1), path1, path2);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }
  else {
    iresult = PyInt_AsLong(result);
  }
  
  Py_DECREF(arglist);
  Py_XDECREF(result);

  return (SbBool)iresult;
}

static SoIntersectionDetectionAction::Resp
SoIntersectionPythonCB(void * closure, 
                       const SoIntersectingPrimitive * p1, 
                       const SoIntersectingPrimitive * p2)
{
  PyObject *func, *arglist;
  PyObject *result, *primitive1, *primitive2;
  int iresult = 0;

  primitive1 = SWIG_NewPointerObj((void *) p1, SWIGTYPE_p_SoIntersectingPrimitive, 1);
  primitive2 = SWIG_NewPointerObj((void *) p2, SWIGTYPE_p_SoIntersectingPrimitive, 1);

  /* the first item in the userdata sequence is the python callback
   * function; the second is the supplied userdata python object */
  func = PyTuple_GetItem((PyObject *)closure, 0);
  arglist = Py_BuildValue("OOO", PyTuple_GetItem((PyObject *)closure, 1), primitive1, primitive2);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }
  else {
    iresult = PyInt_AsLong(result);
  }
  
  Py_DECREF(arglist);
  Py_XDECREF(result);

  return (SoIntersectionDetectionAction::Resp)iresult;
}
%}

%rename(apply_nod) SoIntersectionDetectionAction::apply(SoNode *root);
%rename(apply_pat) SoIntersectionDetectionAction::apply(SoPath *path);

%feature("shadow") SoIntersectionDetectionAction::apply(const SoPathList & paths, SbBool obeysRules = FALSE) %{
def apply(*args):
   if len(args) == 2:
      if isinstance(args[1], SoNode):
         return apply(_pivy.SoIntersectionDetectionAction_apply_nod,args)
      elif isinstance(args[1], SoPath):
         return apply(_pivy.SoIntersectionDetectionAction_apply_pat,args)
   return apply(_pivy.SoIntersectionDetectionAction_apply,args)
%}

/* add python specific callback functions */
%extend SoIntersectionDetectionAction {
  void addVisitationCallback(SoType type, PyObject * pyfunc, PyObject * closure) {
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, closure);
    Py_INCREF(pyfunc);
    Py_INCREF(closure);
    
    self->addVisitationCallback(type, SoIntersectionVisitationPythonCB, (void *) t);       
  }

  void removeVisitationCallback(SoType type, PyObject * pyfunc, PyObject * closure) {
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, closure);
    Py_INCREF(pyfunc);
    Py_INCREF(closure);
    
    self->removeVisitationCallback(type, SoIntersectionVisitationPythonCB, (void *) t);
  }

  void setFilterCallback(PyObject * pyfunc, PyObject * closure = NULL) {
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, closure);
    Py_INCREF(pyfunc);
    Py_INCREF(closure);
    
    self->setFilterCallback(SoIntersectionFilterPythonCB, (void *) t);
  }

  void addIntersectionCallback(PyObject * pyfunc, PyObject * closure  = NULL) {
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, closure);
    Py_INCREF(pyfunc);
    Py_INCREF(closure);
    
    self->addIntersectionCallback(SoIntersectionPythonCB, (void *) t);
  }

  void removeIntersectionCallback(PyObject * pyfunc, PyObject * closure  = NULL) {
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, closure);
    Py_INCREF(pyfunc);
    Py_INCREF(closure);
    
    self->removeIntersectionCallback(SoIntersectionPythonCB, (void *) t);
  }
}
