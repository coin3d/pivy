%typemap(in) double q[4] (double temp[4]) {
  convert_SbVec4d_array($input, temp);
  $1 = temp;
}

%typemap(typecheck) double q[4] {
  $1 = PySequence_Check($input) ? 1 : 0;
}

%typemap(out) float * {
  int i;
  $result = PyTuple_New(4);
  
  for (i=0; i<4; i++) {
    PyTuple_SetItem($result, i, PyFloat_FromDouble((double)(*($1+i))));
  }
}

%rename(SbDPRotation_vec_d) SbDPRotation::SbDPRotation(const SbVec3d & axis, const double radians);
%rename(SbDPRotation_arr) SbDPRotation::SbDPRotation(const double q[4]);
%rename(SbDPRotation_dddd) SbDPRotation::SbDPRotation(const double q0, const double q1, const double q2, const double q3);
%rename(SbDPRotation_mat) SbDPRotation::SbDPRotation(const SbMatrix & m);
%rename(SbDPRotation_vec_vec) SbDPRotation::SbDPRotation(const SbVec3d & rotateFrom, const SbVec3d & rotateTo);

%feature("shadow") SbDPRotation::SbDPRotation %{
def __init__(self,*args):
   newobj = None
   if len(args) == 1:
      if isinstance(args[0], SbMatrix):
         newobj = apply(_coin.new_SbDPRotation_mat,args)
      elif isinstance(args[0], SbDPRotation):
         newobj = _coin.new_SbDPRotation_arr(args[0].getValue())
      else:
         newobj = apply(_coin.new_SbDPRotation_arr,args)
   elif len(args) == 2:
      if isinstance(args[1], SbVec3f):
         newobj = apply(_coin.new_SbDPRotation_vec_vec,args)
      else:
         newobj = apply(_coin.new_SbDPRotation_vec_d,args)
   elif len(args) == 4:
      newobj = apply(_coin.new_SbDPRotation_dddd,args)
   else:
      newobj = apply(_coin.new_SbDPRotation,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}

/* add operator overloading methods instead of the global functions */
%extend SbDPRotation {
  SbDPRotation __mul__(const SbDPRotation &u) { return *self * u; }
  SbDPRotation __mul__(const double d) { SbDPRotation res(*self); return (res *= d); }
  SbVec3d __mul__(const SbVec3d & v) { SbVec3d res; self->multVec(v, res); return res; }
  int __eq__(const SbDPRotation &u) { return *self == u; }
  int __nq__(const SbDPRotation &u) { return *self != u; }
}

%apply float * OUTPUT { double & q0, double & q1, double & q2, double & q3, double & radians};

/* the next 2 typemaps handle the return value for getMatrix and getAxisAngle ~ getValue */
%typemap(in,numinputs=0) SbVec3d & axis, SbDPMatrix & matrix {
    $1 = new $1_basetype();
}
%typemap(argout) SbVec3d & axis, SbDPMatrix & matrix {
  $result = SWIG_NewPointerObj((void *) $1, $1_descriptor, 1);
}
/* undo effect of in typemap for setValue calls */
%typemap(in) const SbVec3d & axis = SWIGTYPE &;
%typemap(argout) const SbVec3d & axis {};

%ignore SbDPRotation::getValue(double & q0, double & q1, double & q2, double & q3) const;
%rename(getAxisAngle) SbDPRotation::getValue(SbVec3d & axis, double & radians) const;
%rename(getMatrix) SbDPRotation::getValue(SbDPMatrix & matrix) const;
