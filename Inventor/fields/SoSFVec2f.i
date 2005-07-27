%typemap(in) float xy[2] (float temp[2]) {
  convert_SbVec2f_array($input, temp);
  $1 = temp;
}

%rename(setValue_ff) SoSFVec2f::setValue(const float x, const float y);
%rename(setValue_vec) SoSFVec2f::setValue(SbVec2f const &);

%feature("shadow") SoSFVec2f::setValue(const float xy[2]) %{
def setValue(*args):
   if len(args) == 3:
      return apply(_coin.SoSFVec2f_setValue_ff,args)
   elif isinstance(args[1],SbVec2f):
      return apply(_coin.SoSFVec2f_setValue_vec,args)
   return apply(_coin.SoSFVec2f_setValue,args)
%}

%extend SoSFVec2f {
  void __call__(const float x, const float y) { self->setValue(x,y); }
  void __call__(float xy[2]) { self->setValue(xy); }
  void __call__(SbVec2f & vec) { self->setValue(vec); }
}
