%{
static void
convert_SbVec3f_array(PyObject *input, float temp[3])
{
  if (PySequence_Check(input) && (PySequence_Size(input) == 3) &&
      PyNumber_Check(PySequence_GetItem(input, 0)) && 
      PyNumber_Check(PySequence_GetItem(input, 1)) && 
      PyNumber_Check(PySequence_GetItem(input, 2))) {
    temp[0] = PyFloat_AsDouble(PySequence_GetItem(input, 0));
    temp[1] = PyFloat_AsDouble(PySequence_GetItem(input, 1));
    temp[2] = PyFloat_AsDouble(PySequence_GetItem(input, 2));
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence with 3 floats");
    PyErr_Print();
  } 
}
%}

%typemap(in) float v[3] (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

/* for some strange reason the %apply directive below doesn't work 
 * for this class on getValue(f,f,f)...
 * created this typemap for getValue(void) instead as a workaround.
 */
%typemap(out) float * {
  int i;
  $result = PyTuple_New(3);
  
  for (i=0; i<3; i++) {
	PyTuple_SetItem($result, i, PyFloat_FromDouble((double)(*($1+i))));
  }
}

%rename(SbVec3f_vec) SbVec3f::SbVec3f(const float v[3]);
%rename(SbVec3f_fff) SbVec3f::SbVec3f(const float x, const float y, const float z);
%rename(SbVec3f_pl_pl_pl) SbVec3f::SbVec3f(const SbPlane & p0, const SbPlane & p1, const SbPlane & p2);

%feature("shadow") SbVec3f::SbVec3f %{
def __init__(self,*args):
   if len(args) == 1:
      self.this = apply(_pivy.new_SbVec3f_vec,args)
      self.thisown = 1
      return
   elif len(args) == 3:
      if isinstance(args[0], SbPlane):
         self.this = apply(_pivy.new_SbVec3f_pl_pl_pl,args)
         self.thisown = 1
         return
      else:
         self.this = apply(_pivy.new_SbVec3f_fff,args)
         self.thisown = 1
         return
   self.this = apply(_pivy.new_SbVec3f,args)
   self.thisown = 1
%}

%rename(setValue_fff) SbVec3f::setValue(const float x, const float y, const float z);
%rename(setValue_vec_vec_vec_vec) SbVec3f::setValue(const SbVec3f & barycentric, const SbVec3f & v0, const SbVec3f & v1, const SbVec3f & v2);
%rename(setValue_vec) SbVec3f::setValue(const SbVec3d & v);

%feature("shadow") SbVec3f::setValue(const float vec[3]) %{
def setValue(*args):
   if len(args) == 4:
      return apply(_pivy.SbVec3f_setValue_fff,args)
   elif len(args) == 5:
      return apply(_pivy.SbVec3f_setValue_vec_vec_vec_vec,args)
   elif len(args) == 2:
      return apply(_pivy.SbVec3f_setValue_vec,args)
   return apply(_pivy.SbVec3f_setValue,args)
%}

%rename(SbVec3f_mul) operator *(const SbVec3f & v, const float d);
%rename(SbVec3f_d_mul) operator *(const float d, const SbVec3f & v);
%rename(SbVec3f_add) operator+(const SbVec3f & v1, const SbVec3f & v2);
%rename(SbVec3f_sub) operator-(const SbVec3f & v1, const SbVec3f & v2);
%rename(SbVec3f_div) operator /(const SbVec3f & v, const float d);
%rename(SbVec3f_eq) operator ==(const SbVec3f & v1, const SbVec3f & v2);
%rename(SbVec3f_neq) operator !=(const SbVec3f & v1, const SbVec3f & v2);

%apply float *OUTPUT { float & x, float & y, float & z };

%ignore SbVec3f::getValue(float & x, float & y, float & z) const;

// add a method for wrapping c++ operator[] access
%extend SbVec3f {
  float __getitem__(int i) {
    return (self->getValue())[i];
  }
  void  __setitem__(int i, float value) {
    (*self)[i] = value;
  }
}
