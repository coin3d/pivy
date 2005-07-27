%typemap(in) float xyzw[4] (float temp[4]) {
  convert_SbVec4f_array($input, temp);
  $1 = temp;
}

%rename(setValue_ffff) SoSFVec4f::setValue(const float x, const float y, const float z, const float w);
%rename(setValue_vec) SoSFVec4f::setValue(SbVec4f const &);

%feature("shadow") SoSFVec4f::setValue(const float xyzw[4]) %{
def setValue(*args):
   if len(args) == 5:
      return apply(_coin.SoSFVec4f_setValue_ffff,args)
   elif isinstance(args[1],SbVec4f):
      return apply(_coin.SoSFVec4f_setValue_vec,args)
   return apply(_coin.SoSFVec4f_setValue,args)
%}

%extend SoSFVec4f {
  void __call__(const SbVec4f & vec) { self->setValue(vec); }
  void __call__(const float x, const float y, const float z, const float w) { self->setValue(x,y,z,w); }
  void __call__(float xyzw[4]) { self->setValue(xyzw); }
}
