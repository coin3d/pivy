%rename(SbString_str) SbString::SbString(const char * str);
%rename(SbString_str_i_i) SbString::SbString(const char * str, int start, int end);
%rename(SbString_i) SbString::SbString(const int digits);

%feature("shadow") SbString::SbString %{
def __init__(self,*args):
   if len(args) == 1:
      if type(args[0]) == type(1):
         self.this = apply(_pivy.new_SbString_i,args)
         self.thisown = 1
         return
      else:
         self.this = apply(_pivy.new_SbString_str,args)
         self.thisown = 1
         return
   elif len(args) == 3:
      self.this = apply(_pivy.new_SbString_str_i_i,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SbString,args)
   self.thisown = 1
%}

%rename(hash_str) SbString::hash(const char * s);

%feature("shadow") SbString::hash(void) %{
def hash(*args):
   if len(args) == 2:
      return apply(_pivy.SbString_hash_str,args)
   return apply(_pivy.SbString_hash,args)
%}

// add a method for wrapping c++ operator[] access
%extend SbString {
  float __getitem__(int i) {
    return (self->getString())[i];
  }
}
