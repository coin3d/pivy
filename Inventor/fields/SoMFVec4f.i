%{
static void
convert_SoMFVec4f_array(PyObject *input, int len, float temp[][4])
{
  int i,j;

  for (i=0; i<len; i++) {
    PyObject *oi = PySequence_GetItem(input,i);

    for (j=0; j<4; j++) {
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

%typemap(in) float xyzw[][4] (float (*temp)[4]) {
  int len;

  if (PySequence_Check($input)) {
    len = PySequence_Length($input);

    temp = (float (*)[4]) malloc(len*4*sizeof(float));
    convert_SoMFVec4f_array($input, len, temp);
  
    $1 = temp;
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence.");
  }
}

%typemap(in) float xyzw[4] (float temp[4]) {
  convert_SbVec4f_array($input, temp);
  $1 = temp;
}

%rename(setValue_vec) SoMFVec4f::setValue(SbVec4f const &);
%rename(setValue_ffff) SoMFVec4f::setValue(const float x, const float y, const float z, const float w);

%feature("shadow") SoMFVec4f::setValue(const float xyzw[4]) %{
def setValue(*args):
   if isinstance(args[1], SbVec4f):
      return apply(_pivy.SoMFVec4f_setValue_vec,args)
   elif len(args) == 5:
      return apply(_pivy.SoMFVec4f_setValue_ffff,args)
   return apply(_pivy.SoMFVec4f_setValue,args)
%}

%rename(set1Value_i_vec) SoMFVec4f::set1Value(int const ,SbVec4f const &);
%rename(set1Value_i_ffff) SoMFVec4f::set1Value(const int idx, const float x, const float y, const float z, const float w);

%feature("shadow") SoMFVec4f::set1Value(const int idx, const float xyzw[4]) %{
def set1Value(*args):
   if isinstance(args[2], SbVec4f):
      return apply(_pivy.SoMFVec4f_set1Value_i_vec,args)
   elif len(args) == 6:
      return apply(_pivy.SoMFVec4f_set1Value_i_fff,args)
   return apply(_pivy.SoMFVec4f_set1Value,args)
%}

%rename(setValues_i_i_vec) SoMFVec4f::setValues(int const ,int const ,SbVec4f const *);

%feature("shadow") SoMFVec4f::setValues(const int start, const int num, const float xyzw[][4]) %{
def setValues(*args):
   if isinstance(args[3], SbVec4f):
      return apply(_pivy.SoMFVec4f_setValues_i_i_vec,args)
   return apply(_pivy.SoMFVec4f_setValues,args)
%}

%extend SoMFVec4f {
  void __call__(const SbVec4f & vec) {
    self->setValue(vec);
  }
  void __call__(const float x, const float y, const float z, const float w) {
    self->setValue(x,y,z,w);
  }
  void __call__(float xyzw[4]) {
    self->setValue(xyzw);
  }
  const SbVec4f & __getitem__(int i) {
    return (*self)[i];
  }
  void  __setitem__(int i, const SbVec4f & value) {
    self->set1Value(i, value);
  }  
}
