%{
static void
convert_SoMFUInt32_array(PyObject *input, int len, uint32_t *temp)
{
  int i;

  for (i=0; i<len; i++) {
    PyObject *oi = PySequence_GetItem(input,i);
    if (PyNumber_Check(oi)) {
      temp[i] = (uint32_t) PyInt_AsLong(oi);
    } else {
      PyErr_SetString(PyExc_ValueError,"Sequence elements must be numbers");
      free(temp);       
      return;
    }
  }
  return;
}
%}

%typemap(in) uint32_t * (uint32_t *temp) {
  int len;

  if (PySequence_Check($input)) {
    len = PySequence_Length($input);
    temp = (uint32_t *) malloc(len*sizeof(uint32_t));
    convert_SoMFUInt32_array($input, len, temp);
  
    $1 = temp;
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence.");
  }
}

%ignore SoMFUInt32::getValues(const int start) const;

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

%feature("shadow") SoMFUInt32::setValues %{
def setValues(*args):
   if len(args) == 2:
      if isinstance(args[1], SoMFUInt32):
         val = args[1].getValues()
         return _pivy.SoMFUInt32_setValues(args[0],0,len(val),val)
      else:
         return _pivy.SoMFUInt32_setValues(args[0],0,len(args[1]),args[1])
   elif len(args) == 3:
      if isinstance(args[2], SoMFUInt32):
         val = args[2].getValues()
         return _pivy.SoMFUInt32_setValues(args[0],args[1],len(val),val)
      else:
         return _pivy.SoMFUInt32_setValues(args[0],args[1],len(args[2]),args[2])
   return _pivy.SoMFUInt32_setValues(*args)
%}

%extend SoMFUInt32 {
  const uint32_t __getitem__(int i) {
    return (*self)[i];
  }
  void  __setitem__(int i, uint32_t value) {
    self->set1Value(i, value);
  }
  const uint32_t * __getValuesHelper__(int & len, int i) {
    if( i < 0 || i > self->getNum())
      return 0;
    len = self->getNum() - i;
    return self->getValues(i);
  }
/* implement getValues to have default argument etc. */
%pythoncode %{
   def getValues(*args):
     if len(args) == 1:
        return _pivy.SoMFUInt32___getValuesHelper__(args[0], 0)
     return _pivy.SoMFUInt32___getValuesHelper__(*args)
%}
/* shadow __iter__ to return a new iterator object */
%pythoncode %{
   def __iter__(self):
      iter = MFieldIterator(self)
      return iter
%}
}
