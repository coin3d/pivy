%extend SoSFString {
  void __call__(const SbString & sbstr) {
    self->setValue(sbstr);
  }
  void __call__(char * str) {
    self->setValue(str);
  }
}
