%typemap(in) const char * strings[] {
  int len;  
  if (PySequence_Check($input)) {
    len = PySequence_Length($input);
    if (len > 0) {
      $1 = (char **)malloc(len * sizeof(char *));
      for (int i = 0; i < len; i++) {
        PyObject * item = PyObject_Str(PySequence_GetItem($input,i));
        $1[i] = PyString_AsString(item);
        Py_DECREF(item);
      }
    } else { $1 = NULL; }
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence.");
    return NULL;
  }
}

/* free the list */
%typemap(freearg) const char * strings[] {
  if ($1) { free($1); }
}

%typemap(typecheck,precedence=SWIG_TYPECHECK_POINTER) const char * strings[] {
  $1 = PySequence_Check($input) ? 1 : 0;
}

%feature("shadow") SoMFName::setValues %{
def setValues(*args):
   if len(args) == 2:
     return _coin.SoMFName_setValues(args[0], 0, len(args[1]), args[1])
   elif len(args) == 3:
     return _coin.SoMFName_setValues(args[0], args[1], len(args[2]), args[2])
   return apply(_coin.SoMFName_setValues,args)
%}

%ignore SoMFName::getValues(const int start) const;

%typemap(in,numinputs=0) int & len (int temp) {
  $1 = &temp;
  *$1 = 0;
}

%typemap(argout) int & len {
  Py_XDECREF($result); /* free up any previous result */
  $result = PyList_New(*$1);
  if (result) {
    for (int i = 0; i < *$1; i++) {
      PyObject * str = PyString_FromString(result[i].getString());
      PyList_SetItem($result, i, str);
    }
  }
}

%rename(getValues) SoMFName::__getValuesHelper__;

%extend SoMFName {
  const SbName & __getitem__(int i) { return (*self)[i]; }
  void  __setitem__(int i, const SbName & value) { self->set1Value(i, value); }
  void setValue(const SoMFName * other ){ *self = *other; }
  const SbName * __getValuesHelper__(int & len, int i = 0) {
    if (i < 0 || i >= self->getNum()) { return NULL; }
    len = self->getNum() - i;
    return self->getValues(i);
  }
}
