%extend SbPlane {
  int __eq__(const SbPlane & u) { return *self == u; }
  int __ne__(const SbPlane & u) { return *self != u; }
}
