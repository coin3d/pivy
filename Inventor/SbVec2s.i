%{
static void
convert_SbVec2s_array(PyObject *input, short temp[2])
{
  if (PySequence_Check(input) && (PySequence_Size(input) == 2) &&
      PyNumber_Check(PySequence_GetItem(input, 0)) && 
      PyNumber_Check(PySequence_GetItem(input, 1))) {
    temp[0] = PyInt_AsLong(PySequence_GetItem(input, 0));
    temp[1] = PyInt_AsLong(PySequence_GetItem(input, 1));
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence with 2 shorts");
    PyErr_Print();
  } 
}
%}

%typemap(in) short v[2] (short temp[2]) {
  convert_SbVec2s_array($input, temp);
  $1 = temp;
}

%rename(SbVec2s_vec) SbVec2s::SbVec2s(const short v[2]);
%rename(SbVec2s_ss) SbVec2s::SbVec2s(const short x, const short y);

%feature("shadow") SbVec2s::SbVec2s %{
def __init__(self,*args):
   if len(args) == 1:
      self.this = apply(_pivy.new_SbVec2s_vec,args)
      self.thisown = 1
      return
   elif len(args) == 2:
      self.this = apply(_pivy.new_SbVec2s_ss,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SbVec2s,args)
   self.thisown = 1
%}

%rename(setValue_ss) SbVec2s::setValue(short x, short y);

%feature("shadow") SbVec2s::setValue(const short v[2]) %{
def setValue(*args):
   if len(args) == 3:
      return apply(_pivy.SbVec2s_setValue_ss,args)
   return apply(_pivy.SbVec2s_setValue,args)
%}

%rename(SbVec2s_mul) operator *(const SbVec2s &v, double d);
%rename(SbVec2s_d_mul) operator *(double d, const SbVec2s &v);
%rename(SbVec2s_add) operator +(const SbVec2s &v1, const SbVec2s &v2);
%rename(SbVec2s_sub) operator -(const SbVec2s &v1, const SbVec2s &v2);
%rename(SbVec2s_div) operator /(const SbVec2s &c, double d);
%rename(SbVec2s_eq) operator ==(const SbVec2s &v1, const SbVec2s &v2);
%rename(SbVec2s_neq) operator !=(const SbVec2s &v1, const SbVec2s &v2);

%apply short *OUTPUT { short &x, short &y };

%ignore SbVec2s::getValue(void) const;

// add a method for wrapping c++ operator[] access
%extend SbVec2s {
  short __getitem__(int i) {
    return (self->getValue())[i];
  }
}
