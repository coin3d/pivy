%rename(hash_str) SbString::hash(const char * s);

%feature("shadow") SbString::hash(void) %{
def hash(*args):
   if len(args) == 2:
      return apply(_coin.SbString_hash_str,args)
   return apply(_coin.SbString_hash,args)
%}

/* add operator overloading methods instead of the global functions */
%extend SbString {      
  int __eq__(const SbString &u) { return *self == u; }
  int __nq__(const SbString &u) { return *self != u; }
  int __eq__(char * u) { return *self == u; }
  int __nq__(char * u) { return *self != u; }
  // add a method for wrapping c++ operator[] access
  char __getitem__(int i) { return (*self)[i]; }
 // iterator for string
%pythoncode %{
  def __iter__(self):
    return getString().__iter__()
%} 
  const char * __repr__(void) { return self->getString(); }
}
