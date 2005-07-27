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
   newobj = None
   if len(args) == 1:
      if isinstance(args[0], SbVec2s):
         newobj = _coin.new_SbVec2s()
         newobj.setValue(args[0])
      else:
         newobj = apply(_coin.new_SbVec2s_vec,args)
   elif len(args) == 2:
      newobj = apply(_coin.new_SbVec2s_ss,args)
   else:
      newobj = apply(_coin.new_SbVec2s,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}

%rename(setValue_ss) SbVec2s::setValue(short x, short y);

%feature("shadow") SbVec2s::setValue(const short v[2]) %{
def setValue(*args):
   if len(args) == 2:
      if isinstance(args[1], SbVec2s):
         return _coin.SbVec2s_setValue(args[0], args[1].getValue())
   elif len(args) == 3:
      return apply(_coin.SbVec2s_setValue_ss,args)
   return apply(_coin.SbVec2s_setValue,args)
%}

/* add operator overloading methods instead of the global functions */
%extend SbVec2s {
  SbVec2s __add__(const SbVec2s &u) { return *self + u; }
  SbVec2s __sub__(const SbVec2s &u) { return *self - u; }
  SbVec2s __mul__(const double d) { return *self * d; }
  SbVec2s __rmul__(const double d) { return *self * d; }
  SbVec2s __div__(const double d) { return *self / d; }
  int __eq__(const SbVec2s &u) { return *self == u; }
  int __nq__(const SbVec2s &u ) { return *self != u; }
  // add a method for wrapping c++ operator[] access
  short __getitem__(int i) { return (self->getValue())[i]; }
  void  __setitem__(int i, short value) { (*self)[i] = value; }
}

%apply short *OUTPUT { short &x, short &y };

%ignore SbVec2s::getValue() const;
