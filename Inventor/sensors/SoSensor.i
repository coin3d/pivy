%{
static void
SoSensorPythonCB(void * data, SoSensor * sensor)
{
  PyObject *func, *arglist;
  PyObject *result, *sensCB;

  sensCB = SWIG_NewPointerObj((void *) sensor, SWIGTYPE_p_SoSensor, 1);

  /* the first item in the data sequence is the python callback
   * function; the second is the supplied data python object */
  func = PyTuple_GetItem((PyObject *)data, 0);
  arglist = Py_BuildValue("OO", PyTuple_GetItem((PyObject *)data, 1), sensCB);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }

  Py_DECREF(arglist);
  Py_XDECREF(result);
}
%}

%typemap(in) SoSensorCB * func {
  if (!PyCallable_Check($input)) {
    PyErr_SetString(PyExc_TypeError, "need a callable object!");
    return NULL;
  }
  $1 = SoSensorPythonCB;
}

%typemap(typecheck) SoSensorCB * func {
  $1 = PyCallable_Check($input) ? 1 : 0;
}

%typemap(in) void * data {
  if (!PyTuple_Check($input)) {
    PyErr_SetString(PyExc_TypeError, "tuple expected!");
    return NULL;
  }

  Py_INCREF($input);
  $1 = (void *)$input;
}

%typemap(typecheck) void * data {
  $1 = PyTuple_Check($input) ? 1 : 0;
}
