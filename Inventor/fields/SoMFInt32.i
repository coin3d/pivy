%{
static void
convert_SoMFInt32_array(PyObject *input, int len, int32_t *temp)
{
  int i;

  for (i=0; i<len; i++) {
    PyObject *oi = PySequence_GetItem(input,i);
    if (PyNumber_Check(oi)) {
      temp[i] = (int32_t) PyInt_AsLong(oi);
    } else {
      PyErr_SetString(PyExc_ValueError,"Sequence elements must be numbers");
      free(temp);       
      return;
    }
  }
  return;
}
%}

%typemap(in) int32_t * (int32_t *temp) {
  int len;

  if (PySequence_Check($input)) {
    len = PySequence_Length($input);
    temp = (int32_t *) malloc(len*sizeof(int32_t));
    convert_SoMFInt32_array($input, len, temp);
  
    $1 = temp;
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence.");
  }
}

%extend SoMFInt32 {
  void __call__(int i) {
    self->setValue(i);
  }
  const int32_t __getitem__(int i) {
    return (*self)[i];
  }
  void  __setitem__(int i, int32_t value) {
    self->set1Value(i, value);
  }  
}
