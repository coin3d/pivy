%{
static void
convert_SoMFFloat_array(PyObject *input, int len, float *temp)
{
  int i;

  for (i=0; i<len; i++) {
    PyObject *oi = PySequence_GetItem(input,i);
    if (PyNumber_Check(oi)) {
      temp[i] = (float) PyFloat_AsDouble(oi);
    } else {
      PyErr_SetString(PyExc_ValueError,"Sequence elements must be floats");
      free(temp);       
      return;
    }
  }
  return;
}
%}

%typemap(in) float * (float *temp) {
  int len;

  if (PySequence_Check($input)) {
    len = PySequence_Length($input);
    temp = (float *) malloc(len*sizeof(float));
    convert_SoMFFloat_array($input, len, temp);
  
    $1 = temp;
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence.");
  }
}

%extend SoMFFloat {
  void __call__(float i) {
    self->setValue(i);
  }
  const float __getitem__(int i) {
    return (*self)[i];
  }
  void  __setitem__(int i, float value) {
    self->set1Value(i, value);
  }  
}
