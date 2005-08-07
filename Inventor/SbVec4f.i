%{
static void
convert_SbVec4f_array(PyObject *input, float temp[4])
{
  if (PySequence_Check(input) && (PySequence_Size(input) == 4) &&
      PyNumber_Check(PySequence_GetItem(input, 0)) && 
      PyNumber_Check(PySequence_GetItem(input, 1)) && 
      PyNumber_Check(PySequence_GetItem(input, 2)) && 
      PyNumber_Check(PySequence_GetItem(input, 3))) {
    temp[0] = PyFloat_AsDouble(PySequence_GetItem(input, 0));
    temp[1] = PyFloat_AsDouble(PySequence_GetItem(input, 1));
    temp[2] = PyFloat_AsDouble(PySequence_GetItem(input, 2));
    temp[3] = PyFloat_AsDouble(PySequence_GetItem(input, 3));
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence with 4 floats");
    PyErr_Print();
  } 
}
%}

%typemap(in) float v[4] (float temp[4]) {
  convert_SbVec4f_array($input, temp);
  $1 = temp;
}

%typemap(typecheck) float v[4] {
  $1 = PySequence_Check($input) ? 1 : 0;
}

/* for some strange reason the %apply directive below doesn't work 
 * for this class on getValue(f,f,f,f)...
 * created this typemap for getValue(void) instead as a workaround.
 */
%typemap(out) float * {
  int i;
  $result = PyTuple_New(4);
  
  for (i=0; i<4; i++) {
    PyTuple_SetItem($result, i, PyFloat_FromDouble((double)(*($1+i))));
  }
}

%rename(SbVec4f_vec) SbVec4f::SbVec4f(const float v[4]);
%rename(SbVec4f_ffff) SbVec4f::SbVec4f(const float x, const float y, const float z, const float w);

%feature("shadow") SbVec4f::SbVec4f %{
def __init__(self,*args):
   newobj = None
   if len(args) == 1:
      if isinstance(args[0], SbVec4f):
         newobj = _coin.new_SbVec4f()
         newobj.setValue(args[0])
      else:
         newobj = apply(_coin.new_SbVec4f_vec,args)
   elif len(args) == 4:
      newobj = apply(_coin.new_SbVec4f_ffff,args)
   else:
      newobj = apply(_coin.new_SbVec4f,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}

/* add operator overloading methods instead of the global functions */
%extend SbVec4f {
  SbVec4f __add__(const SbVec4f &u) { return *self + u; }
  SbVec4f __sub__(const SbVec4f &u) { return *self - u; }
  SbVec4f __mul__(const float d) { return *self * d; }
  SbVec4f __rmul__(const float d) { return *self * d; }
  SbVec4f __div__(const float d) { return *self / d; }
  int __eq__(const SbVec4f &u) { return *self == u; }
  int __nq__(const SbVec4f &u) { return *self != u; }
  // swig - add a method for wrapping c++ operator[] access
  float __getitem__(int i) { return (self->getValue())[i]; }
  void  __setitem__(int i, float value) { (*self)[i] = value; }
}

%apply float *OUTPUT { float& x, float& y, float& z, float& w };

%ignore SbVec4f::getValue(float& x, float& y, float& z, float& w) const;
