%{
static void
convert_SbVec3s_array(PyObject *input, short temp[3])
{
  if (PySequence_Check(input) && (PySequence_Size(input) == 3) &&
      PyNumber_Check(PySequence_GetItem(input, 0)) && 
      PyNumber_Check(PySequence_GetItem(input, 1)) &&
      PyNumber_Check(PySequence_GetItem(input, 2))) {
    temp[0] = PyInt_AsLong(PySequence_GetItem(input, 0));
    temp[1] = PyInt_AsLong(PySequence_GetItem(input, 1));
    temp[2] = PyInt_AsLong(PySequence_GetItem(input, 2));
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence with 3 shorts");
    PyErr_Print();
  } 
}
%}

%typemap(in) short v[3] (short temp[3]) {
  convert_SbVec3s_array($input, temp);
  $1 = temp;
}

%rename(SbVec3s_vec) SbVec3s::SbVec3s(const short v[3]);
%rename(SbVec3s_ss) SbVec3s::SbVec3s(const short x, const short y, const short z);

%feature("shadow") SbVec3s::SbVec3s %{
def __init__(self,*args):
   if len(args) == 1:
      self.this = apply(_pivy.new_SbVec3s_vec,args)
      self.thisown = 1
      return
   elif len(args) == 3:
      self.this = apply(_pivy.new_SbVec3s_ss,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SbVec3s,args)
   self.thisown = 1
%}

%rename(setValue_ss) SbVec3s::setValue(short x, short y, short z);

%feature("shadow") SbVec3s::setValue(const short v[3]) %{
def setValue(*args):
   if len(args) == 4:
      return apply(_pivy.SbVec3s_setValue_ss,args)
   return apply(_pivy.SbVec3s_setValue,args)
%}

%rename(SbVec3s_mul) operator *(const SbVec3s & v, double d);
%rename(SbVec3s_d_mul) operator *(double d, const SbVec3s & v);
%rename(SbVec3s_add) operator+(const SbVec3s & v1, const SbVec3s & v2);
%rename(SbVec3s_sub) operator-(const SbVec3s & v1, const SbVec3s & v2);
%rename(SbVec3s_div) operator /(const SbVec3s & v, double d);
%rename(SbVec3s_eq) operator ==(const SbVec3s & v1, const SbVec3s & v2);
%rename(SbVec3s_neq) operator !=(const SbVec3s & v1, const SbVec3s & v2);


%apply short *OUTPUT { short &x, short &y, short &z };

%ignore SbVec3s::getValue(void) const;

// add a method for wrapping c++ operator[] access
%extend SbVec3s {
  short __getitem__(int i) {
    return (self->getValue())[i];
  }
}
