%typemap(in) float hsv[3] (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%typemap(in) float rgb[3] (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%rename(setValue_col) SoSFColor::setValue(SbColor const &);
%rename(setValue_vec) SoSFColor::setValue(const SbVec3f &vec);
%rename(setValue_fff) SoSFColor::setValue(const float red, const float green, const float blue);

%feature("shadow") SoSFColor::setValue(const float rgb[3]) %{
def setValue(*args):
   if len(args) == 2:
      if isinstance(args[1], SbVec3f):
         return apply(_coin.SoSFColor_setValue_vec,args)
      else:
         return apply(_coin.SoSFColor_setValue_col,args)
   elif len(args) == 4:
      return apply(_coin.SoSFColor_setValue_fff,args)
   return apply(_coin.SoSFColor_setValue,args)
%}

%rename(setHSVValue_fff) SoSFColor::setHSVValue(const float h, const float s, const float v);

%feature("shadow") SoSFColor::setHSVValue(const float hsv[3]) %{
def setHSVValue(*args):
   if len(args) == 4:
      return apply(_coin.SoSFColor_setHSVValue_fff,args)
   return apply(_coin.SoSFColor_setHSVValue,args)
%}
