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

%typemap(typecheck) float v[2] {
  $1 = PySequence_Check($input) ? 1 : 0;
}

%rename(SbVec2f_vec) SbVec2f::SbVec2f(const float v[2]);
%rename(SbVec2f_ff) SbVec2f::SbVec2f(const float x, const float y);

%feature("shadow") SbVec2f::SbVec2f %{
def __init__(self,*args):
   newobj = None
   if len(args) == 1:
      if isinstance(args[0], SbVec2f):
         newobj = _coin.new_SbVec2f()
         newobj.setValue(args[0])
      else:
         newobj = apply(_coin.new_SbVec2f_vec,args)
   elif len(args) == 2:
      newobj = apply(_coin.new_SbVec2f_ff,args)
   else:
      newobj = apply(_coin.new_SbVec2f,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}

/* add operator overloading methods instead of the global functions */
%extend SbVec2f {
  SbVec2f __add__(const SbVec2f &u) { return *self + u; }
  SbVec2f __sub__(const SbVec2f &u) { return *self - u; }
  SbVec2f __mul__(const float d) { return *self * d; }
  SbVec2f __rmul__(const float d) { return *self * d; }
  SbVec2f __div__(const float d) { return *self / d; }
  int __eq__(const SbVec2f &u ) { return *self == u; }
  int __nq__(const SbVec2f &u) { return *self != u; }
  // add a method for wrapping c++ operator[] access
  float __getitem__(int i) { return (self->getValue())[i]; }
  void  __setitem__(int i, float value) { (*self)[i] = value; }
}

%apply float *OUTPUT { float & x, float & y };

%ignore SbVec2f::getValue() const;
