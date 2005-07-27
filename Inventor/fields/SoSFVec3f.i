%typemap(in) float xyz[3] (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%rename(setValue_fff) SoSFVec3f::setValue(const float x, const float y, const float z);
%rename(setValue_vec) SoSFVec3f::setValue(SbVec3f const &);

%feature("shadow") SoSFVec3f::setValue(const float xyz[3]) %{
def setValue(*args):
   if len(args) == 4:
      return apply(_coin.SoSFVec3f_setValue_fff,args)
   elif isinstance(args[1],SbVec3f):
      return apply(_coin.SoSFVec3f_setValue_vec,args)
   return apply(_coin.SoSFVec3f_setValue,args)
%}

%extend SoSFVec3f {
  void __call__(SbVec3f & vec) { self->setValue(vec); }
  void __call__(const float x, const float y, const float z) { self->setValue(x,y,z); }
  void __call__(float xyz[3]) { self->setValue(xyz); }
}
