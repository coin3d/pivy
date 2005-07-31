%extend SoSFTime {
  void setValue(const SoSFTime * other){
    *self = *other;
  }
}
