%typemap(in) double q[4] (double temp[4]) {
  convert_SbVec4d_array($input, temp);
  $1 = temp;
}

%typemap(out) float * {
  int i;
  $result = PyTuple_New(4);
  
  for (i=0; i<4; i++) {
	PyTuple_SetItem($result, i, PyFloat_FromDouble((double)(*($1+i))));
  }
}

%rename(SbDPRotation_vec_d) SbDPRotation::SbDPRotation(const SbVec3f & axis, const double radians);
%rename(SbDPRotation_arr) SbDPRotation::SbDPRotation(const double q[4]);
%rename(SbDPRotation_dddd) SbDPRotation::SbDPRotation(const double q0, const double q1, const double q2, const double q3);
%rename(SbDPRotation_mat) SbDPRotation::SbDPRotation(const SbMatrix & m);
%rename(SbDPRotation_vec_vec) SbDPRotation::SbDPRotation(const SbVec3f & rotateFrom, const SbVec3f & rotateTo);

%feature("shadow") SbDPRotation::SbDPRotation %{
def __init__(self,*args):
   newobj = None
   if len(args) == 1:
      if isinstance(args[0], SbMatrix):
         newobj = apply(_pivy.new_SbDPRotation_mat,args)
      else:
         newobj = apply(_pivy.new_SbDPRotation_arr,args)
   elif len(args) == 2:
      if isinstance(args[1], SbVec3f):
         newobj = apply(_pivy.new_SbDPRotation_vec_vec,args)
      else:
         newobj = apply(_pivy.new_SbDPRotation_vec_d,args)
   elif len(args) == 4:
      newobj = apply(_pivy.new_SbDPRotation_dddd,args)
   else:
      newobj = apply(_pivy.new_SbDPRotation,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
%}

%rename(setValue_arr) SbDPRotation::setValue(const double q[4]);
%rename(setValue_mat) SbDPRotation::setValue(const SbMatrix & m);
%rename(setValue_vec_d) SbDPRotation::setValue(const SbVec3f & axis, const double radians);
%rename(setValue_vec_vec) SbDPRotation::setValue(const SbVec3f & rotateFrom, const SbVec3f & rotateTo);

%feature("shadow") SbDPRotation::setValue(const double q0, const double q1, const double q2, const double q3) %{
def setValue(*args):
   if len(args) == 2:
      if isinstance(args[1], SbMatrix):
         return apply(_pivy.SbDPRotation_setValue_mat,args)
      else:
         return apply(_pivy.SbDPRotation_setValue_arr,args)
   elif len(args) == 3:
      if isinstance(args[2], SbVec3f):
         return apply(_pivy.SbDPRotation_setValue_vec_vec,args)
      else:
         return apply(_pivy.SbDPRotation_setValue_vec_d,args)
   return apply(_pivy.SbDPRotation_setValue,args)
%}

%rename(SbDPRotation_eq) operator ==(const SbDPRotation & q1, const SbDPRotation & q2);
%rename(SbDPRotation_neq) operator !=(const SbDPRotation & q1, const SbDPRotation & q2);
%rename(SbDPRotation_mul) operator *(const SbDPRotation & q1, const SbDPRotation & q2);

%ignore SbDPRotation::getValue(double & q0, double & q1, double & q2, double & q3) const;
%ignore SbDPRotation::getValue(SbVec3f & axis, double & radians) const;
%ignore SbDPRotation::getValue(SbMatrix & matrix) const;
