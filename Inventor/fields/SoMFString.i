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

/* FIXME: need to merge with the stuff above
%feature("shadow") SoMFString::setValues %{
def setValues(*args):
   if len(args) == 2:
      if isinstance(args[1], SoMFString):
         val = args[1].getValues()
         return _pivy.SoMFString_setValues(args[0],0,len(val),val)
      else:
         return _pivy.SoMFString_setValues(args[0],0,len(args[1]),args[1])
   elif len(args) == 3:
      if isinstance(args[2], SoMFString):
         val = args[2].getValues()
         return _pivy.SoMFString_setValues(args[0],args[1],len(val),val)
      else:
         return _pivy.SoMFString_setValues(args[0],args[1],len(args[2]),args[2])
   return _pivy.SoMFString_setValues(*args)
%}
*/

%ignore SoMFString::getValues(const int start) const;

%typemap(in,numinputs=1) (int & len, int i) {
   $1 = new int;
   *$1 = 0;
   $2 = PyInt_AsLong($input);
}

%typemap(argout) (int & len, int i) {
  Py_XDECREF($result);   /* Blow away any previous result */
  $result = PyList_New(*$1);
  if(result) {
    for(int i = 0; i < *$1; i++){ 
      PyObject * str = PyString_FromString(result[i].getString());
      PyList_SetItem($result, i, str);
    }
  }
  delete $1;
}

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
  const SbString * __getValuesHelper__(int & len, int i) {
    if( i < 0 || i > self->getNum())
      return 0;
    len = self->getNum() - i;
    return self->getValues(i);
  }
/* implement getValues to have default argument etc. */
%pythoncode %{
   def getValues(*args):
     if len(args) == 1:
        return _pivy.SoMFString___getValuesHelper__(args[0], 0)
     return _pivy.SoMFString___getValuesHelper__(*args)
%}
}
