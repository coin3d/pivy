%rename(SbString_str) SbString::SbString(const char * str);
%rename(SbString_str_i_i) SbString::SbString(const char * str, int start, int end);
%rename(SbString_i) SbString::SbString(const int digits);

%feature("shadow") SbString::SbString %{
def __init__(self,*args):
   newobj = None
   if len(args) == 1:
      if type(args[0]) == type(1):
         newobj = apply(_pivy.new_SbString_i,args)
      else:
         newobj = apply(_pivy.new_SbString_str,args)
   elif len(args) == 3:
      newobj = apply(_pivy.new_SbString_str_i_i,args)
   else:
      newobj = apply(_pivy.new_SbString,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
%}

%rename(hash_str) SbString::hash(const char * s);

%feature("shadow") SbString::hash(void) %{
def hash(*args):
   if len(args) == 2:
      return apply(_pivy.SbString_hash_str,args)
   return apply(_pivy.SbString_hash,args)
%}

/* add operator overloading methods instead of the global functions */
%extend SbString {      
    int __eq__( const SbString &u )
    {
        return *self == u;
    };
    
    int __nq__( const SbString &u )
    {
        return *self != u;
    };
}

// add a method for wrapping c++ operator[] access
%extend SbString {
  float __getitem__(int i) {
    return (self->getString())[i];
  }
}
