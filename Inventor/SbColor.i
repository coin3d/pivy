%typemap(in) float hsv[3] (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%typemap(in) float *rgb (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%rename(SbColor_vec) SbColor::SbColor(const SbVec3f &v);
%rename(SbColor_rgb) SbColor::SbColor(const float *const rgb);
%rename(SbColor_fff) SbColor::SbColor(const float r, const float g, const float b);

%feature("shadow") SbColor::SbColor %{
def __init__(self,*args):
   newobj = None
   if len(args) == 1:
      if isinstance(args[0], SbVec3f):
         newobj = apply(_pivy.new_SbColor_vec,args)
      else:
         newobj = apply(_pivy.new_SbColor_rgb,args)
   elif len(args) == 3:
      newobj = apply(_pivy.new_SbColor_fff,args)
   else:
      newobj = apply(_pivy.new_SbColor,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}

%rename(setHSVValue_fff) SbColor::setHSVValue(float h, float s, float v);

%feature("shadow") SbColor::setHSVValue(const float hsv[3]) %{
def setHSVValue(*args):
   if len(args) == 4:
      return apply(_pivy.SbColor_setHSVValue_fff,args)
   return apply(_pivy.SbColor_setHSVValue,args)
%}

%apply float *OUTPUT { float & h, float & s, float & v };

%ignore SbColor::getHSVValue(float hsv[3]) const;

%rename(SbColor_mul) operator *(const SbColor & v, const float d);
%rename(SbColor_d_mul) operator *(const float d, const SbColor & v);
%rename(SbColor_add) operator+(const SbColor & v1, const SbColor & v2);
%rename(SbColor_sub) operator-(const SbColor & v1, const SbColor & v2);
%rename(SbColor_div) operator /(const SbColor & v, const float d);
%rename(SbColor_eq) operator ==(const SbColor & v1, const SbColor & v2);
%rename(SbColor_neq) operator !=(const SbColor & v1, const SbColor & v2);

COIN_DLL_API SbColor operator *(const SbColor & v, const float d);
COIN_DLL_API SbColor operator *(const float d, const SbColor & v);
COIN_DLL_API SbColor operator /(const SbColor & v, const float d);
COIN_DLL_API SbColor operator +(const SbColor & v1, const SbColor & v2);
COIN_DLL_API SbColor operator -(const SbColor & v1, const SbColor & v2);
COIN_DLL_API int operator ==(const SbColor & v1, const SbColor & v2);
COIN_DLL_API int operator !=(const SbColor & v1, const SbColor & v2);
