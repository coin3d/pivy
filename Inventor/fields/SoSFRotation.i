%typemap(in) float q[4] (float temp[4]) {
  convert_SbVec4f_array($input, temp);
  $1 = temp;
}

%rename(setValue_rot) SoSFRotation::setValue(SbRotation const &);
%rename(setValue_ffff) SoSFRotation::setValue(const float q0, const float q1, const float q2, const float q3);
%rename(setValue_array) SoSFRotation::setValue(const float q[4]);

%feature("shadow") SoSFRotation::setValue(const SbVec3f & axis, const float angle) %{
def setValue(*args):
   if len(args) == 5:
      return apply(_pivy.SoSFRotation_setValue_ffff,args)
   if len(args) == 2:
      if isinstance(args[1], SbRotation):
         return apply(_pivy.SoSFRotation_setValue_rot,args)
      else:
         return apply(_pivy.SoSFRotation_setValue_array,args)
   return apply(_pivy.SoSFRotation_setValue,args)
%}

%extend SoSFRotation {
  void __call__(SbVec3f & axis, float angle) {
    self->setValue(axis, angle);
  }
  void __call__(const float q0, const float q1, const float q2, const float q3) {
    self->setValue(q0, q1, q2, q3);
  }
  void __call__(float q[4]) {
    self->setValue(q);
  }
  void __call__(const SbRotation & o) {
    self->setValue(o);
  }
}
