%typemap(in) float hsv[3] (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%typemap(in) float rgb[3] (float temp[3]) {
  convert_SbVec3f_array($input, temp);
  $1 = temp;
}

%typemap(typecheck,precedence=SWIG_TYPECHECK_POINTER) float [3] {
    $1 = PySequence_Check($input) ? 1 : 0;
}

%extend SoSFColor {
  void setValue(const SoSFColor * other){
    *self = *other;
  }
}
