%typemap(in) float rgb[][3] (float (*temp)[3]) {
  int len;

  if (PySequence_Check($input)) {
    len = PySequence_Length($input);

    temp = (float (*)[3]) malloc(len*3*sizeof(float));
    convert_SoMFVec3f_array($input, len, temp);
  
    $1 = temp;
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence.");
  }
}

%typemap(in) float hsv[3] (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%typemap(in) float rgb[3] (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%rename(setValue_col) SoMFColor::setValue(SbColor const &);
%rename(setValue_vec) SoMFColor::setValue(const SbVec3f &vec);
%rename(setValue_fff) SoMFColor::setValue(const float red, const float green, const float blue);

%feature("shadow") SoMFColor::setValue(const float rgb[3]) %{
def setValue(*args):
   if len(args) == 2:
      if isinstance(args[1], SbVec3f):
         return apply(_coin.SoMFColor_setValue_vec,args)
      elif isinstance(args[1], SbColor):
         return apply(_coin.SoMFColor_setValue_col,args)
      else:
         return apply(_coin.SoMFColor_setValue,args)
   elif len(args) == 4:
      return apply(_coin.SoMFColor_setValue_fff,args)
%}

%rename(set1Value_i_col) SoMFColor::set1Value(int const ,SbColor const &);
%rename(set1Value_i_vec) SoMFColor::set1Value(const int idx, const SbVec3f &vec);
%rename(set1Value_i_fff) SoMFColor::set1Value(const int idx, const float r, const float g, const float b);

%feature("shadow") SoMFColor::set1Value(const int idx, const float rgb[3]) %{
def set1Value(*args):
   if len(args) == 3:
      if isinstance(args[2], SbVec3f):
         return apply(_coin.SoMFColor_set1Value_i_vec,args)
      elif isinstance(args[2], SbColor):
         return apply(_coin.SoMFColor_set1Value_i_col,args)
      else:
         return apply(_coin.SoMFColor_set1Value,args)
   elif len(args) == 5:
      return apply(_coin.SoMFColor_set1Value_i_fff,args)
%}

%rename(setHSVValue_fff) SoMFColor::setHSVValue(const float h, const float s, const float v);

%feature("shadow") SoMFColor::setHSVValue(const float hsv[3]) %{
def setHSVValue(*args):
   if len(args) == 4:
      return apply(_coin.SoMFColor_setHSVValue_fff,args)
   return apply(_coin.SoMFColor_setHSVValue,args)
%}

%rename(set1HSVValue_i_fff) SoMFColor::set1HSVValue(const int idx, const float h, const float s, const float v);

%feature("shadow") SoMFColor::set1HSVValue(const int idx, const float hsv[3]) %{
def set1HSVValue(*args):
   if len(args) == 5:
      return apply(_coin.SoMFColor_set1HSVValue_i_fff,args)
   return apply(_coin.SoMFColor_set1HSVValue,args)
%}

%rename(setValues_i_i_col) SoMFColor::setValues(int const ,int const ,SbColor const *);

%feature("shadow") SoMFColor::setValues(const int start, const int num, const float rgb[][3]) %{
def setValues(*args):
   if isinstance(args[3], SbColor):
      return apply(_coin.SoMFColor_setValues_i_i_col,args)
   return apply(_coin.SoMFColor_setValues,args)
%}

%extend SoMFColor {
  void __call__(float rgb[3]) { self->setValue(rgb); }
  void __call__(const SbVec3f & vec) { self->setValue(vec); }
  void __call__(const float r, const float g, const float b) { self->setValue(r,g,b); }
  const SbColor & __getitem__(int i) { return (*self)[i]; }
  void  __setitem__(int i, const SbColor & value) { self->set1Value(i, value); }
}
