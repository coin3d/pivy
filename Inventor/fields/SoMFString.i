%typemap(in) const char * strings[] {
  int i;

  /* check if the sequence really matches the expected length */
  if (PySequence_Size(obj3) < arg3) {
    PyErr_SetString(PyExc_ValueError, "provided sequence is smaller than num");
    return NULL;
  }

  $1 = (char **)malloc(arg3*sizeof(char *));
  for (i=0; i < arg3; i++) {
    PyObject *item = PySequence_GetItem(obj3,i);
    if (!PyString_Check(item)) {
        free($1);
        PyErr_SetString(PyExc_ValueError, "list items must be strings");
        return NULL;
    }
    $1[i] = PyString_AsString(item);
  }
}

%rename(setValues_i_i_str) SoMFString::setValues(int const ,int const ,SbString const *);

%feature("shadow") SoMFString::setValues(const int start, const int num, const char * strings[]) %{
def setValues(*args):
   if isinstance(args[3], SbString):
      return apply(_pivy.SoMFString_setValues_i_i_str,args)
   return apply(_pivy.SoMFString_setValues,args)
%}

%extend SoMFString {
  void __call__(const SbString & sbstr) {
    self->setValue(sbstr);
  }
  void __call__(char * str) {
    self->setValue(str);
  }
  const SbString & __getitem__(int i) {
    return (*self)[i];
  }
  void  __setitem__(int i, const SbString & value) {
    self->set1Value(i, value);
  }
}
