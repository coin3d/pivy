%extend SoSFEnum {
  void __call__(int i) { self->setValue(i); }
  void __call__(const SbName name) { self->setValue(name); }
}
