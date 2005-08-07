%{
static void
SoDraggerPythonCB(void * data, SoDragger * dragger)
{
  PyObject *func, *arglist;
  PyObject *result, *dragCB;

  dragCB = SWIG_NewPointerObj((void *) dragger, SWIGTYPE_p_SoDragger, 1);

  /* the first item in the data sequence is the python callback
   * function; the second is the supplied data python object */
  func = PyTuple_GetItem((PyObject *)data, 0);
  arglist = Py_BuildValue("OO", PyTuple_GetItem((PyObject *)data, 1), dragCB);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }
  Py_DECREF(arglist);
  Py_XDECREF(result);

  return /*void*/;
}
%}

%typemap(in) PyObject *pyfunc {
  if (!PyCallable_Check($input)) {
    PyErr_SetString(PyExc_TypeError, "need a callable object!");
    return NULL;
  }
  $1 = $input;
}

%typemap(typecheck) PyObject *pyfunc {
  $1 = PyCallable_Check($input) ? 1 : 0;
}

/* add python specific callback functions */
%extend SoDragger {
  void addStartCallback(PyObject *pyfunc, PyObject *data = NULL) {
    if (data == NULL) {
      Py_INCREF(Py_None);
      data = Py_None;
    }

    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, data);
    Py_INCREF(pyfunc);
    Py_INCREF(data);

    self->addStartCallback(SoDraggerPythonCB, (void *) t);
  }

  void removeStartCallback(PyObject *pyfunc, PyObject *data = NULL) {
    if (data == NULL) {
      Py_INCREF(Py_None);
      data = Py_None;
    }

    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, data);

    self->removeStartCallback(SoDraggerPythonCB, (void *) t);
  }

  void addMotionCallback(PyObject *pyfunc, PyObject *data = NULL) {
    if (data == NULL) {
      Py_INCREF(Py_None);
      data = Py_None;
    }

    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, data);
    Py_INCREF(pyfunc);
    Py_INCREF(data);

    self->addMotionCallback(SoDraggerPythonCB, (void *) t);
  }

  void removeMotionCallback(PyObject *pyfunc, PyObject *data = NULL) {
    if (data == NULL) {
      Py_INCREF(Py_None);
      data = Py_None;
    }

    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, data);

    self->removeMotionCallback(SoDraggerPythonCB, (void *) t);
  }

  void addFinishCallback(PyObject *pyfunc, PyObject *data = NULL) {
    if (data == NULL) {
      Py_INCREF(Py_None);
      data = Py_None;
    }

    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, data);
    Py_INCREF(pyfunc);
    Py_INCREF(data);

    self->addFinishCallback(SoDraggerPythonCB, (void *) t);
  }

  void removeFinishCallback(PyObject *pyfunc, PyObject *data = NULL) {
    if (data == NULL) {
      Py_INCREF(Py_None);
      data = Py_None;
    }

    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, data);

    self->removeFinishCallback(SoDraggerPythonCB, (void *) t);
  }

  void addValueChangedCallback(PyObject *pyfunc, PyObject *data = NULL) {
    if (data == NULL) {
      Py_INCREF(Py_None);
      data = Py_None;
    }

    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, data);
    Py_INCREF(pyfunc);
    Py_INCREF(data);

    self->addValueChangedCallback(SoDraggerPythonCB, (void *) t);
  }

  void removeValueChangedCallback(PyObject *pyfunc, PyObject *data = NULL) {
    if (data == NULL) {
      Py_INCREF(Py_None);
      data = Py_None;
    }

    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, data);

    self->removeValueChangedCallback(SoDraggerPythonCB, (void *) t);
  }

  void addOtherEventCallback(PyObject *pyfunc, PyObject *data = NULL) {
    if (data == NULL) {
      Py_INCREF(Py_None);
      data = Py_None;
    }

    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, data);
    Py_INCREF(pyfunc);
    Py_INCREF(data);

    self->addOtherEventCallback(SoDraggerPythonCB, (void *) t);
  }

  void removeOtherEventCallback(PyObject *pyfunc, PyObject *data = NULL) {
    if (data == NULL) {
      Py_INCREF(Py_None);
      data = Py_None;
    }

    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, data);

    self->removeOtherEventCallback(SoDraggerPythonCB, (void *) t);
  }
}
