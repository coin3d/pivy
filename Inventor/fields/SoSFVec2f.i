%typemap(in) float xy[2] (float temp[2]) {
  convert_SbVec2f_array($input, temp);
  $1 = temp;
}

%extend SoSFVec2f {
  void setValue(const SoSFVec2f * other){
    *self = *other;
  }
}
