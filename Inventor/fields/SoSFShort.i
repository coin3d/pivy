%extend SoSFShort {
  void __call__(short i) {
    self->setValue(i);
  }
}
