%{
static void
convert_SoMFVec2f_array(PyObject *input, int len, float temp[][2])
{
  int i,j;

  for (i=0; i<len; i++) {
    PyObject *oi = PySequence_GetItem(input,i);

    for (j=0; j<2; j++) {
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

%typemap(in) float xy[][2] (float (*temp)[2]) {
  int len;

  if (PySequence_Check($input)) {
    len = PySequence_Length($input);

    temp = (float (*)[2]) malloc(len*2*sizeof(float));
    convert_SoMFVec2f_array($input, len, temp);
  
    $1 = temp;
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence.");
  }
}

%typemap(in) float xy[2] (float temp[2]) {
  convert_SbVec2f_array($input, temp);
  $1 = temp;
}

%rename(setValue_vec) SoMFVec2f::setValue(SbVec2f const &);
%rename(setValue_ff) SoMFVec2f::setValue(const float x, const float y);

%feature("shadow") SoMFVec2f::setValue(const float xy[2]) %{
def setValue(*args):
   if isinstance(args[1], SbVec2f):
      return apply(_pivy.SoMFVec2f_setValue_vec,args)
   elif len(args) == 3:
      return apply(_pivy.SoMFVec2f_setValue_ff,args)
   return apply(_pivy.SoMFVec2f_setValue,args)
%}

%rename(set1Value_i_vec) SoMFVec2f::set1Value(int const ,SbVec2f const &);
%rename(set1Value_i_ff) SoMFVec2f::set1Value(const int idx, const float x, const float y);

%feature("shadow") SoMFVec2f::set1Value(const int idx, const float xy[2]) %{
def set1Value(*args):
   if isinstance(args[2], SbVec2f):
      return apply(_pivy.SoMFVec2f_set1Value_i_vec,args)
   elif len(args) == 4:
      return apply(_pivy.SoMFVec2f_set1Value_i_ff,args)
   return apply(_pivy.SoMFVec2f_set1Value,args)
%}

%rename(setValues_i_i_vec) SoMFVec2f::setValues(int const ,int const ,SbVec2f const *);

%feature("shadow") SoMFVec2f::setValues(const int start, const int num, const float xyz[][2]) %{
def setValues(*args):
   if isinstance(args[3], SbVec2f):
      return apply(_pivy.SoMFVec2f_setValues_i_i_vec,args)
   return apply(_pivy.SoMFVec2f_setValues,args)
%}

%extend SoMFVec2f {
  void __call__(const SbVec2f & vec) {
    self->setValue(vec);
  }
  void __call__(const float x, const float y) {
    self->setValue(x,y);
  }
  void __call__(float xy[2]) {
    self->setValue(xy);
  }
  const SbVec2f & __getitem__(int i) {
    return (*self)[i];
  }
  void  __setitem__(int i, const SbVec2f & value) {
    self->set1Value(i, value);
  }  
}
