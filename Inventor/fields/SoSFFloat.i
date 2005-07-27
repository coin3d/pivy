%extend SoSFFloat {
  void __call__(float f) { self->setValue(f); }
}
