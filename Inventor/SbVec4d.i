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
   newobj = None
   if len(args) == 1:
      if isinstance(args[0], SbVec4d):
         newobj = _pivy.new_SbVec4d()
         newobj.setValue(args[0])
      else:
         newobj = apply(_pivy.new_SbVec4d_vec,args)
   elif len(args) == 4:
      newobj = apply(_pivy.new_SbVec4d_ffff,args)
   else:
      newobj = apply(_pivy.new_SbVec4d,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}

%rename(setValue_ffff) SbVec4d::setValue(const double x, const double y, const double z, const double w);

%feature("shadow") SbVec4d::setValue(const double vec[4]) %{
def setValue(*args):
   if len(args) == 5:
      return apply(_pivy.SbVec4d_setValue_ffff,args)
   if len(args) == 2:
      if isinstance(args[1], SbVec4d):
         return _pivy.SbVec4d_setValue(args[0],args[1].getValue())      
   return apply(_pivy.SbVec4d_setValue,args)
%}

/* add operator overloading methods instead of the global functions */
%extend SbVec4d {
    SbVec4d __add__( const SbVec4d &u)
    {
        return *self + u;
    };
    
    SbVec4d __sub__( const SbVec4d &u)    
    {
       return *self - u;
    };
    
    SbVec4d __mul__( const double d)
    {
       return *self * d;
    };
    
    SbVec4d __rmul__( const double d)
    {
           return *self * d;
    };
    
    SbVec4d __div__( const double d)
    {
        return *self / d;
    };
    
    int __eq__( const SbVec4d &u )
    {
        return *self == u;
    };
    
    int __nq__( const SbVec4d &u )
    {
        return *self != u;
    };    
}

%apply double *OUTPUT { double& x, double& y, double& z, double& w };

%ignore SbVec4d::getValue(double& x, double& y, double& z, double& w) const;

// swig - add a method for wrapping c++ operator[] access
%extend SbVec4d {
  double __getitem__(int i) {
    return (self->getValue())[i];
  }
  void  __setitem__(int i, double value) {
    (*self)[i] = value;
  }
}
