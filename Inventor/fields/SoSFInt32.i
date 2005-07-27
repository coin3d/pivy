typedef int int32_t;

%extend SoSFInt32 {
  void __call__(int i) { self->setValue(i); }
}
