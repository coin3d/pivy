%{
static void
convert_SoMFVec3f_array(PyObject *input, int len, float temp[][3])
{
  int i,j;

  for (i=0; i<len; i++) {
    PyObject *oi = PySequence_GetItem(input,i);

    for (j=0; j<3; j++) {
      PyObject *oj = PySequence_GetItem(oi,j);

      if (PyNumber_Check(oj)) {
        temp[i][j] = (float) PyFloat_AsDouble(oj);
      } else {
        PyErr_SetString(PyExc_ValueError,"Sequence elements must be numbers");
        free(temp);       
        return;
      }
    }
  }
  return;
}
%}

%typemap(in) float xyz[][3] (float (*temp)[3]) {
  int len;

  if (PySequence_Check($input)) {
    len = PySequence_Length($input);

    temp = (float (*)[3]) malloc(len*3*sizeof(float));
    convert_SoMFVec3f_array($input, len, temp);
  
    $1 = temp;
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence.");
  }
}

%typemap(in) float xyz[3] (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%rename(setValue_vec) SoMFVec3f::setValue(SbVec3f const &);
%rename(setValue_fff) SoMFVec3f::setValue(const float x, const float y, const float z);

%feature("shadow") SoMFVec3f::setValue(const float xyz[3]) %{
def setValue(*args):
   if isinstance(args[1], SbVec3f):
      return apply(_pivy.SoMFVec3f_setValue_vec,args)
   elif len(args) == 4:
      return apply(_pivy.SoMFVec3f_setValue_fff,args)
   return apply(_pivy.SoMFVec3f_setValue,args)
%}

%rename(set1Value_i_vec) SoMFVec3f::set1Value(int const ,SbVec3f const &);
%rename(set1Value_i_fff) SoMFVec3f::set1Value(const int idx, const float x, const float y, const float z);

%feature("shadow") SoMFVec3f::set1Value(const int idx, const float xyz[3]) %{
def set1Value(*args):
   if isinstance(args[2], SbVec3f):
      return apply(_pivy.SoMFVec3f_set1Value_i_vec,args)
   elif len(args) == 5:
      return apply(_pivy.SoMFVec3f_set1Value_i_fff,args)
   return apply(_pivy.SoMFVec3f_set1Value,args)
%}

%rename(setValues_i_i_vec) SoMFVec3f::setValues(int const ,int const ,SbVec3f const *);

%feature("shadow") SoMFVec3f::setValues(const int start, const int num, const float xyz[][3]) %{
def setValues(*args):
   if isinstance(args[3], SbVec3f):
      return apply(_pivy.SoMFVec3f_setValues_i_i_vec,args)
   return apply(_pivy.SoMFVec3f_setValues,args)
%}

%extend SoMFVec3f {
  void __call__(const SbVec3f & vec) {
    self->setValue(vec);
  }
  void __call__(const float x, const float y, const float z) {
    self->setValue(x,y,z);
  }
  void __call__(float xyz[3]) {
    self->setValue(xyz);
  }
  const SbVec3f & __getitem__(int i) {
    return (*self)[i];
  }
  void  __setitem__(int i, const SbVec3f & value) {
    self->set1Value(i, value);
  }  
}
