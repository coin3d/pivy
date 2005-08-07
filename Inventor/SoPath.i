/* add operator overloading methods instead of the global functions */
%extend SoPath {      
  int __eq__(const SoPath &u) { return *self == u; }
  int __nq__(const SoPath &u) { return *self != u; }
}
