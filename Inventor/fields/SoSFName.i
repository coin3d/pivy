%extend SoSFName {
  void __call__(char * str) {
    self->setValue(str);
  }
  void __call__(const SbName & name) {
    self->setValue(name);
  }
}
