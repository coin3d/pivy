%{
static void
convert_SbVec4d_array(PyObject *input, double temp[4])
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

%typemap(in) double v[4] (double temp[4]) {
  convert_SbVec4d_array($input, temp);
  $1 = temp;
}

/* for some strange reason the %apply directive below doesn't work 
 * for this class on getValue(f,f,f,f)...
 * created this typemap for getValue(void) instead as a workaround.
 */
%typemap(out) double * {
  int i;
  $result = PyTuple_New(4);
  
  for (i=0; i<4; i++) {
	PyTuple_SetItem($result, i, PyFloat_FromDouble((double)(*($1+i))));
  }
}

%rename(SbVec4d_vec) SbVec4d::SbVec4d(const double v[4]);
%rename(SbVec4d_ffff) SbVec4d::SbVec4d(const double x, const double y, const double z, const double w);

%feature("shadow") SbVec4d::SbVec4d %{
def __init__(self,*args):
   if len(args) == 1:
      self.this = apply(_pivy.new_SbVec4d_vec,args)
      self.thisown = 1
      return
   elif len(args) == 4:
      self.this = apply(_pivy.new_SbVec4d_ffff,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SbVec3f,args)
   self.thisown = 1
%}

%rename(setValue_ffff) SbVec4d::setValue(const double x, const double y, const double z, const double w);

%feature("shadow") SbVec4d::setValue(const double vec[4]) %{
def setValue(*args):
   if len(args) == 5:
      return apply(_pivy.SbVec4d_setValue_ffff,args)
   return apply(_pivy.SbVec4d_setValue,args)
%}

%rename(SbVec4d_mul) operator *(const SbVec4d & v, const double d);
%rename(SbVec4d_d_mul) operator *(const double d, const SbVec4d & v);
%rename(SbVec4d_add) operator+(const SbVec4d & v1, const SbVec4d & v2);
%rename(SbVec4d_sub) operator-(const SbVec4d & v1, const SbVec4d & v2);
%rename(SbVec4d_div) operator /(const SbVec4d & v, const double d);
%rename(SbVec4d_eq) operator ==(const SbVec4d & v1, const SbVec4d & v2);
%rename(SbVec4d_neq) operator !=(const SbVec4d & v1, const SbVec4d & v2);

%apply double *OUTPUT { double& x, double& y, double& z, double& w };

%ignore SbVec4d::getValue(double& x, double& y, double& z, double& w) const;

// swig - add a method for wrapping c++ operator[] access
%extend SbVec4d {
  double __getitem__(int i) {
    return (self->getValue())[i];
  }
}
