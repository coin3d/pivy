%{
static void
SoGLRenderPassPythonCB(void * userdata)
{
  PyObject *func, *arglist;
  PyObject *result;

  /* the first item in the userdata sequence is the python callback
   * function; the second is the supplied userdata python object */
  func = PyTuple_GetItem((PyObject *)userdata, 0);
  arglist = Py_BuildValue("O", PyTuple_GetItem((PyObject *)userdata, 1));

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }

  Py_DECREF(arglist);
  Py_XDECREF(result);

  return /*void*/;
}

static SoGLRenderAction::AbortCode
SoGLRenderAbortPythonCB(void * userdata)
{
  PyObject *func, *arglist;
  PyObject *result;
  SoGLRenderAction::AbortCode res;

  /* the first item in the userdata sequence is the python callback
   * function; the second is the supplied userdata python object */
  func = PyTuple_GetItem((PyObject *)userdata, 0);
  arglist = Py_BuildValue("O", PyTuple_GetItem((PyObject *)userdata, 1));

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }

  res = (SoGLRenderAction::AbortCode)PyInt_AsLong(result);

  Py_DECREF(arglist);
  Py_XDECREF(result);

  return res;
}

static void
SoGLPreRenderPythonCB(void * userdata, class SoGLRenderAction * action)
{
  PyObject *func, *arglist;
  PyObject *result, *acCB;

  acCB = SWIG_NewPointerObj((void *) action, SWIGTYPE_p_SoGLRenderAction, 1);

  /* the first item in the userdata sequence is the python callback
   * function; the second is the supplied userdata python object */
  func = PyTuple_GetItem((PyObject *)userdata, 0);
  arglist = Py_BuildValue("OO", PyTuple_GetItem((PyObject *)userdata, 1), acCB);

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

/* add python specific callback functions */
%extend SoGLRenderAction {
  void setPassCallback(PyObject *pyfunc, PyObject * userdata){
    if (userdata == NULL) {
      Py_INCREF(Py_None);
      userdata = Py_None;
    }
    
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userdata);
    Py_INCREF(pyfunc);
    Py_INCREF(userdata);
    
    self->setPassCallback(SoGLRenderPassPythonCB, (void *) t);
  }

  void setAbortCallback(PyObject *pyfunc, PyObject * userdata){
    if (userdata == NULL) {
      Py_INCREF(Py_None);
      userdata = Py_None;
    }
	  
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userdata);
    Py_INCREF(pyfunc);
    Py_INCREF(userdata);

    self->setAbortCallback(SoGLRenderAbortPythonCB, (void *) t);    
  }
  
  void addPreRenderCallback(PyObject *pyfunc, PyObject * userdata) {
    if (userdata == NULL) {
      Py_INCREF(Py_None);
      userdata = Py_None;
    }
	  
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userdata);
    Py_INCREF(pyfunc);
    Py_INCREF(userdata);

    self->addPreRenderCallback(SoGLPreRenderPythonCB, (void *) t);
  }

  void removePreRenderCallback(PyObject *pyfunc, PyObject * userdata) {
    if (userdata == NULL) {
      Py_INCREF(Py_None);
      userdata = Py_None;
    }
	  
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userdata);
    Py_INCREF(pyfunc);
    Py_INCREF(userdata);

    self->removePreRenderCallback(SoGLPreRenderPythonCB, (void *) t);
  }

}
