%{
static void
convert_SoMFBool_array(PyObject *input, int len, SbBool *temp)
{
  int i;

  for (i=0; i<len; i++) {
    PyObject *oi = PySequence_GetItem(input,i);
    if (PyNumber_Check(oi)) {
      temp[i] = (SbBool) PyInt_AsLong(oi);
    } else {
      PyErr_SetString(PyExc_ValueError,"Sequence elements must be numbers");
      free(temp);       
      return;
    }
  }
  return;
}
%}

%typemap(in) SbBool * (SbBool *temp) {
  int len;

  if (PySequence_Check($input)) {
    len = PySequence_Length($input);
    temp = (int32_t *) malloc(len*sizeof(int32_t));
    convert_SoMFBool_array($input, len, temp);
  
    $1 = temp;
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence.");
  }
}

%ignore SoMFBool::getValues(const int start) const;

%typemap(in,numinputs=1) (int & len, int i) {
   $1 = new int;
   *$1 = 0;
   $2 = PyInt_AsLong($input);
}

%typemap(argout) (int & len, int i) {
  Py_XDECREF($result);   /* Blow away any previous result */
  $result = PyList_New(*$1);
  if(result) {
    for(int i = 0; i < *$1; i++){ PyList_SetItem($result, i, PyInt_FromLong((long)result[i])); }
  }
  delete $1;
}

%feature("shadow") SoMFBool::setValues %{
def setValues(*args):
   if len(args) == 2:
      if isinstance(args[1], SoMFBool):
         val = args[1].getValues()
         return _pivy.SoMFBool_setValues(args[0],0,len(val),val)
      else:
         return _pivy.SoMFBool_setValues(args[0],0,len(args[1]),args[1])
   elif len(args) == 3:
      if isinstance(args[2], SoMFBool):
         val = args[2].getValues()
         return _pivy.SoMFBool_setValues(args[0],args[1],len(val),val)
      else:
         return _pivy.SoMFBool_setValues(args[0],args[1],len(args[2]),args[2])
   return _pivy.SoMFBool_setValues(*args)
%}

%extend SoMFBool {
  void __call__(int i) {
    self->setValue(i);
  }
  const SbBool __getitem__(int i) {
    return (*self)[i];
  }
  void  __setitem__(int i, SbBool value) {
    self->set1Value(i, value);
  }  
  const SbBool * __getValuesHelper__(int & len, int i) {
    if( i < 0 || i > self->getNum())
      return 0;
    len = self->getNum() - i;
    return self->getValues(i);
  }
/* implement getValues to have default argument etc. */
%pythoncode %{
   def getValues(*args):
     if len(args) == 1:
        return _pivy.SoMFBool___getValuesHelper__(args[0], 0)
     return _pivy.SoMFBool___getValuesHelper__(*args)
%}
/* shadow __iter__ to return a new iterator object */
%pythoncode %{
   def __iter__(self):
      iter = MFieldIterator(self)
      return iter
%}
}
