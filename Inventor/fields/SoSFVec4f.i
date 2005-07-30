%typemap(in) float xyzw[4] (float temp[4]) {
  convert_SbVec4f_array($input, temp);
  $1 = temp;
}

%extend SoSFVec4f {
  void setValue(const SoSFVec4f * other){
    *self = *other;
  }
}
