%rename(SbDict_dict) SbDict::SbDict(const SbDict & from);

%feature("shadow") SbDict::SbDict %{
def __init__(self,*args):
   newobj = None
   if type(args[0]) == type(1):
      newobj = apply(_pivy.new_SbDict,args)
   else:
      newobj = apply(_pivy.new_SbDict_dict,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}

%rename(applyToAll_func_void) SbDict::applyToAll(void (* rtn)(unsigned long key, void * value, void * data),
                                                 void * data) const;

%feature("shadow") SbDict::applyToAll(void (* rtn)(unsigned long key, void * value)) %{
def applyToAll(*args):
   if len(args) == 3:
      return apply(_pivy.SbDict_applyToAll_func_void,args)
   return apply(_pivy.SbDict_applyToAll,args)
%}
