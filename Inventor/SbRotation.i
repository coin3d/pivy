%typemap(in) float q[4] (float temp[4]) {
  convert_SbVec4f_array($input, temp);
  $1 = temp;
}

%typemap(out) float * {
  int i;
  $result = PyTuple_New(4);
  
  for (i=0; i<4; i++) {
	PyTuple_SetItem($result, i, PyFloat_FromDouble((double)(*($1+i))));
  }
}

%rename(SbRotation_vec_f) SbRotation::SbRotation(const SbVec3f & axis, const float radians);
%rename(SbRotation_arr) SbRotation::SbRotation(const float q[4]);
%rename(SbRotation_ffff) SbRotation::SbRotation(const float q0, const float q1, const float q2, const float q3);
%rename(SbRotation_mat) SbRotation::SbRotation(const SbMatrix & m);
%rename(SbRotation_vec_vec) SbRotation::SbRotation(const SbVec3f & rotateFrom, const SbVec3f & rotateTo);

%feature("shadow") SbRotation::SbRotation %{
def __init__(self,*args):
   newobj = None
   if len(args) == 1:
      if isinstance(args[0], SbMatrix):
         newobj = apply(_pivy.new_SbRotation_mat,args)
      else:
         newobj = apply(_pivy.new_SbRotation_arr,args)
   elif len(args) == 2:
      if isinstance(args[1], SbVec3f):
         newobj = apply(_pivy.new_SbRotation_vec_vec,args)
      else:
         newobj = apply(_pivy.new_SbRotation_vec_f,args)
   elif len(args) == 4:
      newobj = apply(_pivy.new_SbRotation_ffff,args)
   else:
      newobj = apply(_pivy.new_SbRotation,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
%}

%rename(setValue_arr) SbRotation::setValue(const float q[4]);
%rename(setValue_mat) SbRotation::setValue(const SbMatrix & m);
%rename(setValue_vec_f) SbRotation::setValue(const SbVec3f & axis, const float radians);
%rename(setValue_vec_vec) SbRotation::setValue(const SbVec3f & rotateFrom, const SbVec3f & rotateTo);

%feature("shadow") SbRotation::setValue(const float q0, const float q1, const float q2, const float q3) %{
def setValue(*args):
   if len(args) == 2:
      if isinstance(args[1], SbMatrix):
         return apply(_pivy.SbRotation_setValue_mat,args)
      else:
         return apply(_pivy.SbRotation_setValue_arr,args)
   elif len(args) == 3:
      if isinstance(args[2], SbVec3f):
         return apply(_pivy.SbRotation_setValue_vec_vec,args)
      else:
         return apply(_pivy.SbRotation_setValue_vec_f,args)
   return apply(_pivy.SbRotation_setValue,args)
%}

/* add operator overloading methods instead of the global functions */
%extend SbRotation {
   
    SbRotation __mul__( const SbRotation &u )
    {
       return *self * u;
    };
    
    SbRotation __mul__( const double d )
    {
        SbRotation res(*self);
        res *= d;
        return res;
    };        
        
    SbVec3f __mul__( const SbVec3f & v )
    {
        SbVec3f res;
        self->multVec( v, res );
        return res;
    };
    
    int __eq__( const SbRotation &u )
    {
        return *self == u;
    };
    
    int __nq__( const SbRotation &u )
    {
        return *self != u;
    };
}

%ignore SbRotation::getValue(float & q0, float & q1, float & q2, float & q3) const;
%ignore SbRotation::getValue(SbVec3f & axis, float & radians) const;
%ignore SbRotation::getValue(SbMatrix & matrix) const;
