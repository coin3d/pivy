%{
static void
convert_SbVec2f_array(PyObject *input, float temp[2])
{
  if (PySequence_Check(input) && (PySequence_Size(input) == 2) &&
      PyNumber_Check(PySequence_GetItem(input, 0)) && 
      PyNumber_Check(PySequence_GetItem(input, 1))) {
    temp[0] = PyFloat_AsDouble(PySequence_GetItem(input, 0));
    temp[1] = PyFloat_AsDouble(PySequence_GetItem(input, 1));
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence with 2 floats");
    PyErr_Print();
  } 
}
%}

%typemap(in) float v[2] (float temp[2]) {
  convert_SbVec2f_array($input, temp);
  $1 = temp;
}

%rename(SbVec2f_vec) SbVec2f::SbVec2f(const float v[2]);
%rename(SbVec2f_ff) SbVec2f::SbVec2f(const float x, const float y);

%feature("shadow") SbVec2f::SbVec2f %{
def __init__(self,*args):
   newobj = None
   if len(args) == 1:
      newobj = apply(_pivy.new_SbVec2f_vec,args)
   elif len(args) == 2:
      newobj = apply(_pivy.new_SbVec2f_ff,args)
   else:
      self.this = apply(_pivy.new_SbVec2f,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}

%rename(setValue_ff) SbVec2f::setValue(const float x, const float y);

%feature("shadow") SbVec2f::setValue(const float vec[2]) %{
def setValue(*args):
   if len(args) == 3:
      return apply(_pivy.SbVec2f_setValue_ff,args)
   return apply(_pivy.SbVec2f_setValue,args)
%}

/* add operator overloading methods instead of the global functions */
%extend SbVec2f {
    SbVec2f __add__( const SbVec2f &u)
    {
        return *self + u;
    };
    
    SbVec2f __sub__( const SbVec2f &u)    
    {
       return *self - u;
    };
        
    SbVec2f __mul__( const float d)
    {
       return *self * d;
    };
    
    SbVec2f __rmul__( const float d)
    {
           return *self * d;
    };
       
    SbVec2f __div__( const float d)
    {
        return *self / d;
    };
    
    int __eq__( const SbVec2f &u )
    {
        return *self == u;
    };
    
    int __nq__( const SbVec2f &u )
    {
        return *self != u;
    };
}

%apply float *OUTPUT { float & x, float & y };

%ignore SbVec2f::getValue(void) const;

// add a method for wrapping c++ operator[] access
%extend SbVec2f {
  float __getitem__(int i) {
    return (self->getValue())[i];
  }
}
