%typemap(in) float xyz[3] (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%extend SoSFVec3f {
  void setValue(const SoSFVec3f * other){
    *self = *other;
  }
}
