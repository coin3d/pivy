%rename(SbDict_dict) SbDict::SbDict(const SbDict & from);

%feature("shadow") SbDict::SbDict %{
def __init__(self,*args):
   if type(args[0]) == type(1):
      self.this = apply(_pivy.new_SbDict,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SbDict_dict,args)
   self.thisown = 1
%}

%rename(applyToAll_func_void) SbDict::applyToAll(void (* rtn)(unsigned long key, void * value, void * data),
												 void * data) const;

%feature("shadow") SbDict::applyToAll(void (* rtn)(unsigned long key, void * value)) %{
def applyToAll(*args):
   if len(args) == 3:
      return apply(_pivy.SbDict_applyToAll_func_void,args)
   return apply(_pivy.SbDict_applyToAll,args)
%}
