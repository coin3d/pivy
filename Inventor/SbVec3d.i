%{
static void
convert_SbVec3d_array(PyObject *input, double temp[3])
{
  if (PySequence_Check(input) && (PySequence_Size(input) == 3) &&
      PyNumber_Check(PySequence_GetItem(input, 0)) && 
      PyNumber_Check(PySequence_GetItem(input, 1)) && 
      PyNumber_Check(PySequence_GetItem(input, 2))) {
    temp[0] = PyFloat_AsDouble(PySequence_GetItem(input, 0));
    temp[1] = PyFloat_AsDouble(PySequence_GetItem(input, 1));
    temp[2] = PyFloat_AsDouble(PySequence_GetItem(input, 2));
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence with 3 doubles");
    PyErr_Print();
  } 
}
%}

%typemap(in) double v[3] (double temp[3]) {
  convert_SbVec3d_array($input, temp);
  $1 = temp;
}

/* for some strange reason the %apply directive below doesn't work 
 * for this class on getValue(f,f,f)...
 * created this typemap for getValue(void) instead as a workaround.
 */
%typemap(out) double * {
  int i;
  $result = PyTuple_New(3);
  
  for (i=0; i<3; i++) {
	PyTuple_SetItem($result, i, PyFloat_FromDouble((double)(*($1+i))));
  }
}

%rename(SbVec3d_vec) SbVec3d::SbVec3d(const double v[3]);
%rename(SbVec3d_fff) SbVec3d::SbVec3d(const double x, const double y, const double z);
%rename(SbVec3d_pl_pl_pl) SbVec3d::SbVec3d(const SbPlane & p0, const SbPlane & p1, const SbPlane & p2);

%feature("shadow") SbVec3d::SbVec3d %{
def __init__(self,*args):
   if len(args) == 1:
      self.this = apply(_pivy.new_SbVec3d_vec,args)
      self.thisown = 1
      return
   elif len(args) == 3:
      if isinstance(args[0], SbPlane):
         self.this = apply(_pivy.new_SbVec3d_pl_pl_pl,args)
         self.thisown = 1
         return
      else:
         self.this = apply(_pivy.new_SbVec3d_fff,args)
         self.thisown = 1
         return
   self.this = apply(_pivy.new_SbVec3d,args)
   self.thisown = 1
%}

%rename(setValue_fff) SbVec3d::setValue(const double x, const double y, const double z);
%rename(setValue_vec_vec_vec_vec) SbVec3d::setValue(const SbVec3d & barycentric, const SbVec3d & v0, const SbVec3d & v1, const SbVec3d & v2);
%rename(setValue_vec) SbVec3d::setValue(const SbVec3d & v);

%feature("shadow") SbVec3d::setValue(const double vec[3]) %{
def setValue(*args):
   if len(args) == 4:
      return apply(_pivy.SbVec3d_setValue_fff,args)
   elif len(args) == 5:
      return apply(_pivy.SbVec3d_setValue_vec_vec_vec_vec,args)
   elif len(args) == 2:
      return apply(_pivy.SbVec3d_setValue_vec,args)
   return apply(_pivy.SbVec3d_setValue,args)
%}

%rename(SbVec3d_mul) operator *(const SbVec3d & v, const double d);
%rename(SbVec3d_d_mul) operator *(const double d, const SbVec3d & v);
%rename(SbVec3d_add) operator+(const SbVec3d & v1, const SbVec3d & v2);
%rename(SbVec3d_sub) operator-(const SbVec3d & v1, const SbVec3d & v2);
%rename(SbVec3d_div) operator /(const SbVec3d & v, const double d);
%rename(SbVec3d_eq) operator ==(const SbVec3d & v1, const SbVec3d & v2);
%rename(SbVec3d_neq) operator !=(const SbVec3d & v1, const SbVec3d & v2);

%apply double *OUTPUT { double & x, double & y, double & z };

%ignore SbVec3d::getValue(double & x, double & y, double & z) const;

// add a method for wrapping c++ operator[] access
%extend SbVec3d {
  float __getitem__(int i) {
    return (self->getValue())[i];
  }
  void  __setitem__(int i, float value) {
    (*self)[i] = value;
  }
}
