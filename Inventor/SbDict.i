%rename(SbDict_dict) SbDict::SbDict(const SbDict & from);

%feature("shadow") SbDict::SbDict %{
def __init__(self,*args):
   newobj = None
   if type(args[0]) == type(1):
      newobj = apply(_coin.new_SbDict,args)
   else:
      newobj = apply(_coin.new_SbDict_dict,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}
