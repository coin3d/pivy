%typemap(in) float hsv[3] (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%typemap(typecheck) float hsv[3] {
  $1 = PySequence_Check($input) ? 1 : 0;
}

%typemap(in) float *rgb (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%typemap(typecheck) float *rgb = float hsv[3];

%rename(SbColor_vec) SbColor::SbColor(const SbVec3f &v);
%rename(SbColor_rgb) SbColor::SbColor(const float *const rgb);
%rename(SbColor_fff) SbColor::SbColor(const float r, const float g, const float b);

%feature("shadow") SbColor::SbColor %{
def __init__(self,*args):
   newobj = None
   if len(args) == 1:
      if isinstance(args[0], SbVec3f):
         newobj = apply(_coin.new_SbColor_vec,args)
      else:
         newobj = apply(_coin.new_SbColor_rgb,args)
   elif len(args) == 3:
      newobj = apply(_coin.new_SbColor_fff,args)
   else:
      newobj = apply(_coin.new_SbColor,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}

%apply float *OUTPUT { float & h, float & s, float & v };

%ignore SbColor::getHSVValue(float hsv[3]) const;

%extend SbColor {
  SbColor __add__(const SbColor &u) { return *self + u; }
  SbColor __sub__(const SbColor &u) { return *self - u; }
  SbColor __mul__(const float d) { return *self * d; }
  SbColor __rmul__(const float d) { return *self * d; }
  SbColor __div__( const float d) { return *self / d; }
  int __eq__(const SbColor &u ) { return *self == u; }
  int __nq__(const SbColor &u) { return *self != u; }
  float __getitem__(int i) { return (self->getValue())[i]; }
  void  __setitem__(int i, float value) { (*self)[i] = value; }
}
