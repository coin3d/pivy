%{
static void
SoSelectionPathPythonCB(void * data, SoPath * path)
{
  PyObject *func, *arglist;
  PyObject *result, *pathCB;

  pathCB = SWIG_NewPointerObj((void *) path, SWIGTYPE_p_SoPath, 1);

  /* the first item in the data sequence is the python callback
   * function; the second is the supplied data python object */
  func = PyTuple_GetItem((PyObject *)data, 0);
  arglist = Py_BuildValue("OO", PyTuple_GetItem((PyObject *)data, 1), pathCB);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }

  Py_DECREF(arglist);
  Py_XDECREF(result);

  return /*void*/;
}

static void
SoSelectionClassPythonCB(void * data, SoSelection * sel)
{
  PyObject *func, *arglist;
  PyObject *result, *selCB;

  selCB = SWIG_NewPointerObj((void *) sel, SWIGTYPE_p_SoSelection, 1);

  /* the first item in the data sequence is the python callback
   * function; the second is the supplied data python object */
  func = PyTuple_GetItem((PyObject *)data, 0);
  arglist = Py_BuildValue("OO", PyTuple_GetItem((PyObject *)data, 1), selCB);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }

  Py_DECREF(arglist);
  Py_XDECREF(result);

  return /*void*/;
}

static SoPath *
SoSelectionPickPythonCB(void * data, const SoPickedPoint * pick)
{
  PyObject *func, *arglist;
  PyObject *result, *pickCB;
  SoPath *resultobj;

  pickCB = SWIG_NewPointerObj((void *) pick, SWIGTYPE_p_SoPickedPoint, 1);

  /* the first item in the data sequence is the python callback
   * function; the second is the supplied data python object */
  func = PyTuple_GetItem((PyObject *)data, 0);
  arglist = Py_BuildValue("OO", PyTuple_GetItem((PyObject *)data, 1), pickCB);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }
  else {
    SWIG_ConvertPtr(result, (void **) &resultobj, SWIGTYPE_p_SoPath, 1);
  }

  Py_DECREF(arglist);
  Py_XDECREF(result);

  return resultobj;
}
%}

%typemap(in) PyObject *pyfunc %{
  if (!PyCallable_Check($input)) {
    PyErr_SetString(PyExc_TypeError, "need a callable object!");
    return NULL;
  }
  $1 = $input;
%}

%rename(SoSelection_i) SoSelection::SoSelection(const int nChildren);

%feature("shadow") SoSelection::SoSelection %{
def __init__(self,*args):
   newobj = None
   if len(args) == 1:
      newobj = apply(_coin.new_SoSelection_i,args)
   else:
      newobj = apply(_coin.new_SoSelection,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}

%rename(select_nod) SoSelection::select(SoNode *node);

%feature("shadow") SoSelection::select(const SoPath * path) %{
def select(*args):
   if isinstance(args[1], SoNode):
      return apply(_coin.SoSelection_select_nod,args)
   return apply(_coin.SoSelection_select,args)
%}

%rename(deselect_i) SoSelection::deselect(const int which);
%rename(deselect_nod) SoSelection::deselect(SoNode *node);

%feature("shadow") SoSelection::deselect(const SoPath * path) %{
def deselect(*args):
   if isinstance(args[1], SoNode):
      return apply(_coin.SoSelection_deselect_nod,args)
   elif type(args[1]) == type(1):
      return apply(_coin.SoSelection_deselect_i,args)
   return apply(_coin.SoSelection_select,args)
%}

%rename(toggle_nod) SoSelection::toggle(SoNode * node);

%feature("shadow") SoSelection::toggle(const SoPath * path) %{
def toggle(*args):
   if isinstance(args[1], SoNode):
      return apply(_coin.SoSelection_toggle_nod,args)
   return apply(_coin.SoSelection_toggle,args)
%}

%rename(isSelected_nod) SoSelection::isSelected(SoNode * node) const;

%feature("shadow") isSelected(const SoPath * path) const %{
def isSelected(*args):
   if isinstance(args[1], SoNode):
      return apply(_coin.SoSelection_isSelected_nod,args)
   return apply(_coin.SoSelection_isSelected,args)
%}

/* add python specific callback functions */
%extend SoSelection {
  void addSelectionCallback(PyObject *pyfunc, PyObject *userdata = NULL) {
    if (userdata == NULL) {
      Py_INCREF(Py_None);
      userdata = Py_None;
    }
      
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userdata);
    Py_INCREF(pyfunc);
    Py_INCREF(userdata);

    self->addSelectionCallback(SoSelectionPathPythonCB, (void *) t);
  }

  void removeSelectionCallback(PyObject *pyfunc, PyObject *userdata = NULL) {
    if (userdata == NULL) {
      Py_INCREF(Py_None);
      userdata = Py_None;
    }
      
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userdata);

    self->removeSelectionCallback(SoSelectionPathPythonCB, (void *) t);
  }

  void addDeselectionCallback(PyObject *pyfunc, PyObject *userdata = NULL) {
    if (userdata == NULL) {
      Py_INCREF(Py_None);
      userdata = Py_None;
    }
      
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userdata);
    Py_INCREF(pyfunc);
    Py_INCREF(userdata);

    self->addDeselectionCallback(SoSelectionPathPythonCB, (void *) t);
  }

  void removeDeselectionCallback(PyObject *pyfunc, PyObject *userdata = NULL) {
    if (userdata == NULL) {
      Py_INCREF(Py_None);
      userdata = Py_None;
    }
      
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userdata);

    self->removeDeselectionCallback(SoSelectionPathPythonCB, (void *) t);
  }

  void addStartCallback(PyObject *pyfunc, PyObject *userdata = NULL) {
    if (userdata == NULL) {
      Py_INCREF(Py_None);
      userdata = Py_None;
    }
      
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userdata);
    Py_INCREF(pyfunc);
    Py_INCREF(userdata);

    self->addStartCallback(SoSelectionClassPythonCB, (void *) t);
  }

  void removeStartCallback(PyObject *pyfunc, PyObject *userdata = NULL) {
    if (userdata == NULL) {
      Py_INCREF(Py_None);
      userdata = Py_None;
    }
      
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userdata);

    self->removeStartCallback(SoSelectionClassPythonCB, (void *) t);
  }

  void addFinishCallback(PyObject *pyfunc, PyObject *userdata = NULL) {
    if (userdata == NULL) {
      Py_INCREF(Py_None);
      userdata = Py_None;
    }
      
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userdata);
    Py_INCREF(pyfunc);
    Py_INCREF(userdata);

    self->addFinishCallback(SoSelectionClassPythonCB, (void *) t);
  }

  void removeFinishCallback(PyObject *pyfunc, PyObject *userdata = NULL) {
    if (userdata == NULL) {
      Py_INCREF(Py_None);
      userdata = Py_None;
    }
      
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userdata);

    self->removeFinishCallback(SoSelectionClassPythonCB, (void *) t);
  }

  void setPickFilterCallback(PyObject *pyfunc, PyObject *userdata = NULL, int callOnlyIfSelectable = 1) {
    if (userdata == NULL) {
      Py_INCREF(Py_None);
      userdata = Py_None;
    }
      
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userdata);
    Py_INCREF(pyfunc);
    Py_INCREF(userdata);

    self->setPickFilterCallback(SoSelectionPickPythonCB, (void *) t, callOnlyIfSelectable);
  }

  void addChangeCallback(PyObject *pyfunc, PyObject *userdata = NULL) {
    if (userdata == NULL) {
      Py_INCREF(Py_None);
      userdata = Py_None;
    }
      
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userdata);
    Py_INCREF(pyfunc);
    Py_INCREF(userdata);

    self->addChangeCallback(SoSelectionClassPythonCB, (void *) t);
  }

  void removeChangeCallback(PyObject *pyfunc, PyObject *userdata = NULL) {
    if (userdata == NULL) {
      Py_INCREF(Py_None);
      userdata = Py_None;
    }
      
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, userdata);
    Py_INCREF(pyfunc);
    Py_INCREF(userdata);

    self->removeChangeCallback(SoSelectionClassPythonCB, (void *) t);
  }
}
