%typemap(in) float col[4] (float temp[4]) {
  convert_SbVec4f_array($input, temp);
  $1 = temp;
}

%typemap(in) float * rgba (float temp[4]) {
  convert_SbVec4f_array($input, temp);
  $1 = temp;
}

%typemap(in) float hsv[3] (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%typemap(in) float *rgb (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%rename(SbColor4f_col_f) SbColor4f::SbColor4f(const SbColor &rgb, const float alpha);
%rename(SbColor4f_vec) SbColor4f::SbColor4f(const SbVec4f &v);
%rename(SbColor4f_rgb) SbColor4f::SbColor4f(const float *const rgba);
%rename(SbColor4f_ffff) SbColor4f::SbColor4f(const float r, const float g, const float b, const float a=1.0f);

%feature("shadow") SbColor4f::SbColor4f %{
def __init__(self,*args):
   newobj = None
   if len(args) == 1:
      if isinstance(args[0], SbVec4f):
         newobj = apply(_pivy.new_SbColor4f_vec,args)
      else:
         newobj = apply(_pivy.new_SbColor4f_rgb,args)
   elif len(args) == 2:
      newobj = apply(_pivy.new_SbColor4f_col_f,args)
   elif len(args) == 3:
      newobj = apply(_pivy.new_SbColor4f_ffff,args)
   else:
      newobj = apply(_pivy.new_SbColor4f,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}

%rename(setValue_ffff) SbColor4f::setValue(const float r, const float g, const float b, const float a=1.0f);

%feature("shadow") SbColor4f::setValue(const float col[4]) %{
def setValue(*args):
   if len(args) == 5:
      return apply(_pivy.SbColor4f_setValue_ffff,args)
   return apply(_pivy.SbColor4f_setValue,args)
%}

%rename(setHSVValue_ffff) SbColor4f::setHSVValue(float h, float s, float v, float a=1.0f);

%feature("shadow") SbColor4f::setHSVValue(const float hsv[3], float alpha=1.0f) %{
def setHSVValue(*args):
   if len(args) == 5:
      return apply(_pivy.SbColor4f_setHSVValue_ffff,args)
   return apply(_pivy.SbColor4f_setHSVValue,args)
%}

/* add operator overloading methods instead of the global functions */
%extend SbColor4f {
    SbColor4f __add__(const SbColor4f &u)
    {
        return *self + u;
    };
    
    SbColor4f __sub__(const SbColor4f &u)
    {
       return *self - u;
    };
    
    SbColor4f __mul__(const float d)
    {
       return *self * d;
    };
    
    SbColor4f __rmul__(const float d)
    {
           return *self * d;
    };
    
    SbColor4f __div__(const float d)
    {
        return *self / d;
    };
    
    int __eq__( const SbColor4f &u )
    {
        return *self == u;
    };
    
    int __nq__( const SbColor4f &u )
    {
        return *self != u;
    };
}

%apply float *OUTPUT { float &r, float &g, float &b, float &a };
%apply float *OUTPUT { float &h, float &s, float &v };

%ignore SbColor4f::getValue() const;
%ignore SbColor4f::getHSVValue(float hsv[3]) const;

// add a method for wrapping c++ operator[] access
%extend SbColor4f {
  float __getitem__(int i) {
          return (self->getValue())[i];
  }
}
