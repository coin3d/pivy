%{
static void
convert_SbVec2f_array(PyObject *input, float temp[2])
{
  if (PySequence_Check(input) && (PySequence_Size(input) == 2) &&
      PyNumber_Check(PySequence_GetItem(input, 0)) && 
      PyNumber_Check(PySequence_GetItem(input, 1))) {
    temp[0] = PyFloat_AsDouble(PySequence_GetItem(input, 0));
    temp[1] = PyFloat_AsDouble(PySequence_GetItem(input, 1));
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence with 2 floats");
    PyErr_Print();
  } 
}
%}

%typemap(in) float v[2] (float temp[2]) {
  convert_SbVec2f_array($input, temp);
  $1 = temp;
}

%rename(SbVec2f_vec) SbVec2f::SbVec2f(const float v[2]);
%rename(SbVec2f_ff) SbVec2f::SbVec2f(const float x, const float y);

%feature("shadow") SbVec2f::SbVec2f %{
def __init__(self,*args):
   if len(args) == 1:
      self.this = apply(_pivy.new_SbVec2f_vec,args)
      self.thisown = 1
      return
   elif len(args) == 2:
      self.this = apply(_pivy.new_SbVec2f_ff,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SbVec2f,args)
   self.thisown = 1
%}

%rename(setValue_ff) SbVec2f::setValue(const float x, const float y);

%feature("shadow") SbVec2f::setValue(const float vec[2]) %{
def setValue(*args):
   if len(args) == 3:
      return apply(_pivy.SbVec2f_setValue_ff,args)
   return apply(_pivy.SbVec2f_setValue,args)
%}

%rename(SbVec2f_mul) operator *(const SbVec2f & v, const float d);
%rename(SbVec2f_d_mul) operator *(const float d, const SbVec2f & v);
%rename(SbVec2f_add) operator+(const SbVec2f & v1, const SbVec2f & v2);
%rename(SbVec2f_sub) operator-(const SbVec2f & v1, const SbVec2f & v2);
%rename(SbVec2f_div) operator /(const SbVec2f & v, const float d);
%rename(SbVec2f_eq) operator ==(const SbVec2f & v1, const SbVec2f & v2);
%rename(SbVec2f_neq) operator !=(const SbVec2f & v1, const SbVec2f & v2);

%apply float *OUTPUT { float & x, float & y };

%ignore SbVec2f::getValue(void) const;

// add a method for wrapping c++ operator[] access
%extend SbVec2f {
  float __getitem__(int i) {
    return (self->getValue())[i];
  }
}