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
   newobj = None
   if len(args) == 1:
      if isinstance(args[0], SbVec3f):
         newobj = _pivy.new_SbVec3f()
         newobj.setValue(args[0])
      else:
         newobj = apply(_pivy.new_SbVec3f_vec,args)
   elif len(args) == 3:
      if isinstance(args[0], SbPlane):
         newobj = apply(_pivy.new_SbVec3f_pl_pl_pl,args)
      else:
         newobj = apply(_pivy.new_SbVec3f_fff,args)
   else:
      newobj = apply(_pivy.new_SbVec3f,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
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
      if isinstance(args[1], SbVec3d):
         return apply(_pivy.SbVec3f_setValue_vec,args)
      elif isinstance(args[1], SbVec3f):
         return _pivy.SbVec3f_setValue(args[0],args[1].getValue())
   return apply(_pivy.SbVec3f_setValue,args)
%}

/* add operator overloading methods instead of the global functions */
%extend SbVec3f {
    SbVec3f __add__( const SbVec3f &u)
    {
        return *self + u;
    };
    
    SbVec3f __sub__( const SbVec3f &u)    
    {
       return *self - u;
    };
        
    SbVec3f __mul__( const float d)
    {
       return *self * d;
    };
    
    SbVec3f __rmul__( const float d)
    {
           return *self * d;
    };
        
    SbVec3f __div__( const float d)
    {
        return *self / d;
    };
        
    int __eq__( const SbVec3f &u )
    {
        return *self == u;
    };
    
    int __nq__( const SbVec3f &u )
    {
        return *self != u;
    };    
}

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
