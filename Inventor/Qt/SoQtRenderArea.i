%{
static SbBool
SoQtRenderAreaEventPythonCB(void * closure, QEvent * event)
{
  PyObject *func, *arglist;
  PyObject *result, *shiboken, *qt, *qev = NULL;
  int ret = 0;

  /* try to create a QEvent PySide instance over shiboken */


  /* check if the shiboken module is available and import it */
  shiboken = getShiboken();

  if (shiboken && PyModule_Check(shiboken)) {
    /* check if the qt module is available and import it */
    if (!(qt = PyDict_GetItemString(PyModule_GetDict(PyImport_AddModule("__main__")), PYSIDE_QTCORE))) {
      qt = PyImport_ImportModule(PYSIDE_QTCORE);
    }

    if (qt && PyModule_Check(qt)) {
      /* grab the wrapinstance(addr, type) function */
      PyObject *shiboken_wrapinst_func;
      shiboken_wrapinst_func = PyDict_GetItemString(PyModule_GetDict(shiboken), "wrapInstance");
      
      if (PyCallable_Check(shiboken_wrapinst_func)) {
        PyObject *qevent_type;
        qevent_type = PyDict_GetItemString(PyModule_GetDict(qt), "QEvent");

        arglist = Py_BuildValue("(lO)", event, qevent_type);

        if (!(qev = PyEval_CallObject(shiboken_wrapinst_func, arglist))) {
          PyErr_Print();
        }

        Py_DECREF(arglist);
      }
    }
  }

  /* if no QEvent could be created through shiboken return a swig QEvent type */
  if (!qev) {
    qev = SWIG_NewPointerObj((void *)event, SWIGTYPE_p_QEvent, 0);
  }

  /* the first item in the closure sequence is the python callback
   * function; the second is the supplied closure python object */
  func = PyTuple_GetItem((PyObject *)closure, 0);
  arglist = Py_BuildValue("(OO)", PyTuple_GetItem((PyObject *)closure, 1), qev);

  if (!(result = PyEval_CallObject(func, arglist))) {
    PyErr_Print();
  } else {
    ret = PyInt_AsLong(result);
  }

  if (shiboken) {Py_DECREF(shiboken); }
  Py_DECREF(arglist);
  Py_DECREF(qev);
  Py_XDECREF(result);

  return ret;
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
%extend SoQtRenderArea {
  void setEventCallback(PyObject *pyfunc, PyObject *user = NULL) {
    self->setEventCallback(SoQtRenderAreaEventPythonCB,
                           (void *)Py_BuildValue("(OO)",
                                                 pyfunc,
                                                 user ? user : Py_None));
  }
}
