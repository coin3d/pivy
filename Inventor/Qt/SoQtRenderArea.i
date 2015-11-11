%{
static SbBool
SoQtRenderAreaEventPythonCB(void * closure, QEvent * event)
{
  PyObject *func, *arglist;
  PyObject *result, *sip, *qt, *qev = NULL;
  int ret = 0;

  /* try to create a QEvent PyQt instance over sip */

  initialize_pyqt_module_import_name();

  /* check if the sip module is available and import it */
  if (!(sip = PyDict_GetItemString(PyModule_GetDict(PyImport_AddModule("__main__")), "sip"))) {
    sip = PyImport_ImportModule("sip");
  }

  if (sip && PyModule_Check(sip)) {
    /* check if the qt module is available and import it */
    if (!(qt = PyDict_GetItemString(PyModule_GetDict(PyImport_AddModule("__main__")), PYQT_MODULE_IMPORT_NAME))) {
      qt = PyImport_ImportModule(PYQT_MODULE_IMPORT_NAME);
    }

    if (qt && PyModule_Check(qt)) {
      /* grab the wrapinstance(addr, type) function */
      PyObject *sip_wrapinst_func;
      sip_wrapinst_func = PyDict_GetItemString(PyModule_GetDict(sip), "wrapinstance");
      
      if (PyCallable_Check(sip_wrapinst_func)) {
        PyObject *qevent_type;
        qevent_type = PyDict_GetItemString(PyModule_GetDict(qt), "QEvent");

        arglist = Py_BuildValue("(lO)", event, qevent_type);

        if (!(qev = PyEval_CallObject(sip_wrapinst_func, arglist))) {
          PyErr_Print();
        }

        Py_DECREF(arglist);
      }
    }
  }

  /* if no QEvent could be created through sip return a swig QEvent type */
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

  if (sip) {Py_DECREF(sip); }
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
