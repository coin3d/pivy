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
   newobj = None
   if len(args) == 1:
      if isinstance(args[0], SbVec3s):
         newobj = _coin.new_SbVec3s()
         newobj.setValue(args[0])
      else:
         newobj = apply(_coin.new_SbVec3s_vec,args)
   elif len(args) == 3:
      newobj = apply(_coin.new_SbVec3s_ss,args)
   else:
      newobj = apply(_coin.new_SbVec3s,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}

%rename(setValue_ss) SbVec3s::setValue(short x, short y, short z);

%feature("shadow") SbVec3s::setValue(const short v[3]) %{
def setValue(*args):
   if len(args) == 4:
      return apply(_coin.SbVec3s_setValue_ss,args)
   if len(args) == 2:
      if isinstance(args[1], SbVec3s):
         return _coin.SbVec3s_setValue(args[0], args[1].getValue())
   return apply(_coin.SbVec3s_setValue,args)
%}

/* add operator overloading methods instead of the global functions */
%extend SbVec3s {
  SbVec3s __add__(const SbVec3s &u) { return *self + u; }
  SbVec3s __sub__(const SbVec3s &u) { return *self - u; }
  SbVec3s __mul__(const double d) { return *self * d; }
  SbVec3s __rmul__(const double d) { return *self * d; }
  SbVec3s __div__(const double d) { return *self / d; }
  int __eq__(const SbVec3s &u) { return *self == u; }
  int __nq__(const SbVec3s &u) { return *self != u; }
  // add a method for wrapping c++ operator[] access
  short __getitem__(int i) { return (self->getValue())[i]; }
  void  __setitem__(int i, short value) { (*self)[i] = value; }
}

%apply short *OUTPUT { short &x, short &y, short &z };

%ignore SbVec3s::getValue(void) const;
