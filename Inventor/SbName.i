%rename(SbName_char) SbName::SbName(const char * nameString);
%rename(SbName_str) SbName::SbName(const SbString & str);
%rename(SbName_name) SbName::SbName(const SbName & name);

%feature("shadow") SbName::SbName %{
def __init__(self,*args):
   newobj = None
   if len(args) == 1:
      if isinstance(args[0], SbName):
         newobj = apply(_pivy.new_SbName_str,args)
      elif isinstance(args[0], SbName):
         newobj = apply(_pivy.new_SbName_name,args)
      else:
         newobj = apply(_pivy.new_SbName_char,args)
   else:
      newobj = apply(_pivy.new_SbName,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}

%rename(SbName_eq) operator ==(const SbName & lhs, const SbName & rhs);
%rename(SbName_neq) operator !=(const SbName & lhs, const SbName & rhs);
