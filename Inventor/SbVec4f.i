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
   if len(args) == 1:
      self.this = apply(_pivy.new_SbVec4f_vec,args)
      self.thisown = 1
      return
   elif len(args) == 4:
      self.this = apply(_pivy.new_SbVec4f_ffff,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SbVec3f,args)
   self.thisown = 1
%}

%rename(setValue_ffff) SbVec4f::setValue(const float x, const float y, const float z, const float w);

%feature("shadow") SbVec4f::setValue(const float vec[4]) %{
def setValue(*args):
   if len(args) == 5:
      return apply(_pivy.SbVec4f_setValue_ffff,args)
   return apply(_pivy.SbVec4f_setValue,args)
%}

%apply float *OUTPUT { float& x, float& y, float& z, float& w };

%ignore SbVec4f::getValue(float& x, float& y, float& z, float& w) const;

// swig - add a method for wrapping c++ operator[] access
%extend SbVec4f {
  float __getitem__(int i) {
    return (self->getValue())[i];
  }
}
