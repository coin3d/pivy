%{
static SoCallbackAction::Response
SoCallbackActionPythonCB(void * userdata,
                         SoCallbackAction * action,
                         const SoNode * node) {
  PyObject *func, *arglist;
  PyObject *result, *acCB, *pynode;
  int iresult = 0;

  acCB = SWIG_NewPointerObj((void *) action, SWIGTYPE_p_SoCallbackAction, 1);
  pynode = SWIG_NewPointerObj((void *) node, SWIGTYPE_p_SoNode, 1);

  /* the first item in the userdata sequence is the python callback
   * function; the second is the supplied userdata python object */
  func = PyTuple_GetItem((PyObject *)userdata, 0);
  arglist = Py_BuildValue("OOO", PyTuple_GetItem((PyObject *)userdata, 1), acCB, pynode);

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

static void
SoTrianglePythonCB(void * userdata, SoCallbackAction * action,
                   const SoPrimitiveVertex * v1,
                   const SoPrimitiveVertex * v2,
                   const SoPrimitiveVertex * v3)
{
  PyObject *func, *arglist;
  PyObject *result, *acCB;
  PyObject *vertex1, *vertex2, *vertex3;

  acCB = SWIG_NewPointerObj((void *) action, SWIGTYPE_p_SoCallbackAction, 1);
  vertex1 = SWIG_NewPointerObj((void *) v1, SWIGTYPE_p_SoPrimitiveVertex, 1);
  vertex2 = SWIG_NewPointerObj((void *) v2, SWIGTYPE_p_SoPrimitiveVertex, 1);
  vertex3 = SWIG_NewPointerObj((void *) v3, SWIGTYPE_p_SoPrimitiveVertex, 1);

  /* the first item in the userdata sequence is the python callback
   * function; the second is the supplied userdata python object */
  func = PyTuple_GetItem((PyObject *)userdata, 0);
  arglist = Py_BuildValue("OOOOO", PyTuple_GetItem((PyObject *)userdata, 1), acCB, vertex1, vertex2, vertex3);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }
  Py_DECREF(arglist);
  Py_XDECREF(result);

  return /*void*/;
}

static void
SoLineSegmentPythonCB(void * userdata, SoCallbackAction * action,
				const SoPrimitiveVertex * v1,
				const SoPrimitiveVertex * v2)
{
  PyObject *func, *arglist;
  PyObject *result, *acCB;
  PyObject *vertex1, *vertex2;

  acCB = SWIG_NewPointerObj((void *) action, SWIGTYPE_p_SoCallbackAction, 1);
  vertex1 = SWIG_NewPointerObj((void *) v1, SWIGTYPE_p_SoPrimitiveVertex, 1);
  vertex2 = SWIG_NewPointerObj((void *) v2, SWIGTYPE_p_SoPrimitiveVertex, 1);

  /* the first item in the userdata sequence is the python callback
   * function; the second is the supplied userdata python object */
  func = PyTuple_GetItem((PyObject *)userdata, 0);
  arglist = Py_BuildValue("OOOO", PyTuple_GetItem((PyObject *)userdata, 1), acCB, vertex1, vertex2);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }
  Py_DECREF(arglist);
  Py_XDECREF(result);

  return /*void*/;
}

static void
SoPointPythonCB(void * userdata, SoCallbackAction * action, const SoPrimitiveVertex * v)
{
  PyObject *func, *arglist;
  PyObject *result, *acCB;
  PyObject *vertex;

  acCB = SWIG_NewPointerObj((void *) action, SWIGTYPE_p_SoCallbackAction, 1);
  vertex = SWIG_NewPointerObj((void *) v, SWIGTYPE_p_SoPrimitiveVertex, 1);

  /* the first item in the userdata sequence is the python callback
   * function; the second is the supplied userdata python object */
  func = PyTuple_GetItem((PyObject *)userdata, 0);
  arglist = Py_BuildValue("OOO", PyTuple_GetItem((PyObject *)userdata, 1), acCB, vertex);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }
  Py_DECREF(arglist);
  Py_XDECREF(result);

  return /*void*/;
}
%}

%typemap(in) PyObject *pyfunc %{
  if (!PyCallable_Check($input)) {
    PyErr_SetString(PyExc_TypeError, "need a callable object!");
    return NULL;
  }
  $1 = $input;
%}

%rename(SoCallbackAction_vpr) SoCallbackAction::SoCallbackAction(const SbViewportRegion & vp);

%feature("shadow") SoCallbackAction::SoCallbackAction %{
def __init__(self,*args):
   if len(args) == 1:
      self.this = apply(_pivy.new_SoCallbackAction_vpr,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SoCallbackAction,args)
   self.thisown = 1
%}

  /* add python specific callback functions */
%extend SoCallbackAction {
  void addPreCallback(const SoType type, PyObject *pyfunc, PyObject *userdata) {
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userdata);
    Py_INCREF(pyfunc);
    Py_INCREF(userdata);

    self->addPreCallback(type, SoCallbackActionPythonCB, (void *) t);
  }

  void addPostCallback(const SoType type, PyObject *pyfunc, PyObject *userdata) {
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userdata);
    Py_INCREF(pyfunc);
    Py_INCREF(userdata);

    self->addPostCallback(type, SoCallbackActionPythonCB, (void *) t);
  }

  void addPreTailCallback(PyObject *pyfunc, PyObject *userdata) {
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userdata);
    Py_INCREF(pyfunc);
    Py_INCREF(userdata);

    self->addPreTailCallback(SoCallbackActionPythonCB, (void *) t);
  }

  void addPostTailCallback(PyObject *pyfunc, PyObject *userdata) {
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userdata);
    Py_INCREF(pyfunc);
    Py_INCREF(userdata);

    self->addPostTailCallback(SoCallbackActionPythonCB, (void *) t);
  }

  void addTriangleCallback(const SoType type, PyObject *pyfunc, PyObject *userdata) {
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userdata);
    Py_INCREF(pyfunc);
    Py_INCREF(userdata);

    self->addTriangleCallback(type, SoTrianglePythonCB, (void *) t);
  }

  void addLineSegmentCallback(const SoType type, PyObject *pyfunc, PyObject *userdata) {
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userdata);
    Py_INCREF(pyfunc);
    Py_INCREF(userdata);

    self->addLineSegmentCallback(type, SoLineSegmentPythonCB, (void *) t);
  }

  void addPointCallback(const SoType type, PyObject *pyfunc, PyObject *userdata) {
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userdata);
    Py_INCREF(pyfunc);
    Py_INCREF(userdata);

    self->addPointCallback(type, SoPointPythonCB, (void *) t);
  }
}
