%{
static void
SoSceneManagerPythonCB(void * userdata, SoSceneManager * mgr)
{
  PyObject *func, *arglist;
  PyObject *result, *mgrCB;

  mgrCB = SWIG_NewPointerObj((void *)mgr, SWIGTYPE_p_SoSceneManager, 1);

  /* the first item in the userdata sequence is the python callback
   * function; the second is the supplied userdata python object */
  func = PyTuple_GetItem((PyObject *)userdata, 0);
  arglist = Py_BuildValue("OO", PyTuple_GetItem((PyObject *)userdata, 1), mgrCB);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }  
  Py_DECREF(arglist);
  Py_XDECREF(result);

  return /*void*/;
}
%}

/* add python specific callback functions */
%extend SoSceneManager {
  void setRenderCallback(PyObject * pyfunc, PyObject * userData = NULL) {
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userData);
    Py_INCREF(pyfunc);
    Py_INCREF(userData);
    
    self->setRenderCallback(SoSceneManagerPythonCB, (void *)t);
  }
}
