%extend SoSFBool {
  void __call__(int i) {
    self->setValue(i);
  }
}
